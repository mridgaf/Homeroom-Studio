"""The beat's KEY — root note plus mode (punch list step 1, 2026-07-19).

Until now the engine tracked one harmonic value: `root_note`, a bare
string used for exactly one thing — tuning the sine sub under the kick
(`beat_machine._root_sub`). Everything harmonic that comes next (chords,
bass, picking melodic samples that fit) has to know the MODE too, so
this is that single value grown up into a real key.

The rules are the owner's own, transcribed from `theory/`:
- rap lives in minor, dorian, or phrygian — major is the exception, not
  the default (`song-keys.md`);
- the 808 root IS the key's home note: "whatever note your 808/bass is
  playing, the ear treats as what this chord IS" (`song-keys.md`);
- roots sit low, where an 808 slaps hardest (`song-keys.md`);
- CHORDS below is a straight transcription of `chords.md`'s interval
  formulas, so voicings come from the owner's doc, not from me.

DELIBERATELY unchanged: which note a given beat picks. SUB_ROOTS keeps
the same seven names in the same order the old ROOT_HZ dict had, so
every beat already on disk still re-renders on the low note it has
always had. The mode is new information — inert until the harmony
layer reads it.
"""

# Sharps are the spelling this module thinks in; the display spelling a
# KeyContext was handed ("Bb") is kept as-is so recipes and file names
# don't churn.
SHARPS = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
_ALIAS = {"DB": "C#", "EB": "D#", "GB": "F#", "AB": "G#", "BB": "A#",
          "FB": "E", "CB": "B", "E#": "F", "B#": "C"}

# semitones from the root. song-keys.md: minor/dorian/phrygian are the
# rap modes; major is here because progressions.md spells a few loops
# (I-V-vi-IV, ii-V-I) in it.
MODES = {
    "major":    (0, 2, 4, 5, 7, 9, 11),
    "minor":    (0, 2, 3, 5, 7, 8, 10),
    "dorian":   (0, 2, 3, 5, 7, 9, 10),
    "phrygian": (0, 1, 3, 5, 7, 8, 10),
    # Added 2026-07-24 from web research at the owner's request ("collect
    # any modes that you are missing"). Sources agree the working set for
    # this music is small: "most trap melodies are based on one of these
    # 3 scales - minor, harmonic minor, and phrygian", with dorian the
    # warmer minor used in melodic/R&B-leaning hip hop.
    "harmonic_minor": (0, 2, 3, 5, 7, 8, 11),   # raised 7th; trap staple
    # 5th mode of harmonic minor = the "Hijaz"/Spanish/Freygish sound.
    # Its b2-against-major-3rd gives the augmented second the ear reads
    # instantly as Middle Eastern — documented as Timbaland's "Get Ur
    # Freak On" mode, which is why Timberline uses it.
    "phrygian_dominant": (0, 1, 4, 5, 7, 8, 10),
    # major with a b7: bluesy, unresolved, "funk uses it heavily"
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    # major with a #4: the floating/dreamy one
    "lydian": (0, 2, 4, 6, 7, 9, 11),
}

# Which major/minor family a mode belongs to. The owner's sample library
# only ever labels a file "major", "minor" or nothing (the vendors write
# "Gm"/"C", never "G dorian"), so a modal KEY could never tier-match a
# sample and melodic_loops.in_key returned ZERO picks for it — which
# silently killed the loop voice for every modal identity. Matching on
# the FAMILY fixes that without flattening the identity itself.
MODE_FAMILY = {
    "major": "major", "lydian": "major", "mixolydian": "major",
    "minor": "minor", "dorian": "minor", "phrygian": "minor",
    "harmonic_minor": "minor", "phrygian_dominant": "minor",
}


def mode_family(mode):
    """'dorian' -> 'minor'. Unknown modes fall back to minor, which is
    this music's default and the safer guess."""
    return MODE_FAMILY.get(mode, "minor")

# theory/chords.md, spelled as semitones up from the root.
CHORDS = {
    "major":    (0, 4, 7),
    "minor":    (0, 3, 7),
    "dim":      (0, 3, 6),
    "aug":      (0, 4, 8),
    "sus2":     (0, 2, 7),
    "sus4":     (0, 5, 7),
    "maj7":     (0, 4, 7, 11),
    "min7":     (0, 3, 7, 10),
    "dom7":     (0, 4, 7, 10),
    "min9":     (0, 3, 7, 10, 14),
    "maj9":     (0, 4, 7, 11, 14),
    "add9":     (0, 4, 7, 14),
    "7#9":      (0, 4, 7, 10, 15),
    # not in chords.md — but the packs are full of bare root+fifth stabs
    # and calling one a "major" chord would be a lie about the 3rd.
    "5":        (0, 7),
}

# how each quality is written after a note name / a roman numeral
SYMBOL = {"major": "", "minor": "m", "dim": "dim", "aug": "aug",
          "sus2": "sus2", "sus4": "sus4", "maj7": "maj7", "min7": "m7",
          "dom7": "7", "min9": "m9", "maj9": "maj9", "add9": "add9",
          "7#9": "7#9", "5": "5"}
FIGURE = {"major": "", "minor": "", "dim": "°", "aug": "+",
          "sus2": "sus2", "sus4": "sus4", "maj7": "maj7", "min7": "7",
          "dom7": "7", "min9": "9", "maj9": "maj9", "add9": "add9",
          "7#9": "7#9", "5": "5"}
MINORISH = ("minor", "dim", "min7", "min9")

_ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII")

# The sub's root pool, in the order the old ROOT_HZ dict listed it.
# beat_machine picks from this with a seeded Random, so the ORDER is
# load-bearing: shuffle it and every traditional beat on disk changes
# its low note. Add notes only at the end, and only on purpose.
SUB_ROOTS = ("C", "D", "E", "F", "G", "A", "Bb")
SUB_OCTAVE = 1                      # ~33-58 Hz, where song-keys.md puts it


def pitch_class(name):
    """Note name -> 0-11. Accepts flats ("Bb") and sharps ("A#")."""
    text = str(name).strip()
    up = text.upper()
    up = _ALIAS.get(up, up)
    if up not in SHARPS:
        raise ValueError("not a note name: %r" % (name,))
    return SHARPS.index(up)


class KeyContext(object):
    """What key this beat is in: a root note and a mode.

    >>> KeyContext("F", "minor").hz                 # the 808's note
    43.65352892912549
    >>> KeyContext("A", "minor").roman(0, "major")  # C major in A minor
    'III'
    """

    def __init__(self, root="F", mode="minor", octave=SUB_OCTAVE):
        self.pc = pitch_class(root)
        self.root = str(root).strip()        # keep the given spelling
        if mode not in MODES:
            raise ValueError("unknown mode %r (have %s)"
                             % (mode, ", ".join(sorted(MODES))))
        self.mode = mode
        self.octave = octave

    @classmethod
    def from_recipe(cls, rec):
        """The key of an already-rendered beat. Forgiving on purpose: a
        recipe written before this module existed has only `root_note`
        and no mode, and a half-written one shouldn't be able to crash a
        rebuild the way a raised exception here would."""
        try:
            return cls(rec.get("root_note") or "F",
                       rec.get("key_mode") or "minor")
        except (AttributeError, ValueError):
            return cls("F", "minor")

    def __repr__(self):
        return "KeyContext(%r, %r)" % (self.root, self.mode)

    def __str__(self):
        return "%s %s" % (self.root, self.mode)

    def __eq__(self, other):
        return (isinstance(other, KeyContext) and other.pc == self.pc
                and other.mode == self.mode and other.octave == self.octave)

    def __hash__(self):
        return hash((self.pc, self.mode, self.octave))

    @property
    def midi(self):
        """The root as a MIDI note number, in this key's octave."""
        return (self.octave + 1) * 12 + self.pc

    @property
    def hz(self):
        """Equal-tempered frequency of the root — what sub808 is tuned
        to. Reproduces the old ROOT_HZ table to 2 decimal places."""
        return 440.0 * 2.0 ** ((self.midi - 69) / 12.0)

    def scale(self):
        """The pitch classes in this key, tonic first."""
        return tuple((self.pc + step) % 12 for step in MODES[self.mode])

    def degree(self, pc):
        """Scale degree (1-7) of a pitch class, or None if it's outside
        the key."""
        notes = self.scale()
        pc = pc % 12
        return notes.index(pc) + 1 if pc in notes else None

    def spell(self, pc):
        return SHARPS[pc % 12]

    def chord_name(self, root_pc, quality="minor"):
        """"Am", "Cmaj7" — the name a producer would say out loud."""
        return self.spell(root_pc) + SYMBOL.get(quality, quality)

    def roman(self, root_pc, quality="minor"):
        """Roman numeral for a chord root in this key, spelled the way
        progressions.md spells them: lowercase = minor-ish, a leading b
        (or #) for a root that isn't in the key. In A minor, C major is
        'III' and Bb major is 'bII'."""
        steps = MODES[self.mode]
        rel = (root_pc - self.pc) % 12
        if rel in steps:
            num, acc = _ROMAN[steps.index(rel)], ""
        elif rel + 1 in steps:              # a step below the one above
            num, acc = _ROMAN[steps.index(rel + 1)], "b"
        else:                               # ...or above the one below
            num, acc = _ROMAN[steps.index(rel - 1)], "#"
        if quality in MINORISH:
            num = num.lower()
        return acc + num + FIGURE.get(quality, "")

    def shift_from(self, other):
        """Semitones to move music written in `other` into this key.
        Takes the SHORT way round (never more than 6), so a transposed
        loop or MIDI phrase stays in the register it was played in
        instead of leaping an octave."""
        gap = (self.pc - other.pc) % 12
        return gap - 12 if gap > 6 else gap

    def voice(self, root_pc, quality="minor", octave=3):
        """A chord's actual MIDI notes, stacked up from the root in the
        given octave — chords.md's formula turned into keys you could
        play on the Launchkey."""
        base = (octave + 1) * 12 + (root_pc % 12)
        return [base + step for step in CHORDS[quality]]

    def triad(self, degree):
        """The plain 3-note chord built on a scale degree (1-7) of this
        key, as (root pitch class, quality) — stack two more scale notes
        on top of the degree and see what came out. This is how III ends
        up major in a minor key without anyone hardcoding it."""
        notes = self.scale()
        i = (int(degree) - 1) % 7
        root = notes[i]
        third = (notes[(i + 2) % 7] - root) % 12
        fifth = (notes[(i + 4) % 7] - root) % 12
        for quality in ("major", "minor", "dim", "aug"):
            if CHORDS[quality] == (0, third, fifth):
                return root, quality
        return root, "5"                     # neither — leave the 3rd out


def name_chord(notes, bass=None):
    """Name a stack of sounding notes -> (root pitch class, quality),
    or None if it isn't a chord this vocabulary knows.

    Ties go to the reading rooted on the BASS note, because that's the
    owner's own rule from song-keys.md: the bass is the anchor, and
    "whatever note your 808/bass is playing, the ear treats as what
    this chord IS". C-E-G over an A bass is Am7, not C major.
    """
    pcs = set(int(n) % 12 for n in notes)
    if len(pcs) < 2:
        return None
    if bass is not None:
        bass = int(bass) % 12
    best = None
    for root in pcs:
        above = set((pc - root) % 12 for pc in pcs)
        for quality, form in CHORDS.items():
            want = set(step % 12 for step in form)
            if not want <= above:
                continue                     # formula isn't even in there
            # prefer: the bass as root, then the fullest formula, then
            # the fewest notes left over unexplained
            rank = (root == bass, len(want), -len(above - want))
            if best is None or rank > best[0]:
                best = (rank, root, quality)
    return (best[1], best[2]) if best else None
