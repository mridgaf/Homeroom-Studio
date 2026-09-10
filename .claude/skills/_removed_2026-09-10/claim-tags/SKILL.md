---
name: claim-tags
description: Tags substantive claims with their provenance — verified by running/checking, recalled from training data (possibly stale), or inferred/guessed — so confidence is legible instead of uniform. Use this whenever producing technical output (code review, debugging, research summaries, factual writeups) where the difference between "I checked this" and "I think this" matters and would otherwise be invisible on the page. Do NOT use for casual conversation, creative writing, or opinions clearly framed as opinion — this is for claims that read as fact.
---

# Claim Tags

The problem: a guess and a verified fact can read identically in prose.
Fluency isn't evidence of accuracy. This skill makes the difference visible
instead of leaving it implicit.

## The three tags

- **`[verified]`** — checked directly in this session: ran the code, read the
  file, executed the test, fetched the source. Not "should be right" —
  actually confirmed.
- **`[recalled]`** — stated from training data / general knowledge, not
  checked this session. Could be outdated, could be slightly wrong, wasn't
  re-verified. This is the default state for most factual claims and isn't a
  bad thing — just an honest one.
- **`[inferred]`** — a guess, extrapolation, or judgment call with no direct
  source. Pattern-completion, best-available reasoning, not a lookup.

## When to tag

Tag claims that would otherwise be presented as flat fact and where being
wrong has a cost — technical claims, numbers, statuses, "this is how X
works," "this API does Y." Don't tag every sentence; that's noise. Skip
tagging for:
- things already hedged in plain language ("I think," "probably")
- creative or subjective content
- claims already covered by a citation (citations are a stronger version of
  `[verified]` — don't double up)

## How to tag

Inline, brief, at the point of the claim — not a disclaimer paragraph at the
end that vaguely covers everything:

> The config file loads from `~/.app/config.yaml` `[verified — read the file]`.
> That path convention follows the XDG spec `[recalled]`.
> Given your directory structure, I'd guess the loader checks `$HOME` before
> XDG as a fallback `[inferred]`.

## Where this is weakest — be honest about it

Self-reported confidence is not reliable evidence of correctness. Tagging
something `[recalled]` doesn't mean it's right, and `[inferred]` doesn't mean
it's more likely wrong than `[recalled]` — it only reports *how* the claim was
produced, not how accurate it turned out to be. Treat the tags as provenance
metadata, not a calibrated confidence score. For an actual accuracy check —
not just provenance — the claim needs external verification (run it, check
it against a source, or in Claude Code, run the same reasoning independently
more than once via subagents and see if the conclusions agree).

## Pairing with the ledger

If this project also has `DECISIONS.md` (see `session-ledger` skill), an
`[inferred]` or unresolved `[recalled]` claim that matters is a candidate for
a ledger entry with `status: open` — something worth checking later rather
than trusting on faith now.
