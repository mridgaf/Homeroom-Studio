# Skills to keep for building and vibe-coding (2026-10-28)

## What the usage data says
The skill-doctor run showed every gstack, firecrawl, and most superpowers and mattpocock skills at 0–1 uses in the last 80+ days. The heavy users were all Homeroom beat-work skills (audition-batch, session-ledger, beat-crew, dj-rebuild). So the general building skills are unused, not proven useless. Keep the few that cover a real gap and drop the overlaps.

## The real cost is not the list
Two SessionStart hooks inject instructions every session: superpowers ("invoke a skill if there is even a 1% chance it applies") and ponytail (lazy-dev mode). Those, not the listing, drive most of the overhead, and they are why the same job is covered by three skills.

## Overlaps (pick one of each)
| Job | Options installed | Keep |
|---|---|---|
| Plan before building | superpowers brainstorming + writing-plans; gstack office-hours, spec, plan-eng-review, plan-ceo-review, autoplan; mattpocock grill-me, grilling, grill-with-docs | superpowers brainstorming + writing-plans (already forced by its hook) |
| Test first | superpowers test-driven-development; mattpocock tdd | superpowers TDD |
| Find root cause of a bug | superpowers systematic-debugging; mattpocock diagnosing-bugs; gstack investigate | superpowers systematic-debugging |
| Check before saying "done" | superpowers verification-before-completion; gstack review, qa | verification-before-completion (already a house rule) |
| Code review before merge | gstack review; mattpocock code-review; gstack cso (security) | gstack review, and cso only for anything touching money, accounts, or keys |
| Ship a PR | gstack ship, land-and-deploy, setup-deploy; superpowers finishing-a-development-branch | Drop all. You commit and push yourself (house rule), so none fit. |
| Stop destructive commands | gstack careful, freeze, guard | guard (includes both) |
| Lean code | ponytail (on by hook); karpathy-guidelines | ponytail. Drop karpathy-guidelines (overlaps). |
| Throwaway prototype | mattpocock prototype | keep (no overlap, small) |
| UI and visual work | gstack design-consultation, design-html, design-review, design-shotgun, plan-design-review | design-consultation only, when a UI project starts |

## Keep (short list)
1. superpowers: brainstorming, writing-plans, test-driven-development, systematic-debugging, verification-before-completion
2. gstack: office-hours (new idea), review, qa (web apps, uses gstack /browse), guard, investigate only if you drop systematic-debugging
3. ponytail (lazy code)
4. mattpocock: prototype
5. Firecrawl: firecrawl-search, firecrawl-scrape, firecrawl-interact

## Drop or disable
- Redundant with the above: mattpocock grill-me, grilling, grill-with-docs, tdd, diagnosing-bugs, code-review, to-spec, to-tickets, triage, implement; gstack ship, land-and-deploy, setup-deploy, autoplan, plan-ceo-review, plan-devex-review, plan-tune, careful, freeze, karpathy-guidelines
- Not useful for your work: the other ~50 firecrawl-* skills (fantasy-sports, shop, lead-gen, job-postings, and so on), gstack benchmark, canary, retro, document-release, health, learn, devex-review, pair-agent, reverse-engineer-anything
- Whole claude-mem skill bundle (about 50): keep only what the claude-mem memory hooks need. Not checked one by one.

## Not verified
I read descriptions and file sizes, not each skill's full behavior, and I did not test any skill on a real project. Usage counts come from the skill-doctor output only.
