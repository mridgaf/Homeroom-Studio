"""Command-line renderer for the Objekt clean-room prototype."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import ObjektConfig
from .randomizer import randomize_config
from .synth import ObjektSynth
from .wav import write_wav


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render the clean-room Objekt-inspired physical model")
    parser.add_argument("--preset", default="glass_bell")
    parser.add_argument("--note", type=float, default=60.0)
    parser.add_argument("--velocity", type=float, default=0.85)
    parser.add_argument("--duration", type=float, default=2.5)
    parser.add_argument("--sample-rate", type=int, default=48_000)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--randomize", type=float, default=0.0, metavar="AMOUNT")
    parser.add_argument("--output", type=Path, default=Path("artifacts/objekt-demo.wav"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = ObjektConfig.from_preset(args.preset)
    if args.randomize > 0.0:
        config = randomize_config(config, seed=args.seed, amount=args.randomize)
    synth = ObjektSynth(args.sample_rate)
    audio = synth.render_note(args.note, args.velocity, args.duration, config, seed=args.seed)
    target = write_wav(args.output, audio, args.sample_rate)
    print(f"wrote {target} ({len(audio) / args.sample_rate:.2f}s, {args.sample_rate} Hz stereo)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
