"""Reason Voice — push-to-talk speech control + recipe brain for Reason 12.

Run:  python -m reason_voice.main
Hold the hotkey (default: right Option), speak, release.
"""
import sys
from pathlib import Path

import yaml

from .indexer import PatchIndex
from .intents import parse
from .ptt import PushToTalk
from .reason_control import ReasonControl
from .recipes import RecipeLibrary
from .search import search, similar_to
from .transcribe import Transcriber

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATHS = [Path("config.yaml"), PROJECT_ROOT / "config.yaml"]

HELP = """Say things like:
  "next patch" / "previous patch"      browse patches on the targeted device
  "play" "stop" "record" "loop on"     transport
  "next track" / "previous track"      move the remote target
  "find a warm analog pad"             style-search your patch library
  "load two"                           load/open result #2
  "find something like this"           patches similar to the last one loaded
  "recipe for a trap 808"              search the recipe book
  "sounds like Nirvana drums"          search recipes by reference
  "walk me through it"                 step through the recipe hands-free
  "next step" / "repeat" / "done"      navigate the walkthrough
  "what is Scream 4"                   device reference lookup
  "rebuild index" / "help" / "quit" """


def load_config() -> dict:
    for p in CONFIG_PATHS:
        if p.exists():
            return yaml.safe_load(p.read_text()) or {}
    return {}


class Session:
    """Holds what the user is currently looking at, so short commands
    ('load two', 'next step') resolve against the right list."""

    def __init__(self):
        self.results = []          # last search hits (patches or recipes)
        self.results_kind = None   # "patch" | "recipe"
        self.offset = 0
        self.last_loaded = None    # last loaded patch entry
        self.recipe = None         # currently open Recipe
        self.step = -1             # walkthrough position, -1 = not started


def main():
    cfg = load_config()
    print("Reason Voice v0.2 starting…")

    index = PatchIndex(cfg.get("index_cache", "~/.reason_voice/index.json"))
    folders = cfg.get("patch_folders", ["~/Documents/Reason"])
    n = index.load_or_build(folders)
    print(f"Patch index: {n} patches.")

    library = RecipeLibrary(
        cfg.get("recipes_dir", str(PROJECT_ROOT / "recipes")),
        cfg.get("device_refs_dir", str(PROJECT_ROOT / "device_refs")),
    )
    print(f"Recipe book: {len(library.recipes)} recipes, "
          f"{len(library.device_refs)} device references.")

    control = ReasonControl(
        midi_port_substring=cfg.get("midi_port", "IAC"),
        app_name=cfg.get("reason_app_name", "Reason"),
        speak_feedback=cfg.get("speak_feedback", True),
    )
    print("Loading whisper model (first run downloads it)…")
    stt = Transcriber(cfg.get("whisper_model", "small.en"))
    ptt = PushToTalk(cfg.get("hotkey", "right_option"),
                     cfg.get("max_utterance_seconds", 15))
    per_page = cfg.get("results_per_search", 5)

    print(f"\nReady. Hold [{cfg.get('hotkey', 'right_option')}] and speak. "
          f"Say 'help' for commands.\n")

    s = Session()

    def show(results, kind):
        for i, r in enumerate(results, 1):
            if kind == "recipe":
                print(f"  {i}. {r.summary()}")
            else:
                print(f"  {i}. {r['name']}  [{r['device']}]  ({r['score']})")

    def open_recipe(recipe):
        s.recipe, s.step = recipe, -1
        print("\n" + "=" * 60)
        print(recipe.body.strip())
        print("=" * 60 + "\n")
        control.say(f"{recipe.name}. Accuracy {recipe.accuracy}, {recipe.status}. "
                    f"{len(recipe.steps)} steps. Say walk me through it.")

    def speak_step():
        if s.recipe is None or not s.recipe.steps:
            control.say("No recipe open.")
            return
        i = max(0, min(s.step, len(s.recipe.steps) - 1))
        control.say(f"Step {i + 1} of {len(s.recipe.steps)}. {s.recipe.steps[i]}")

    while True:
        audio = ptt.wait_for_speech()
        text = stt.transcribe(audio)
        if not text:
            continue
        print(f"<< {text}")
        intent = parse(text)
        cmd, args = intent.command, intent.args

        # In a walkthrough, a bare "next"/"back" means the step, not the patch
        if s.recipe is not None and s.step >= 0:
            if cmd == "patch_next" and "patch" not in text:
                cmd = "step_next"
            elif cmd == "patch_prev" and "patch" not in text:
                cmd = "step_prev"

        if cmd == "quit":
            control.say("Goodbye.")
            sys.exit(0)
        elif cmd == "help":
            print(HELP)
        elif cmd == "noop":
            continue

        elif cmd in ("patch_next", "patch_prev", "play", "stop", "record",
                     "track_next", "track_prev", "undo", "redo", "loop"):
            if not control.tap(cmd if cmd != "loop" else "loop"):
                control.say("MIDI bridge not connected.")

        elif cmd == "reindex":
            n = index.rebuild(folders)
            control.say(f"Reindexed. {n} patches.")

        elif cmd in ("find", "find_and_load"):
            query = args.get("query", "")
            s.results = search(index.entries, query, per_page * 3)
            s.results_kind, s.offset = "patch", 0
            hits = s.results[:per_page]
            if not hits:
                control.say(f"No patches matching {query}.")
            elif cmd == "find_and_load":
                s.last_loaded = hits[0]
                control.load_patch(hits[0]["path"])
                control.say(f"Loaded {hits[0]['name']}.")
            else:
                control.say(f"{len(s.results)} matches. Top {len(hits)}:")
                show(hits, "patch")

        elif cmd == "recipe_find":
            query = args.get("query", "")
            s.results = library.search(query, per_page)
            s.results_kind, s.offset = "recipe", 0
            if not s.results:
                control.say(f"No recipe for {query} yet. It can be added.")
            elif len(s.results) == 1:
                open_recipe(s.results[0])
            else:
                control.say(f"{len(s.results)} recipes:")
                show(s.results, "recipe")

        elif cmd == "load_result":
            which = args.get("which", 1) - 1 + s.offset
            if not (0 <= which < len(s.results)):
                control.say("No such result.")
            elif s.results_kind == "recipe":
                open_recipe(s.results[which])
            else:
                s.last_loaded = s.results[which]
                control.load_patch(s.last_loaded["path"])
                control.say(f"Loaded {s.last_loaded['name']}.")

        elif cmd == "more_results":
            s.offset += per_page
            hits = s.results[s.offset:s.offset + per_page]
            if hits:
                show(hits, s.results_kind or "patch")
            else:
                control.say("No more results.")

        elif cmd == "find_like_last":
            if s.last_loaded is None:
                control.say("Nothing loaded yet to compare against.")
                continue
            s.results = similar_to(index.entries, s.last_loaded, 15)
            s.results_kind, s.offset = "patch", 0
            hits = s.results[:per_page]
            if hits:
                control.say(f"Similar to {s.last_loaded['name']}:")
                show(hits, "patch")
            else:
                control.say("No similar patches found.")

        elif cmd == "walkthrough":
            if s.recipe is None and s.results_kind == "recipe" and s.results:
                s.recipe = s.results[0]
            if s.recipe is None:
                control.say("Open a recipe first. Say, recipe for, then a sound.")
                continue
            s.step = 0
            control.say(f"Walking through {s.recipe.name}.")
            speak_step()

        elif cmd == "step_next":
            if s.recipe is None:
                control.say("No walkthrough running.")
            elif s.step >= len(s.recipe.steps) - 1:
                control.say(f"That was the last step. Technique learned: "
                            f"{s.recipe.technique or 'see the recipe notes'}.")
                s.step = -1
            else:
                s.step += 1
                speak_step()

        elif cmd == "step_prev":
            if s.recipe is not None and s.step > 0:
                s.step -= 1
            speak_step()

        elif cmd == "step_repeat":
            speak_step()

        elif cmd == "walkthrough_done":
            if s.recipe is not None:
                control.say(f"Closed {s.recipe.name}.")
            s.recipe, s.step = None, -1

        elif cmd == "device_ref":
            name = args.get("name", "")
            path = library.device_ref(name)
            if path is None:
                control.say(f"No device reference for {name} yet.")
            else:
                body = path.read_text(encoding="utf-8")
                print("\n" + body.strip() + "\n")
                first_para = next((ln for ln in body.splitlines()
                                   if ln.strip() and not ln.startswith("#")), "")
                control.say(first_para)


if __name__ == "__main__":
    main()
