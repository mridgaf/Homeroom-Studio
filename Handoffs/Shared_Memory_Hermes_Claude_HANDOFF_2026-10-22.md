# Handoff: Shared Memory for Hermes + Claude (2026-10-22)

---
## Part 1 of 4 — The goal

- John wants ONE memory store on his Mac that **Hermes Agent** and **Claude** (Desktop + Code) both read and write.
- Today they keep separate notes and never see each other's. That is the problem.
- Plan agreed in chat: a plain markdown folder + the **Basic Memory** MCP server, connected to both.
- Run in **Claude Code on the Mac**. Sonnet, medium effort is enough.

House rules (from CLAUDE.md, still apply): plain short words, do it yourself, don't hand John steps, never delete files, never commit/push, ask BLOCKING questions with clickable options, anything he must click goes LAST.

---
## Part 2 of 4 — What is known vs NOT verified

Known:
- Mac: M2 Pro, 16 GB, macOS 26.5.2, shell is bash.
- `uv` is installed at `~/.local/bin/uv`.
- Basic Memory stores notes as markdown and has a Claude Desktop guide:
  https://www.mintlify.com/basicmachines-co/basic-memory/guides/claude-desktop
- Hermes Agent supports MCP servers: https://fast.io/resources/how-to-connect-hermes-agent-to-mcp-storage/
- Hermes memory discussion: https://github.com/NousResearch/hermes-agent/issues/10835

NOT verified — check before acting, do not guess:
- Exact current Basic Memory install + MCP command (check its docs/README today).
- Where Hermes keeps its MCP settings on THIS Mac, for HIS version and profile (read his real files and the Hermes docs; see project memory "hermes-agent-setup" for which profile).
- Whether Claude Desktop's config file already has other MCP servers (merge, never overwrite).

---
## Part 3 of 4 — Steps

1. **Folder.** BLOCKING question to John (clickable): where the memory folder lives. Suggest `~/Homeroom Memory` on the Mac's own disk (not TBOTC 3 — it isn't always mounted).
2. **Install Basic Memory** with uv, per its current docs. Point its project at that folder.
3. **Claude Desktop.** Back up `~/Library/Application Support/Claude/claude_desktop_config.json` (copy, dated), then ADD the basic-memory server entry. John restarts Claude Desktop (his action, last).
4. **Claude Code.** Add the same server for Code (`claude mcp add ...` per current docs), user scope so every project sees it.
5. **Hermes.** Back up its config, add the same server to the profile he uses. Restart Hermes.
6. **Rules so they actually use it.**
   - Add to `~/Desktop/Homeroom Studio/CLAUDE.md`: "Before work, search shared memory (basic-memory). Save lasting decisions there."
   - Add the same rule to Hermes's profile instructions/rulebook.
7. Seed 3–5 starter notes: who John is, the project names, the house rules (short).

---
## Part 4 of 4 — Prove it works, then report

Test both directions, for real:
- Hermes saves a note "test-from-hermes" → Claude Code finds it.
- Claude Code saves "test-from-claude" → Hermes finds it.
- Open the folder and confirm both files exist as markdown.

Only call it done if all three pass. If any fails, say which one, plainly.

Report to John in under 10 lines: what works, what doesn't, then his click actions LAST (e.g. restart Claude Desktop).
Log the decision in `DECISIONS.md` (status: confirmed or open).

---
## Paste this into Claude Code
Read ~/Desktop/Homeroom Studio/Handoffs/Shared_Memory_Hermes_Claude_HANDOFF_2026-10-22.md, all 4 parts, and do it end to end. Verify anything marked NOT verified before acting.
