"""Reason Voice v2 — local web UI.

Run:  python -m reason_voice.server   (ReasonVoice.command does this)
Serves http://localhost:<web_port> and auto-opens it in the browser.

One always-visible window: listening state, transcript, recipe card with the
current walkthrough step highlighted, and buttons duplicating every voice
command. Voice is optional — push-to-talk is a hold-down button (or spacebar)
in the page, audio is captured by this process via sounddevice, so no
Input Monitoring permission is needed anymore.
"""
from __future__ import annotations

import asyncio
import json
import os
import signal
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional

import uvicorn
import yaml
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import dial_llm
from .crates import Crates
from .indexer import PatchIndex, REX_EXTENSIONS, bins, tokenize
from .intents import Intent, parse
from .midi_ptt import MidiPTT
from .reason_control import ReasonControl
from .recipes import Recipe, RecipeLibrary, parse_recipe, split_sections
from .search import filter_by_bpm, filter_by_kind, search, similar_to
from .templates import TemplateLibrary
from .webaudio import WebRecorder

PROJECT_ROOT = Path(__file__).parent.parent
STATIC_DIR = Path(__file__).parent / "static"
CONFIG_PATHS = [Path("config.yaml"), PROJECT_ROOT / "config.yaml"]
SETTINGS_PATH = Path(os.path.expanduser("~/.reason_voice/ui_settings.json"))
REASON_TEMPLATE_SONGS = ("~/Library/Application Support/"
                         "Propellerhead Software/Reason/Template Songs")

# The only device with a Scope block in the remotemap and a calibration
# table. Adding a second one is a remotemap block + a calibrate.py run,
# not a code change here.
DIAL_DEVICE = "MClass Compressor"

NO_MIDI = ("MIDI bridge not connected — enable the IAC Driver "
           "and restart Reason.")

# v2 drops spoken `say` feedback by default — visual instead, toggle in settings.
DEFAULT_SETTINGS = {
    "speak_feedback": False,
    "whisper_model": "small.en",
    "results_per_search": 20,
}

HELP_ITEMS = [
    ("next patch / previous patch", "browse patches on the targeted device"),
    ("play · stop · record · loop on/off", "transport"),
    ("next track / previous track", "move the remote target"),
    ("undo / redo", "edit history"),
    ("recipe for a trap 808", "search the recipe book"),
    ("sounds like Nirvana drums", "search recipes by reference"),
    ("walk me through it", "step through the open recipe"),
    ("next step · repeat · done", "navigate the walkthrough"),
    ("what is Scream 4", "device reference lookup"),
    ("what is the drum pads / my interface", "your Launchkey + AudioBox guides, plain English"),
    ("new session from trap 808", "start a song from a saved template"),
    ("save as template · templates", "add the open recipe to the template library / list it"),
    ("find a warm analog pad", "style-search your saved patches"),
    ("find drum loops / bass samples", "browse audio on your drive by group"),
    ("find 90 bpm drum loops", "tempo-filtered loop search (±5 bpm)"),
    ("claude loops", "your generated drum loop pack, always one command away"),
    ("preview two · stop preview", "audition a sample result right here"),
    ("audition drum loops", "auto-play results one after another"),
    ("skip · that one", "next audition sound / load the one playing"),
    ("star two · add two to my drums crate", "save finds into crates"),
    ("my favorites / open drums crate", "browse a crate"),
    ("it worked · note: used damage 35", "mark the open recipe tested / add a session note"),
    ("load two", "load/open result #2"),
    ("find something like this", "patches similar to the last one loaded"),
    ("give it more punch", "move a knob on the locked device — say what you\n"
     "     want it to sound like, not a number"),
    ("set the attack to 30 milliseconds", "or name the exact value"),
    ("more results / rebuild index / help / quit", "housekeeping"),
]


def load_config() -> dict:
    for p in CONFIG_PATHS:
        if p.exists():
            return yaml.safe_load(p.read_text()) or {}
    return {}


def load_settings(cfg: dict) -> dict:
    s = dict(DEFAULT_SETTINGS)
    s["whisper_model"] = cfg.get("whisper_model", s["whisper_model"])
    s["results_per_search"] = cfg.get("results_per_search", s["results_per_search"])
    if SETTINGS_PATH.exists():
        try:
            s.update(json.loads(SETTINGS_PATH.read_text()))
        except (ValueError, OSError):
            pass
    return s


def save_settings(s: dict):
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(s, indent=2))


def recipe_summary(r: Recipe) -> dict:
    return {
        "path": str(r.path), "name": r.name, "book": r.book,
        "accuracy": r.accuracy, "status": r.status,
        "sounds_like": str(r.sounds_like or ""),
    }


def recipe_card(r: Recipe) -> dict:
    d = recipe_summary(r)
    d["technique"] = str(r.technique or "")
    d["steps"] = r.steps
    d["sections"] = split_sections(r.body)
    return d


def patch_row(p: dict) -> dict:
    return {"name": p["name"], "device": p["device"],
            "score": p.get("score"), "path": p["path"],
            "kind": p.get("kind", "patch"), "folder": p.get("folder", "")}


class Session:
    """What the user is currently looking at, so short commands
    ('load two', 'next step') resolve against the right list."""

    def __init__(self):
        self.results = []          # last search hits (patches or recipes)
        self.results_kind = None   # "patch" | "recipe"
        self.offset = 0
        self.last_loaded = None
        self.recipe: Optional[Recipe] = None
        self.step = -1             # -1 = walkthrough not started


class WebApp:
    def __init__(self):
        print("Reason Voice v2 starting…")
        self.cfg = load_config()
        self.settings = load_settings(self.cfg)
        self.status = "idle"            # idle | recording | thinking
        self.model_ready = False
        self.transcript = ""
        self.feedback = "Loading the speech model — buttons work already."
        self.s = Session()
        self.clients: set = set()
        self.stt = None

        self.index = PatchIndex(self.cfg.get("index_cache", "~/.reason_voice/index.json"))
        self.folders = list(self.cfg.get("patch_folders", ["~/Documents/Reason"]))
        for f in self.cfg.get("sample_folders", []) or []:
            if f not in self.folders:
                self.folders.append(f)
        # instant startup: serve whatever cache exists, rescan in background
        self.index_state = self.index.load_cached()
        self._preview_proc = None
        np_, ns = self._index_counts()
        print(f"Index cache: {np_} patches, {ns} samples ({self.index_state}"
              " — will refresh in the background)"
              if self.index_state != "fresh" else
              f"Index cache: {np_} patches, {ns} samples.")
        self.crates = Crates()
        self.audition_active = False
        self.audition_i = -1
        self.midi_ptt = None
        self.midi_ports = []
        self.lan_url = None
        self.loop = None
        self.library = RecipeLibrary(
            self.cfg.get("recipes_dir", str(PROJECT_ROOT / "recipes")),
            self.cfg.get("device_refs_dir", str(PROJECT_ROOT / "device_refs")),
            self.cfg.get("theory_dir", str(PROJECT_ROOT / "theory")),
        )
        self.control = ReasonControl(
            midi_port_substring=self.cfg.get("midi_port", "IAC"),
            app_name=self.cfg.get("reason_app_name", "Reason"),
            speak_feedback=False,   # server speaks via self.say, never via control
        )
        # Dial: knob names come from the remotemap Reason itself reads, and
        # what each position MEANS comes from the sweep measured off Reason.
        self.dial_knobs = dial_llm.knob_map(DIAL_DEVICE)
        self.dial_cal = dial_llm.load_calibration()
        self.dial_undo = None      # one slot: {knob, pos, param, shown}
        self.recorder = WebRecorder(self.cfg.get("max_utterance_seconds", 15))
        self.templates = TemplateLibrary(
            self.cfg.get("templates_dir", str(PROJECT_ROOT / "templates")))
        Path(self.templates.dir).mkdir(parents=True, exist_ok=True)
        self.sessions_dir = self.cfg.get(
            "sessions_dir", "~/Music/Reason 12/Sessions")

    # -- state broadcast -------------------------------------------------

    def dial_state(self) -> dict:
        """The 8 knobs as Reason last reported them.

        `locked` is simply "Reason has spoken to us" — an effect device only
        reaches this surface once it is Ctrl-clicked -> Lock to ReasonVoice,
        so silence and not-locked are the same thing from here.
        """
        c = self.control
        ends = {}
        for _param, e in (self.dial_cal.get(DIAL_DEVICE) or {}).items():
            table = e.get("table") or []
            if table:
                ends[e.get("knob")] = (table[0][1], table[-1][1])
        knobs = []
        for n in range(1, 9):
            knob = "knob_%d" % n
            reported, shown = c.displays.get(knob, ("", ""))
            lo, hi = ends.get(knob, ("", ""))
            knobs.append({
                "knob": knob,
                # Reason's own name for the parameter beats the remotemap's
                "param": reported or self.dial_knobs.get(knob, knob),
                "pos": c.positions.get(knob),
                "shown": shown,
                "lo": lo, "hi": hi,
            })
        return {"device": DIAL_DEVICE, "locked": bool(c.positions),
                "knobs": knobs, "undo": self.dial_undo}

    def snapshot(self) -> dict:
        per_page = self.per_page
        page = self.s.results[self.s.offset:self.s.offset + per_page]
        if self.s.results_kind == "recipe":
            rows = [recipe_summary(r) for r in page]
        else:
            rows = [patch_row(p) for p in page]
        return {
            "type": "state",
            "status": self.status,
            "model_ready": self.model_ready,
            "midi_connected": self.control.port is not None,
            "transcript": self.transcript,
            "feedback": self.feedback,
            "results": rows,
            "results_kind": self.s.results_kind,
            "results_total": len(self.s.results),
            "results_offset": self.s.offset,
            "recipe": recipe_card(self.s.recipe) if self.s.recipe else None,
            "step": self.s.step,
            "templates": self.templates.items(),
            "recipe_template": (
                (self.templates.for_recipe(self.s.recipe.name) or {}).get("name")
                if self.s.recipe else None),
            "crates": self.crates.summary(),
            "dial": self.dial_state(),
            "audition": self.audition_i if self.audition_active else -1,
            "info": {"lan_url": self.lan_url,
                     "midi_ptt_ports": self.midi_ports,
                     "midi_ptt_cc": self.cfg.get("midi_ptt_cc", 64)},
            "settings": self.settings,
        }

    async def broadcast(self, msg: dict):
        """Send ONE message to every client. Split out from push() so the dial
        tick can send its small panel update instead of the whole snapshot
        five times a second."""
        text = json.dumps(msg)
        dead = []
        for ws in self.clients:
            try:
                await ws.send_text(text)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.clients.discard(ws)

    async def push(self, extra: Optional[dict] = None):
        await self.broadcast(self.snapshot())
        if extra:
            await self.broadcast(extra)

    @property
    def per_page(self) -> int:
        return int(self.settings.get("results_per_search", 5))

    def say(self, text: str):
        self.feedback = text
        if self.settings.get("speak_feedback"):
            subprocess.Popen(["say", "-r", "220", text])

    def _index_counts(self):
        n_samples = sum(1 for e in self.index.entries
                        if e.get("kind") == "sample")
        return len(self.index.entries) - n_samples, n_samples

    def _result_at(self, which) -> Optional[dict]:
        """Page-relative 1-based result number -> index entry (patches/samples
        only, never recipes)."""
        if self.s.results_kind != "patch":
            return None
        i = int(which) - 1 + self.s.offset
        if 0 <= i < len(self.s.results):
            return self.s.results[i]
        return None

    def _preview_stop(self):
        if self._preview_proc is not None and self._preview_proc.poll() is None:
            self._preview_proc.kill()
        self._preview_proc = None

    def _stop_audition(self):
        self.audition_active = False
        self._preview_stop()

    async def _audition_loop(self):
        """Play results one after another until stopped, picked, or done.
        'skip' kills the current afplay, which advances the loop."""
        s = self.s
        while (self.audition_active and s.results_kind == "patch"
               and 0 <= self.audition_i < len(s.results)
               and isinstance(s.results[self.audition_i], dict)):
            entry = s.results[self.audition_i]
            s.offset = (self.audition_i // self.per_page) * self.per_page
            await self.push()
            path = entry.get("path", "")
            if (entry.get("kind") == "sample"
                    and Path(path).suffix.lower() not in REX_EXTENSIONS):
                self._preview_stop()
                self._preview_proc = subprocess.Popen(["afplay", path])
                proc = self._preview_proc
                await asyncio.to_thread(proc.wait)
                await asyncio.sleep(0.25)   # breath between sounds
            if not self.audition_active:
                break
            self.audition_i += 1
        if self.audition_active:
            self.audition_active = False
            self.say("End of results. Say a new search, or, more results.")
        await self.push()

    # -- model loading ---------------------------------------------------

    def _vocabulary(self) -> str:
        """Command words + his actual library names, fed to whisper as a
        decoding bias so 'Klang' and 'walkthrough' stop coming out mangled."""
        words = ["Reason Voice commands: next patch, previous patch, play, "
                 "stop, record, loop, undo, redo, next track, walk me "
                 "through it, next step, repeat, done, recipe for, sounds "
                 "like, find, load, preview, audition, skip, that one, "
                 "star, crate, favorites, new session from, save as "
                 "template, templates, rebuild index, what is, more "
                 "results, find something like this, drum loops, bass "
                 "samples, bpm, Klang, Kong, Combinator, SubTractor, "
                 "Malström, Redrum, NN-XT, Scream 4, RV7000, ReGroove."]
        words += [r.name for r in self.library.recipes]
        words += list(self.library.device_refs)
        words += [t["name"] for t in self.templates.items()]
        return " ".join(words)

    async def load_model(self, name: str):
        self.model_ready = False
        self.say(f"Loading {name} speech model…")
        await self.push()
        vocab = self._vocabulary()

        def _load():
            from .transcribe import Transcriber
            return Transcriber(name, vocabulary=vocab)

        try:
            self.stt = await asyncio.to_thread(_load)
            self.model_ready = True
            self.say("Ready. Hold the talk button (or spacebar) and speak.")
        except Exception as e:  # model download failed etc.
            self.say(f"Speech model failed to load: {e}. Buttons still work.")
        await self.push()

    # -- push-to-talk ----------------------------------------------------

    async def ptt_start(self):
        if self.status != "idle":
            return
        if not self.model_ready:
            self.say("Still loading the speech model — one moment.")
            await self.push()
            return
        self.recorder.start()
        self.status = "recording"
        await self.push()

    async def ptt_stop(self):
        if self.status != "recording":
            return
        audio = self.recorder.stop()
        self.status = "thinking"
        await self.push()
        text = await asyncio.to_thread(self.stt.transcribe, audio)
        self.status = "idle"
        if not text:
            self.say("Didn't catch that.")
            await self.push()
            return
        await self.run_text(text)

    # -- command execution -------------------------------------------------

    def _contextualize(self, intent: Intent, text: str) -> Intent:
        cmd = intent.command
        # While auditioning, "next"/"skip" advance the audition and a bare
        # "stop" ends it rather than hitting the transport
        if self.audition_active:
            if cmd == "patch_next" and "patch" not in text:
                cmd = "audition_skip"
            elif cmd == "stop" and text.strip() == "stop":
                cmd = "preview_stop"
        # In a walkthrough, a bare "next"/"back" means the step, not the patch
        elif self.s.recipe is not None and self.s.step >= 0:
            if cmd == "patch_next" and "patch" not in text:
                cmd = "step_next"
            elif cmd == "patch_prev" and "patch" not in text:
                cmd = "step_prev"
        return Intent(cmd, intent.args)

    async def run_text(self, text: str):
        self.transcript = text
        intent = self._contextualize(parse(text), text.lower())
        await self.execute(intent)

    def _reload_recipe(self, path):
        fresh = parse_recipe(Path(path))
        for i, r in enumerate(self.library.recipes):
            if str(r.path) == str(path):
                self.library.recipes[i] = fresh
                break
        if self.s.recipe is not None and str(self.s.recipe.path) == str(path):
            step = self.s.step
            self.s.recipe, self.s.step = fresh, step

    def _open_recipe(self, recipe: Recipe):
        self.s.recipe, self.s.step = recipe, -1
        self.say(f"{recipe.name}. Accuracy {recipe.accuracy}, {recipe.status}. "
                 f"{len(recipe.steps)} steps. Walk through it when ready.")

    @staticmethod
    def _load_hint(entry) -> str:
        """After loading a drum patch, remind him the pads just work."""
        if "drum" in entry.get("device", ""):
            return (" Launchkey pads play it — Shift + Pad Mode, pick Drum. "
                    "(Ask: what is the drum pads.)")
        return ""

    def _dial_note(self, knob, got):
        """Remember where a knob was, so one Undo can put it back.
        `got` is control.current(knob) — already polled by the caller."""
        if got is None:
            self.dial_undo = None
            return
        pos, name, shown = got
        self.dial_undo = {"knob": knob, "pos": pos, "shown": shown,
                          "param": name or self.dial_knobs.get(knob, knob)}

    def _step_feedback(self):
        r = self.s.recipe
        if r is None or not r.steps:
            self.say("No recipe open.")
            return
        i = max(0, min(self.s.step, len(r.steps) - 1))
        self.say(f"Step {i + 1} of {len(r.steps)}. {r.steps[i]}")

    async def execute(self, intent: Intent):
        s, cmd, args = self.s, intent.command, intent.args
        extra = None
        per_page = self.per_page

        if cmd in ("noop", "help"):
            if cmd == "help":
                extra = {"type": "help", "items": HELP_ITEMS}

        elif cmd == "quit":
            self.say("Goodbye. This window can be closed.")
            await self.push()
            asyncio.get_running_loop().call_later(
                0.8, lambda: os.kill(os.getpid(), signal.SIGINT))
            return

        elif cmd in ("patch_next", "patch_prev", "play", "stop", "record",
                     "track_next", "track_prev", "undo", "redo", "loop"):
            if self.control.tap(cmd):
                self.say(cmd.replace("_", " ").capitalize() + ".")
            else:
                self.say(NO_MIDI)

        elif cmd == "dial":
            phrase = (args.get("phrase") or "").strip()
            self.control.poll()   # a lock that just happened may be waiting
            if not self.control.positions:
                self.say("Nothing is locked to ReasonVoice. In Reason, "
                         "Ctrl-click the device panel and choose “Lock to "
                         "ReasonVoice” — then nudge any knob once so it says "
                         "hello.")
            elif not phrase:
                self.say("Say what you want it to do — like: give it more punch.")
            else:
                self.status = "thinking"
                await self.push()
                # re-read so a fresh calibrate.py run needs no restart
                self.dial_cal = dial_llm.load_calibration()
                answer = await asyncio.to_thread(
                    dial_llm.choose, phrase, DIAL_DEVICE)
                self.status = "idle"
                if answer is None:
                    self.say(f"Couldn’t turn “{phrase}” into a knob move. Try "
                             "naming the feel (more punch, squash it harder) "
                             "or the value (attack to 30 milliseconds).")
                else:
                    knob = answer["knob"]
                    got = self.control.current(knob)
                    name = ((got[1] if got else "")
                            or self.dial_knobs.get(knob, knob))
                    asked = answer.get("target") or answer.get("delta")
                    placed = dial_llm.resolve(
                        answer, DIAL_DEVICE,
                        current_pos=(got[0] if got else None),
                        calibration=self.dial_cal)
                    if placed is None:
                        self.say(f"{name}: can’t place “{asked}”. Percentages "
                                 "always work; real units only where that knob "
                                 "has been calibrated.")
                    else:
                        pos, note = placed
                        self._dial_note(knob, got)
                        if self.control.set_value(knob, pos):
                            why = answer.get("why") or ""
                            self.say(f"{name} → {asked} ({note})."
                                     + (f" {why}" if why else ""))
                        else:
                            self.dial_undo = None
                            self.say(NO_MIDI)

        elif cmd == "dial_set":
            knob = str(args.get("knob", ""))
            try:
                value = int(args.get("value"))
            except (TypeError, ValueError):
                value = None
            if value is None:
                self.say("No value for that knob.")
            else:
                self._dial_note(knob, self.control.current(knob))
                if self.control.set_value(knob, value):
                    self.say("%s → position %d."
                             % (self.dial_knobs.get(knob, knob), value))
                else:
                    self.dial_undo = None
                    self.say(NO_MIDI)

        elif cmd == "dial_undo":
            u = self.dial_undo
            if u is None:
                self.say("Nothing to put back.")
            elif self.control.set_value(u["knob"], u["pos"]):
                self.dial_undo = None
                self.say("Put %s back to %s."
                         % (u["param"], u["shown"] or "position %d" % u["pos"]))
            else:
                self.say(NO_MIDI)

        elif cmd == "reindex":
            await asyncio.to_thread(self.index.rebuild, self.folders)
            np_, ns = self._index_counts()
            self.say(f"Reindexed. {np_} patches, {ns} samples.")
            extra = {"type": "bins", "bins": bins(self.index.entries)}

        elif cmd in ("find", "find_and_load"):
            self._stop_audition()
            query = args.get("query", "")
            pool = filter_by_kind(self.index.entries, tokenize(query))
            browsing_samples = pool is not self.index.entries
            pool = filter_by_bpm(pool, query)
            cap = 200 if browsing_samples else per_page * 3
            s.results = search(pool, query, cap)
            s.results_kind, s.offset = "patch", 0
            if not s.results:
                if browsing_samples:
                    self.say(f"No loose samples matching “{query}”. Add your "
                             "sample folders to config.yaml and rebuild the "
                             "index. (Audio inside ReFills can't be scanned.)")
                else:
                    self.say(f"No patches matching “{query}”. (Patches inside "
                             "ReFills and the Factory Sound Bank can't be "
                             "searched.)")
            elif cmd == "find_and_load":
                s.last_loaded = s.results[0]
                self.control.load_patch(s.last_loaded["path"])
                self.say(f"Loaded {s.last_loaded['name']}."
                         + self._load_hint(s.last_loaded))
            else:
                self.say(f"{len(s.results)} matches for “{query}”.")

        elif cmd == "recipe_find":
            self._stop_audition()
            query = args.get("query", "")
            s.results = self.library.search(query, per_page)
            s.results_kind, s.offset = "recipe", 0
            if not s.results:
                self.say(f"No recipe for “{query}” yet. It can be added.")
            elif len(s.results) == 1:
                self._open_recipe(s.results[0])
            else:
                self.say(f"{len(s.results)} recipes for “{query}”.")

        elif cmd == "load_result":
            which = int(args.get("which", 1)) - 1 + s.offset
            if not (0 <= which < len(s.results)):
                self.say("No such result.")
            elif s.results_kind == "recipe":
                self._open_recipe(s.results[which])
            elif s.results[which].get("kind") == "folder":
                # a Claude-loops folder row: opening it lists its beats,
                # same as clicking it — so "load two" works by voice too
                await self.execute(Intent(
                    "claude_loops", {"folder": s.results[which]["name"]}))
                return
            else:
                s.last_loaded = s.results[which]
                self.control.load_patch(s.last_loaded["path"])
                if s.last_loaded.get("kind") == "sample":
                    self.say(f"Sent {s.last_loaded['name']} to Reason — if "
                             "nothing happened, hit Reveal and drag it in.")
                else:
                    self.say(f"Loaded {s.last_loaded['name']}."
                             + self._load_hint(s.last_loaded))

        elif cmd == "preview_result":
            entry = self._result_at(args.get("which", 1))
            if entry is None:
                self.say("No such result to preview.")
            elif entry.get("kind") != "sample":
                self.say("Preview is for samples — patches load straight "
                         "into Reason.")
            elif Path(entry["path"]).suffix.lower() in REX_EXTENSIONS:
                self.say("REX loops can't be previewed here — reveal it in "
                         "Finder and drag it into Reason.")
            else:
                self._preview_stop()
                self._preview_proc = subprocess.Popen(["afplay", entry["path"]])
                self.say(f"Previewing {entry['name']}.")

        elif cmd == "preview_stop":
            was_audition = self.audition_active
            self._stop_audition()
            self.say("Audition stopped." if was_audition else "Preview stopped.")

        elif cmd == "audition":
            query = args.get("query", "")
            if query:
                pool = filter_by_bpm(
                    filter_by_kind(self.index.entries, tokenize(query)),
                    query)
                s.results = search(pool, query, 200)
                s.results_kind, s.offset = "patch", 0
            if s.results_kind != "patch" or not s.results:
                self.say("Nothing to audition — search for samples first, "
                         "like: audition drum loops.")
            else:
                self._stop_audition()
                self.audition_active = True
                self.audition_i = s.offset
                self.say(f"Auditioning {len(s.results)} sounds — say skip, "
                         "or, that one.")
                asyncio.create_task(self._audition_loop())

        elif cmd == "audition_skip":
            if self.audition_active:
                self._preview_stop()   # loop advances on its own
                return                 # loop pushes state; no double-say
            self.say("No audition running.")

        elif cmd == "audition_pick":
            if self.audition_active and 0 <= self.audition_i < len(s.results):
                entry = s.results[self.audition_i]
                self._stop_audition()
                s.last_loaded = entry
                self.control.load_patch(entry["path"])
                self.say(f"Loaded {entry['name']}. Star it to keep it — "
                         "say, star it, or, add it to a crate.")
            else:
                self.say("No audition running.")

        elif cmd == "crate_add":
            which = args.get("which")
            entry = (self._result_at(which) if which is not None
                     else (s.results[self.audition_i]
                           if self.audition_active else s.last_loaded))
            if entry is None or "path" not in entry:
                self.say("No such result to star.")
            else:
                crate = self.crates.add(args.get("crate", "favorites"), entry)
                self.say(f"Added {entry['name']} to the {crate} crate.")

        elif cmd == "crate_remove":
            entry = self._result_at(args.get("which", 1))
            if entry is not None and self.crates.remove_anywhere(entry["path"]):
                self.say(f"Removed {entry['name']} from your crates.")
            else:
                self.say("That one isn't in a crate.")

        elif cmd == "claude_loops":
            # Grouped by DJ / genre (owner ask 2026-07-25): the beat library
            # is already organized as one folder per identity, so the first
            # click shows those folders as a browsable list; clicking (or
            # "load two") opens one. Stems folders are skipped — a beat's 13
            # solo'd lanes would bury the beats — and so is Trash: that's
            # his reject pile, resurfacing it here would undo the triage.
            self._stop_audition()
            markers = (os.sep + "Claude Drum Loops" + os.sep,
                       os.sep + "Claude Drum Beats" + os.sep)

            def _place(e):
                """(folder shown in the browser, its dir) or None."""
                p = e["path"]
                for mk in markers:
                    j = p.find(mk)
                    if j < 0:
                        continue
                    rest = p[j + len(mk):].split(os.sep)
                    if any(part.endswith(" Stems") for part in rest[:-1]):
                        return None
                    if rest[0] == "Trash":
                        return None
                    top = rest[0] if len(rest) > 1 else \
                        mk.strip(os.sep).replace("Claude ", "")
                    return top, p[:j + len(mk)] + (rest[0] if len(rest) > 1
                                                   else "")
                return None

            def _hits():
                return [(e, pl) for e in self.index.entries
                        for pl in (_place(e),) if pl]
            hits = _hits()
            if not hits:
                self.say("Picking up the Claude loops — refreshing the "
                         "index, a few seconds…")
                await self.push()
                await asyncio.to_thread(self.index.rebuild, self.folders)
                hits = _hits()
            want = args.get("folder")
            if want:
                sel = sorted((e for e, (top, _d) in hits if top == want),
                             key=lambda e: e["name"].lower())
                s.results, s.results_kind, s.offset = sel, "patch", 0
                self.say(f"{len(sel)} in {want}. Say audition, or preview "
                         "a number.")
            elif hits:
                groups: dict = {}
                for e, (top, d) in hits:
                    n, _d = groups.get(top, (0, d))
                    groups[top] = (n + 1, d)
                rows = [{"name": top, "kind": "folder", "path": d,
                         "device": f"{n} to hear",
                         "folder": ""}
                        for top, (n, d) in sorted(groups.items(),
                                                  key=lambda kv: kv[0].lower())]
                s.results, s.results_kind, s.offset = rows, "patch", 0
                self.say(f"{len(rows)} folders of Claude beats and loops — "
                         "by DJ and genre. Open one, or say load two.")
            else:
                self.say("No Claude loops on disk yet — ask Claude in chat "
                         "to generate a pack.")

        elif cmd == "crate_open":
            name = args.get("name", "favorites")
            entries = self.crates.entries(name)
            if not entries:
                self.say(f"The {name} crate is empty. Star results to "
                         "fill it.")
            else:
                self._stop_audition()
                s.results, s.results_kind, s.offset = entries, "patch", 0
                self.say(f"{len(entries)} in the {name} crate.")

        elif cmd == "recipe_tested":
            r = s.recipe
            if r is None:
                self.say("Open a recipe first.")
            elif r.status == "tested":
                self.say(f"{r.name} is already marked tested.")
            else:
                text = Path(r.path).read_text(encoding="utf-8")
                new = text.replace("status: theoretical", "status: tested", 1)
                if new == text:
                    self.say("Couldn't find the status line in that recipe.")
                else:
                    Path(r.path).write_text(new, encoding="utf-8")
                    self._reload_recipe(r.path)
                    self.say(f"Marked {r.name} as tested. The book gets "
                             "more honest every time you do that.")

        elif cmd == "recipe_note":
            r = s.recipe
            note = args.get("text", "").strip()
            if r is None:
                self.say("Open a recipe first, then say: note, and the note.")
            elif note:
                text = Path(r.path).read_text(encoding="utf-8")
                if "## Session notes" not in text:
                    text = text.rstrip() + "\n\n## Session notes\n"
                from datetime import date
                text = text.rstrip() + f"\n- {date.today()}: {note}\n"
                Path(r.path).write_text(text, encoding="utf-8")
                self._reload_recipe(r.path)
                self.say("Noted — it's in the recipe card now.")

        elif cmd == "reveal_result":
            entry = self._result_at(args.get("which", 1))
            if entry is None:
                self.say("No such result.")
            else:
                subprocess.run(["open", "-R", entry["path"]])
                self.say(f"Showing {entry['name']} in Finder — drag it "
                         "into Reason.")

        elif cmd == "more_results":
            if s.offset + per_page < len(s.results):
                s.offset += per_page
                self.say("Next page.")
            else:
                self.say("No more results.")

        elif cmd == "find_like_last":
            if s.last_loaded is None:
                self.say("Nothing loaded yet to compare against.")
            else:
                s.results = similar_to(self.index.entries, s.last_loaded, 15)
                s.results_kind, s.offset = "patch", 0
                if s.results:
                    self.say(f"Similar to {s.last_loaded['name']}.")
                else:
                    self.say("No similar patches found.")

        elif cmd == "walkthrough":
            if s.recipe is None and s.results_kind == "recipe" and s.results:
                s.recipe = s.results[0]
            if s.recipe is None:
                self.say("Open a recipe first — pick one from the book on "
                         "the left, or say “recipe for” a sound.")
            else:
                s.step = 0
                self._step_feedback()

        elif cmd == "step_next":
            if s.recipe is None:
                self.say("No walkthrough running.")
            elif s.step >= len(s.recipe.steps) - 1:
                closing = ("That was the last step. Technique learned: "
                           f"{s.recipe.technique or 'see the recipe notes'}.")
                if s.recipe.status == "theoretical":
                    closing += (" Did it work? Say — it worked — to mark "
                                "this recipe tested, or — note — to log "
                                "what you changed.")
                self.say(closing)
                s.step = -1
            else:
                s.step += 1
                self._step_feedback()

        elif cmd == "step_prev":
            if s.recipe is not None and s.step > 0:
                s.step -= 1
            self._step_feedback()

        elif cmd == "step_repeat":
            self._step_feedback()

        elif cmd == "walkthrough_done":
            if s.recipe is not None:
                self.say(f"Closed {s.recipe.name}.")
            s.recipe, s.step = None, -1

        elif cmd == "template_list":
            items = self.templates.items()
            if items:
                self.say(f"{len(items)} templates: " +
                         ", ".join(t["name"] for t in items[:6]) +
                         ("…" if len(items) > 6 else "."))
            else:
                self.say("No templates yet. Open a recipe and say, save as "
                         "template, to see how to make one.")

        elif cmd == "template_start":
            query = args.get("query") or (self.s.recipe.name
                                          if self.s.recipe else "")
            items = self.templates.items()
            if not query and len(items) == 1:
                tpl = items[0]
            else:
                tpl = self.templates.find(query)
            if tpl is None:
                if query:
                    self.say(f"No template called “{query}” yet. Say, save "
                             "as template, to see how to make one.")
                else:
                    self.say("Which template? Say, new session from, then "
                             "its name — or click one in the Templates list.")
            elif tpl["kind"] == "song":
                copy = await asyncio.to_thread(
                    self.templates.new_session, tpl, self.sessions_dir)
                self.control.load_patch(str(copy))
                self.say(f"New session from {tpl['name']} — opening "
                         f"“{copy.stem}” in Reason. The template itself "
                         "stays untouched.")
            else:   # combinator patch: drops into the current song
                self.control.load_patch(tpl["path"])
                self.say(f"Added the {tpl['name']} Combinator to the rack.")

        elif cmd == "template_howto":
            name = self.s.recipe.name if self.s.recipe else "My Template"
            self.say("Here's how to turn a recipe into a template.")
            extra = {"type": "doc", "name": "Save a template", "body": (
                "Reason can't be scripted to build chains, so a template is "
                "built once by hand — then reused forever.\n\n"
                "1. Build the chain by following the recipe walkthrough.\n"
                "2. **Whole-song template:** in Reason choose File → Save As…\n"
                "3. **Just the device chain:** put the devices in a "
                "Combinator (select them → Combine) and click the floppy "
                "icon on the Combinator instead.\n"
                f"4. Save it into the Templates folder and name it "
                f"**{name}** — matching the recipe name links it to the "
                "recipe card automatically.\n"
                "5. It appears in the Templates list right away. Start a "
                f"fresh song anytime with “new session from {name.lower()}” "
                "— each session is a dated copy, so the template is never "
                "overwritten.\n\n"
                "Click the 📂 button next to Templates to open the folder — "
                "drag it into Reason's Save dialog to jump there.")}

        elif cmd == "templates_folder":
            subprocess.run(["open", self.templates.dir])
            self.say("Opened the Templates folder in Finder.")

        elif cmd == "device_ref":
            name = args.get("name", "")
            path = self.library.device_ref(name)
            if path is None:
                self.say(f"No device reference for “{name}” yet.")
            else:
                body = path.read_text(encoding="utf-8")
                self.say(f"Here's the {path.stem.replace('-', ' ')} guide.")
                extra = {"type": "doc", "name": path.stem.replace("-", " "),
                         "body": body}
        else:
            self.say(f"Don't know how to “{cmd}” yet.")

        await self.push(extra)

    # -- websocket message dispatch ---------------------------------------

    async def handle(self, msg: dict):
        t = msg.get("type")
        if t == "ptt_start":
            await self.ptt_start()
        elif t == "ptt_stop":
            await self.ptt_stop()
        elif t == "text":
            await self.run_text(str(msg.get("text", "")).strip())
        elif t == "command":
            await self.execute(Intent(msg.get("command", "noop"),
                                      msg.get("args") or {}))
        elif t == "open_recipe":
            wanted = msg.get("path", "")
            for r in self.library.recipes:
                if str(r.path) == wanted:
                    self._open_recipe(r)
                    break
            await self.push()
        elif t == "set":
            key, value = msg.get("key"), msg.get("value")
            if key in DEFAULT_SETTINGS:
                self.settings[key] = value
                save_settings(self.settings)
                if key == "whisper_model":
                    asyncio.create_task(self.load_model(value))
                else:
                    await self.push()


# Constructed in main() (or by whoever imports us) AFTER the already-running
# check, so a second double-click never re-scans a 68k-file drive just to
# find the port taken.
state: Optional[WebApp] = None
app = FastAPI()


def init_state() -> WebApp:
    global state
    if state is None:
        state = WebApp()
    return state


@app.on_event("startup")
async def startup():
    init_state()   # no-op when main() already built it
    state.loop = asyncio.get_running_loop()
    asyncio.create_task(state.load_model(state.settings["whisper_model"]))
    asyncio.create_task(finish_startup())
    asyncio.create_task(dial_watch())
    port = state.cfg.get("web_port", 8765)

    async def open_browser():
        await asyncio.sleep(0.4)
        webbrowser.open(f"http://localhost:{port}")

    if not os.environ.get("REASON_VOICE_NO_BROWSER"):
        asyncio.create_task(open_browser())


async def dial_watch():
    """Keep the knob panel honest.

    Reason reports a parameter only when it CHANGES, and those reports sit in
    the MIDI input buffer until collected — so something has to collect them.
    Polling here is what makes a knob turned with the MOUSE in Reason move on
    screen too, not just the ones we moved ourselves.

    Sends only the dial panel, never the whole snapshot.
    """
    seen = None
    while True:
        await asyncio.sleep(0.2)
        try:
            state.control.poll()
            now = (dict(state.control.positions), dict(state.control.displays))
            if now != seen:
                seen = now
                await state.broadcast({"type": "dial",
                                       "dial": state.dial_state()})
        except Exception as e:   # a dead MIDI port must not kill the watcher
            print(f"[dial] poll failed: {e}")
            await asyncio.sleep(2)


async def finish_startup():
    """Background chores that must never delay the page: MIDI push-to-talk,
    template mirroring into Reason's own folder, and the index refresh."""
    def _press():
        asyncio.run_coroutine_threadsafe(state.ptt_start(), state.loop)

    def _release():
        asyncio.run_coroutine_threadsafe(state.ptt_stop(), state.loop)

    state.midi_ptt = MidiPTT(
        _press, _release,
        cc=state.cfg.get("midi_ptt_cc", 64),
        note=state.cfg.get("midi_ptt_note"),
        exclude_substring=state.cfg.get("midi_port", "IAC"))
    state.midi_ports = state.midi_ptt.port_names
    if state.midi_ports:
        print(f"MIDI push-to-talk: hold CC {state.cfg.get('midi_ptt_cc', 64)} "
              f"(sustain pedal) on: {', '.join(state.midi_ports)}")

    if state.cfg.get("mirror_templates", True):
        copied = await asyncio.to_thread(
            state.templates.mirror_to,
            state.cfg.get("templates_mirror_dir", REASON_TEMPLATE_SONGS))
        if copied:
            print(f"Mirrored {copied} template(s) into Reason's "
                  "Template Songs folder (File > New From Template).")

    if state.index_state != "fresh":
        n = await asyncio.to_thread(state.index.rebuild, state.folders)
        state.index_state = "fresh"
        np_, ns = state._index_counts()
        print(f"Index refreshed in the background: {np_} patches, "
              f"{ns} samples ({n} total).")
        await state.push({"type": "bins", "bins": bins(state.index.entries)})


@app.middleware("http")
async def no_stale_ui(request, call_next):
    """Force revalidation of the UI files so a server update is never paired
    with a stale cached app.js/style.css in his browser."""
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "no-cache"
    return response


@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/recipes")
async def recipes():
    return JSONResponse([recipe_summary(r) for r in state.library.recipes])


@app.get("/api/bins")
async def sample_bins():
    return JSONResponse(bins(state.index.entries))


@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    state.clients.add(websocket)
    try:
        await websocket.send_text(json.dumps(state.snapshot()))
        while True:
            try:
                msg = json.loads(await websocket.receive_text())
            except ValueError:
                continue
            await state.handle(msg)
    except WebSocketDisconnect:
        pass
    finally:
        state.clients.discard(websocket)


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
# the band's artwork, same files the Beat Machine masthead uses — so both
# rooms wear the exact same mark (owner ask 2026-07-25). One source of
# truth: drop new art in <project>/brand/ and both pages pick it up.
_BRAND_DIR = Path(__file__).parent.parent / "brand"
if _BRAND_DIR.is_dir():
    app.mount("/brand", StaticFiles(directory=str(_BRAND_DIR)), name="brand")


def _port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def _lan_ip():
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return None


def main():
    cfg = load_config()
    port = cfg.get("web_port", 8765)
    if _port_in_use(port):
        # already running (or the old window is still open) — just show it
        print(f"Reason Voice is already running — opening "
              f"http://localhost:{port} in your browser.")
        print("(The running copy lives in another Terminal window. "
              "This window can be closed.)")
        if not os.environ.get("REASON_VOICE_NO_BROWSER"):
            webbrowser.open(f"http://localhost:{port}")
        return
    init_state()
    host = "0.0.0.0" if cfg.get("network_access", True) else "127.0.0.1"
    print(f"Ready — http://localhost:{port}  "
          f"(leave this window open; Ctrl+C here to quit)")
    if host == "0.0.0.0":
        ip = _lan_ip()
        if ip:
            state.lan_url = f"http://{ip}:{port}"
            print(f"Phone/tablet on the same wifi: {state.lan_url}")
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    main()
