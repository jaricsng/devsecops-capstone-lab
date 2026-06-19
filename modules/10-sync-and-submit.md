# Module 10 — Stay in sync & submit

> **Goal:** learn how to pull kit improvements into your repo after you
> scaffolded, then assemble your capstone submission. Exercises:
> `tools/sync_check.py`, the [RUBRIC](../RUBRIC.md).

You scaffolded from the kit at a point in time (`PLATFORM-KIT.md` records the
commit). The kit keeps evolving — bug fixes, new capabilities. `sync_check.py`
tells you what changed upstream without clobbering your local edits.

## Step 1 — Run the drift check

```bash
python3 <kit>/tools/sync_check.py . --kit-path <kit> --show-diffs
# or: make sync KIT_PATH=<kit>
```

It classifies every file the scaffold copied:

| Status | Meaning |
|--------|---------|
| ✅ unchanged | local = as-scaffolded = current kit |
| ✏️ locally modified | you edited it (expected for most app files) |
| 🆕 upstream changed | the kit updated it since you scaffolded |
| ⚠️ both changed | you *and* the kit changed it — review before merging |
| ➕ new upstream file | kit added a file you don't have |
| 🗑️ removed upstream | kit deleted it |

Capture the output. You don't have to adopt every upstream change — the skill is
*knowing* what drifted and deciding deliberately.

## Step 2 — Assemble your submission

Your capstone deliverable is your **repo** plus a short **completion report**.
Create `CAPSTONE-REPORT.md` with:

1. **Your app** — what you built, the stack, the endpoints.
2. **Checkpoint evidence** — for each [RUBRIC](../RUBRIC.md) row, the command you
   ran and its result (paste `doctor.py` output, a CI run link, a Grafana
   screenshot, the k6 summary, `conftest`/`check_migrations.py` exit codes).
3. **`STACK-CHOICES.md`** — your stack + the one swap you evaluated (cite the
   kit's `TECH-STACK-SWAP-GUIDE.md` section).
4. **`SECURITY-FINDINGS.md`** — from Module 06.
5. **The metric-name decision** from Module 04 and your SLO from Module 08.
6. **Reflection** — which capability surprised you, and what you'd add next.
7. Teams also include the working agreement + evidence of T1–T4.

## Step 3 — Self-grade against the rubric

Walk [RUBRIC.md](../RUBRIC.md) row by row. Every **Core** row must pass. If one
doesn't, that's your next task — go back to the module it points at. A row you
*can't* make pass because the kit itself is broken is a finding worth reporting
(see [KIT-VERIFICATION.md](../KIT-VERIFICATION.md)).

> ### 🤖 Claude Code track
> - *"Run sync_check against the kit and summarize what drifted and what I
>   should adopt vs ignore."*
> - *"Draft CAPSTONE-REPORT.md from my repo: map each RUBRIC.md row to the
>   evidence in this repo and flag any row I haven't satisfied."*

> ### 🛠️ Manual track
> - Run `make sync KIT_PATH=<kit>` and paste the summary into your report.
> - Fill `CAPSTONE-REPORT.md` by hand against the rubric checklist.

> ### Different stack?
> `sync_check.py` works regardless of your app stack — it only tracks files the
> kit manages. Heavily swapped repos will show more ✏️ locally-modified entries;
> that's expected.

## ✅ Checkpoint

- [ ] `sync_check.py` output captured in your report.
- [ ] `CAPSTONE-REPORT.md` maps every Core rubric row to evidence.
- [ ] Every **Core** rubric row passes (teams: + T1–T4).

🎉 **That's the capstone.** You took an app from empty repo to scaffolded,
secured, observable, load-tested, policy-gated, and deploy-ready — and you can
explain why every piece is there. Compare your journey to
[`../reference-solution/`](../reference-solution/) and see where your choices
differed.
