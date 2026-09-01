"""Per-DJ starting positions for the Sound Engine's channel rack.

Reads fx_presets.json (project root) and answers one question: when this
beat opens, where should THIS lane's knobs sit? Nothing here writes audio
or touches a beat file — the generator's output is untouched, exactly as
sound_engine/library.py leaves it. See fx_presets.json's _readme for the
data format and where the numbers came from.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_PRESETS_PATH = Path(__file__).resolve().parent.parent / "fx_presets.json"

# The sub is the kick's low end and the owner's mix rule leaves it alone,
# so these lanes get NO effects at all. Deliberate copy of _LOW_END in
# tools/crew.py:107 rather than an import — pulling in crew drags the whole
# beat-generation stack into this lightweight server, the same reason
# library.py copies the beats-root lookup. Keep the two in sync.
# "bass drum" is the owner's name for the long 808/sub boom (his exact
# distinction, tools/beat_recipes.py:126) and is the thing that must stay
# dry. It is in this list because that is what the FILE is actually called
# — LANE_LABELS renames the lane on its way to disk, so a guard that only
# knew the raw lane keys never fired on a real beat.
_LOW_END = {"sub", "bass", "sub808", "808", "bass drum"}

# Stems are named with the owner-facing label, not the internal lane key
# (tools/beat_recipes.py:134 LANE_LABELS). Mapped back here so a preset can
# keep saying "kick". Copied rather than imported for the reason given at
# the top of this file; keep in sync with that dict.
_LABEL_TO_LANE = {"kick drum": "kick"}

# Trailing lane numbering, in the two shapes that occur on disk:
#   chord0, bass1        -> the numbered family
#   chord0v1, chord1v1   -> a second voicing of that family member
#                           ("brass stack (lead)" beside "strings (support)")
_LANE_SUFFIX = re.compile(r"(?:\d+v\d+|\d+)$")

# Note-valued params and the knob they feed once a tempo is known.
_NOTE_PARAMS = {"dly_note": "dly_time_s", "br_note": "br_cell_s"}


_CACHE = {"mtime": None, "data": {}}


def _valid(raw):
    """Keep only the entries that are shaped like presets.

    _load() used to catch OSError/JSONDecodeError only, so a file that was
    valid JSON but the wrong SHAPE ({"Otto Grit": "grit"}, or a top-level
    array) sailed through and raised inside for_lane — which runs OUTSIDE
    the try in server.py's from-beat, so every beat open 500'd and the FX
    deep link died silently. The docstring above promised the opposite.
    Anything malformed is now dropped rather than trusted.
    (Adversarial review, 2026-09-01.)
    """
    if not isinstance(raw, dict):
        return {}
    out = {}
    for dj, entry in raw.items():
        if dj.startswith("_") and dj != "_default":
            continue
        if not isinstance(entry, dict):
            continue
        lanes = {}
        for lane, params in entry.items():
            # "_other" is a real lane key (the catch-all), not commentary —
            # every other underscore key is prose like "_notes"
            if (lane.startswith("_") and lane != "_other") \
                    or not isinstance(params, dict):
                continue
            # every value must be a real number — a string here would
            # reach _finite_float and take the whole lane down with it
            if all(isinstance(v, (int, float)) and not isinstance(v, bool)
                   for v in params.values()):
                lanes[lane] = params
        if lanes:
            out[dj] = lanes
    return out


def _load():
    """Cached on the file's mtime — this is called once per stem, so a
    beat with 14 channels re-read and re-parsed the file 14 times. Editing
    fx_presets.json still takes effect without a restart."""
    try:
        mtime = _PRESETS_PATH.stat().st_mtime
    except OSError:
        return {}
    if _CACHE["mtime"] != mtime:
        try:
            with open(_PRESETS_PATH) as f:
                _CACHE["data"] = _valid(json.load(f))
        except (OSError, json.JSONDecodeError, ValueError):
            # A missing or broken preset file must not stop a beat from
            # opening — it just means every knob starts where it always did.
            _CACHE["data"] = {}
        _CACHE["mtime"] = mtime
    return _CACHE["data"]


def lane_role(lane_id):
    """'chord0 - piano stack + sample_ ...' -> 'chord'.

    Stems are named '<owner-facing label> - <sample name>', and the
    numbered families (bass0/1/2, chord0/1/2) are one role wearing three
    hats. An uploaded file with no ' - ' at all just uses its whole name,
    which simply won't match a preset — that is the intended no-op.

    bass0/1/2 is the melodic bass LINE, not the 808 (that stem is called
    'bass drum'). It is still treated as low end and left alone, which is
    the conservative reading of "leave the sub dry" and matches what those
    lanes do today.
    """
    head = lane_id.split(" - ", 1)[0].strip().lower()
    head = _LABEL_TO_LANE.get(head, head)
    # `or head`: a lane that is ALL digits ("808") would otherwise strip to
    # an empty string and slip straight past the low-end guard below.
    # .strip() again: the sub runs AFTER the first strip, so "sub 2" would
    # leave "sub " and miss _LOW_END by one space. No such stem exists in
    # the 6,779 on the drive today; this makes it unable to appear.
    return _LANE_SUFFIX.sub("", head).strip() or head


def resolve_dj(dj, beat_name=None):
    """Which tuned personality this beat belongs to.

    The Sound Engine names a beat by its FOLDER, but a favourited beat
    lives in "Favorites/" and a style beat in "Memphis/" — so the folder
    is often not a DJ at all and those beats silently got the generic
    default. 60 beats sit in Favorites today, the folder he opens most.
    The DJ is right there in the filename ("1009 J Dillo Wonky Naptime"),
    so fall back to finding a known name inside it. Longest match wins, so
    a name that contains another cannot be shadowed.
    (Adversarial review, 2026-09-01.)
    """
    presets = _load()
    if dj in presets:
        return dj
    if beat_name:
        hits = [k for k in presets
                if not k.startswith("_") and k.lower() in beat_name.lower()]
        if hits:
            return max(hits, key=len)
    return dj


def for_lane(dj, lane_id, bpm=None, beat_name=None):
    """The knob positions this lane should open at. {} means 'leave it'.

    Falls through to _default when the DJ has no entry yet, so an
    un-auditioned DJ sounds the way it does today rather than borrowing
    someone else's character.
    """
    role = lane_role(lane_id)
    if role in _LOW_END:
        return {}
    presets = _load()
    dj = resolve_dj(dj, beat_name)
    default = presets.get("_default") or {}
    entry = presets.get(dj)
    if entry is None:
        entry = default
    # A tuned DJ with no line for THIS lane still falls back to the gentle
    # default for it. Without this, a beat carrying a lane its DJ was never
    # tuned for (Night Metro has no snare entry, and plenty of its beats
    # have a snare) left that one channel bone dry beside processed ones —
    # which reads as a broken preset, not as a choice.
    # ..._other is the last resort: 66 of 119 beats by the tuned four carry
    # a lane nobody listed (reversefx, woods, vox, blips, claves, timbales,
    # sirens...), and those came back untouched beside processed ones —
    # the same "reads as broken, not as a choice" problem the per-lane
    # fallback was added for, one level up. (Adversarial review.)
    params = dict(entry.get(role) or default.get(role)
                  or default.get("_other") or {})
    if not params:
        return {}

    # note values -> seconds against this beat's own tempo. Without a
    # tempo there is nothing to convert against, so the timed effects are
    # dropped rather than guessed onto a default bpm.
    # The note value is KEPT alongside the seconds it resolves to: the
    # server reads the seconds (_apply_channel_chain ignores keys it does
    # not know), while the browser reads the note so its Time/Grid control
    # can say "dotted 1/8" instead of "511 ms".
    # An absurd tempo produces an out-of-range delay time, and one
    # rejected param used to discard the WHOLE lane's preset — its
    # saturation and EQ with it. _BPM_RE will happily read "9999bpm" out
    # of a filename, so the guard belongs here. (Adversarial review.)
    try:
        bpm = float(bpm) if bpm else None
    except (TypeError, ValueError):
        bpm = None
    if bpm is not None and not (20.0 <= bpm <= 300.0):
        bpm = None

    for note_key, secs_key in _NOTE_PARAMS.items():
        note = params.get(note_key)
        if note is None:
            continue
        if bpm:
            params[secs_key] = float(note) * (60.0 / float(bpm))
        else:
            params.pop(note_key, None)
            params.pop(secs_key, None)
    if not bpm:
        # a delay/stutter with no time is meaningless — turn them off
        # rather than let a mix knob sit up over a nonsense default
        params.pop("dly_mix", None)
        params.pop("br_mix", None)
    return {k: v for k, v in params.items() if not k.startswith("_")}
