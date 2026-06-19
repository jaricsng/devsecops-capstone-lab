# Module 08 — Day-2 ops & safe delivery

> **Goal:** prepare to *operate* the service, not just ship it — finalize SLOs,
> adapt a runbook, and decouple "deployed" from "released" with a feature flag.
> Exercises: `operations/*`, `observability/recording_rules.yml`,
> `docs/FEATURE-FLAGS.md`.

"Day 2" is everything after the first deploy: incidents, rollbacks, capacity,
and shipping changes safely. The kit gives you the scaffolding; this module
makes it real for your service.

## Step 1 — Finalize an SLO and tie it to alerting

Build on the SLI/SLO you drafted in Module 04. In `operations/SLOs.md`, state
the objective (e.g. 99.5% availability over 28 days), the error budget it
implies, and the recording rule in `recording_rules.yml` that measures it. A
good SLO is measurable from data you already emit.

## Step 2 — Adapt a runbook

`operations/runbooks/` ships templates (incident response, rollback, postmortem)
written for a generic service. Adapt **at least the rollback runbook** to your
app: what's the exact command/CI action to roll back, how do you confirm health
afterward (`/ready`!), and who/what decides. A runbook you can't follow at 3am
is theater — make it concrete.

## Step 3 — Decouple deploy from release with a feature flag

Rolling back a deploy is slow and blunt. A feature flag lets you turn a feature
*off* without redeploying. Put one user-visible feature behind a flag — the
reference gates **checkout** behind an OpenFeature flag (see
`../assets/feature-flag/` and `<kit>/docs/FEATURE-FLAGS.md`).

Demonstrate the payoff: with the app running, flip the flag and watch the
feature appear/disappear **without a redeploy**. Write a two-line "rollout plan"
in `operations/`: how you'd ramp it (off → internal → 10% → 100%) and how you'd
kill it if your SLO burns.

## Step 4 — Connect the dots

You now have the full safety story: an **SLO** tells you when you're in trouble,
a **feature flag** is your fast undo, and a **runbook** is the slow undo. Write a
short paragraph in `operations/` describing which you'd reach for in three
scenarios: a bad config value, a slow memory leak, and a corrupt deploy.

> ### 🤖 Claude Code track
> - `/compliance-check observability` (or `governance`) — scorecard across the
>   operational domains.
> - *"Adapt operations/runbooks/rollback.md to my service: my deploy is `<how>`,
>   my health check is /ready. Make every step copy-pasteable."*
> - *"Put my `<feature>` behind an OpenFeature flag per docs/FEATURE-FLAGS.md and
>   assets/feature-flag/."*

> ### 🛠️ Manual track
> - Edit `operations/SLOs.md` and the runbook by hand; diff against
>   `../reference-solution/operations/`.
> - Wire the flag using `../assets/feature-flag/` as a template; toggle it via
>   env/config and confirm no redeploy is needed.

> ### Different stack?
> OpenFeature has SDKs for most languages; the *pattern* (evaluate a flag at a
> decision point, default safely) is universal. SLOs/runbooks are
> stack-agnostic. See `<kit>/docs/FEATURE-FLAGS.md` for provider options.

## ✅ Checkpoint

- [ ] `operations/SLOs.md` has a finalized SLO tied to a recording rule + error budget.
- [ ] The rollback runbook is adapted to your service with concrete steps.
- [ ] One feature is flag-gated; you toggled it on/off **without redeploying**.
- [ ] You wrote the "which undo when" paragraph.

Next: **[Module 09 — Team track (optional)](09-team-track.md)** or, if solo,
skip to **[Module 10 — Stay in sync & submit](10-sync-and-submit.md)**.
