# Start here

This folder has a brief (`HANDOFF.md`) for Claude Code to pick up and keep building
the voice-control project — specifically, making it understand flexible spoken
requests ("give it more punch") instead of only exact pre-written phrases.

## If you don't have Claude Code installed yet

Open Terminal (Spotlight search → type "Terminal" → Enter) and paste this, then
press Enter:

```
curl -fsSL https://claude.ai/install.sh | bash
```

Follow whatever it asks you to do (usually just signing in).

**No terminal at all?** You can also open this same folder in the Claude desktop
app instead — same effect, no command line needed.

## Starting the session

1. Open Terminal.
2. Type `cd ` (with a space after it), then drag this folder into the Terminal
   window — it'll fill in the path. Press Enter.
3. Type `claude` and press Enter.
4. Paste the message below.

## What to paste

> Read HANDOFF.md. It's a brief from a planning session about adding flexible,
> open-ended voice/text command understanding to this project — so it can handle
> requests like "give it more punch" and not just exact pre-written phrases.
>
> Start with the two blocking open questions at the bottom of the brief — where the
> `device_refs`/`recipes` folders should actually live, and how the local model
> should be called. Ask me both before creating any folders or writing any code.

That's it — it'll take it from there.
