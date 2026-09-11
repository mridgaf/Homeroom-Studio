"""Turn a transcript into a (command, args) intent.

Rule-based on purpose: in a studio you want deterministic, instant parsing,
not an LLM round-trip. Extend PATTERNS as your vocabulary grows.

Regex first; if the text would fall through, a fuzzy pass rescues near-miss
command phrases that whisper mangles ("find something like this" heard as
"and something like this"). Whatever survives that is a knob move: the final
fallback is the `dial` command, handled by dial_llm.
"""
import re
from dataclasses import dataclass, field

from rapidfuzz import fuzz

NUM_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
    "to": 2, "too": 2, "for": 4,  # common whisper homophones
}


@dataclass
class Intent:
    command: str
    args: dict = field(default_factory=dict)


# Ordered: first match wins.
PATTERNS = [
    # -- patch browsing (Remote/MIDI) --
    (r"\b(next|forward)\b.*\bpatch\b|\bpatch\b.*\bnext\b|^next$", "patch_next", None),
    (r"\b(previous|prev|back|last)\b.*\bpatch\b|^(back|previous)$", "patch_prev", None),
    # -- the generated Claude loop pack (must outrank transport "play") --
    (r"^(?:open |show |find |play )?(?:my |the )?claude(?:'s)?\s+(?:drum\s+)?loops$", "claude_loops", None),
    # -- sample preview / audition (must outrank transport play/stop) --
    (r"^stop (?:the )?preview$", "preview_stop", None),
    (r"^(?:preview|audition|hear)\s+(?:number\s+)?(\w+)$", "preview_result", "which"),
    (r"^audition$", "audition", None),
    (r"^(?:audition|preview)\s+(.+)$", "audition", "query"),
    (r"^(?:that one|keep (?:it|that|this)|yes,? that(?: one)?|load it)$", "audition_pick", None),
    (r"^skip(?: it)?$", "audition_skip", None),
    # -- crates (favorites) --
    (r"^(?:star|favou?rite)\s+(?:number\s+)?(\w+)$", "crate_add", "which"),
    (r"^add\s+(?:number\s+)?(\w+)\s+to\s+(?:my\s+)?(.+?)(?:\s+crate)?$", "crate_add_to", None),
    (r"^(?:unstar|unfavou?rite)\s+(?:number\s+)?(\w+)$", "crate_remove", "which"),
    (r"^(?:open|show|find)\s+(?:my\s+)?(.+?)\s+crate$", "crate_open", "name"),
    (r"^(?:open|show|find)\s+(?:my\s+)?crate\s+(.+)$", "crate_open", "name"),
    (r"^(?:my\s+)?favou?rites$", "crate_open", None),
    # -- recipe honesty system --
    (r"^(?:it|that) worked$|^mark (?:it |this )?(?:as )?tested$", "recipe_tested", None),
    (r"^(?:add\s+)?note[:,]?\s+(.+)$", "recipe_note", "text"),
    # -- transport --
    (r"^play\b|^start$", "play", None),   # "start a session…" is a template
    (r"^stop\b", "stop", None),
    (r"^record\b", "record", None),
    (r"\bloop (on|off)\b|^loop$", "loop", None),
    (r"^undo\b", "undo", None),
    (r"^redo\b", "redo", None),
    # -- track targeting --
    (r"\b(next|down)\b.*\btrack\b|\btrack\b.*\b(next|down)\b", "track_next", None),
    (r"\b(previous|prev|up)\b.*\btrack\b|\btrack\b.*\b(previous|prev|up)\b", "track_prev", None),
    # -- reindex must outrank recipe search ("rebuild the recipe index") --
    (r"\b(rebuild|refresh|update)\b.*\b(index|library)\b", "reindex", None),
    # -- recipes & walkthrough --
    (r"^(?:next step|step)$", "step_next", None),
    (r"^(?:previous|last|back)\s+step$", "step_prev", None),
    (r"^(?:repeat(?:\s+(?:that|step))?|say (?:that )?again)$", "step_repeat", None),
    (r"^(?:done|finished|end|stop)(?:\s+(?:walkthrough|recipe))?$", "walkthrough_done", None),
    (r"\bwalk me through\b", "walkthrough", None),
    # feelings: "make it feel nostalgic", "how do i make this feel dark"
    (r"^(?:how (?:do|can) i )?make (?:it|this|something|the beat) feel\s+(.+)$", "recipe_find", "query"),
    (r"^i want (?:it|this|the beat) to feel\s+(.+)$", "recipe_find", "query"),
    (r"\brecipes?\b(?:\s+(?:for|to get|to make))?\s+(.+)$", "recipe_find", "query"),
    (r"^how (?:do|can|would) i (?:get|make|create|dial in)\s+(.+)$", "recipe_find", "query"),
    (r"\bsounds?\s+like\s+(.+)$", "recipe_find", "query"),
    (r"^(?:what is|what's|what are|explain|tell me about)\s+(?:the\s+)?(.+)$", "device_ref", "name"),
    # -- templates (must outrank generic load/open/find) --
    (r"^(?:show |list |my )?templates$", "template_list", None),
    (r"^(?:new|start)(?:\s+a)?\s+session\s+(?:from|with|for)\s+(.+)$", "template_start", "query"),
    (r"^(?:new|start)(?:\s+a)?\s+session$", "template_start", None),
    (r"^(?:use|load|open)\s+(?:the\s+)?template\s+(.+)$", "template_start", "query"),
    (r"^(?:save|make)\s+(?:this\s+)?(?:as\s+)?(?:a\s+)?template$", "template_howto", None),
    # -- search / load --
    (r"\bfind (something|sounds?) like (this|that|the last one|it)\b", "find_like_last", None),
    (r"^(?:find|search(?: for)?|show me|give me|i (?:want|need))\s+(.+)$", "find", "query"),
    (r"^(?:load|open|use)\s+(?:number\s+)?(\w+)$", "load_result", "which"),
    (r"^(?:load|open|pull up)\s+(.+)$", "find_and_load", "query"),
    (r"\b(more|other) (results|options)\b|^more$", "more_results", None),
    # -- housekeeping --
    (r"\b(rebuild|refresh|update)\b.*\b(index|library)\b", "reindex", None),
    (r"^(help|what can (i|you) (say|do))\b", "help", None),
    (r"^(quit|exit|shut ?down)\b", "quit", None),
]


# Canonical command phrases for the fuzzy rescue pass. Only consulted when
# the regex outcome would be a generic "find" — so a strong regex match can
# never be overridden, and sound descriptions stay searches.
FUZZY_PHRASES = [
    ("find something like this", "find_like_last"),
    ("find something like that", "find_like_last"),
    ("walk me through it", "walkthrough"),
    ("rebuild the index", "reindex"),
    ("more results", "more_results"),
]
FUZZY_THRESHOLD = 85


def _fuzzy_rescue(text: str):
    best_cmd, best_score = None, 0.0
    for phrase, command in FUZZY_PHRASES:
        sc = fuzz.ratio(text, phrase)
        if sc > best_score:
            best_cmd, best_score = command, sc
    return Intent(best_cmd) if best_score >= FUZZY_THRESHOLD else None


def parse(text: str) -> Intent:
    text = text.strip().lower().rstrip(".!?,")
    if not text:
        return Intent("noop")
    for pattern, command, arg_name in PATTERNS:
        m = re.search(pattern, text)
        if not m:
            continue
        if command == "load_result":
            token = m.group(1)
            if token in NUM_WORDS:
                return Intent("load_result", {"which": NUM_WORDS[token]})
            # "load massive bass" fell through — treat as search+load
            m2 = re.match(r"^(?:load|open|use)\s+(.+)$", text)
            return Intent("find_and_load", {"query": m2.group(1)})
        if command == "preview_result":
            token = m.group(1)
            if token in NUM_WORDS:
                return Intent("preview_result", {"which": NUM_WORDS[token]})
            continue  # "hear a fat bass" etc. — let later patterns handle it
        if command in ("crate_add", "crate_remove"):
            token = m.group(1)
            if token in NUM_WORDS:
                return Intent(command, {"which": NUM_WORDS[token],
                                        "crate": "favorites"})
            continue
        if command == "crate_add_to":
            token = m.group(1)
            if token in NUM_WORDS:
                return Intent("crate_add", {"which": NUM_WORDS[token],
                                            "crate": m.group(2).strip()})
            continue
        if command == "crate_open" and arg_name is None:
            return Intent("crate_open", {"name": "favorites"})
        args = {}
        if arg_name and m.groups():
            args[arg_name] = m.group(m.lastindex).strip()
        if command == "loop":
            args["state"] = "on" if "on" in text else ("off" if "off" in text else "toggle")
        if command == "find":
            rescue = _fuzzy_rescue(text)
            if rescue:
                return rescue
        return Intent(command, args)
    # Nothing matched: fuzzy-rescue a mangled command phrase, else hand the
    # phrase to the dial -- "give it more punch" is a knob move, not a patch
    # search. (Owner decision 2026-09-10: his patches are sealed inside
    # ReFills, so a fallback search found nothing useful anyway. Explicit
    # searches still match the `find` patterns above.)
    return _fuzzy_rescue(text) or Intent("dial", {"phrase": text})
