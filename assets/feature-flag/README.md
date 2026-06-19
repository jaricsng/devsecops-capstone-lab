# Feature flag (decouple deploy from release)

[Module 08](../../modules/08-day2-ops.md) uses a feature flag to separate
*deployed* (the code is live) from *released* (users can reach the feature). The
payoff: turning a feature off is instant and needs no redeploy — your fastest
"undo".

The reference gates **checkout** behind a flag, so the team can deploy the
checkout code dark, enable it for internal users, ramp to 10%, then 100% — and
kill it in one toggle if the SLO burns.

## Pattern (vendor-neutral, via OpenFeature)

```
1. Define a boolean flag, e.g. `checkout_enabled`, default OFF (safe default).
2. At the decision point, evaluate the flag for the current context (user id).
3. If off, return a "coming soon" / 503-style response instead of charging.
4. Flip the flag in your provider/config — no deploy, no restart.
```

> **Code template:** an OpenFeature-based snippet (`flagged_checkout.py`) is
> added in the lab's asset phase. For local use, the kit's
> `<kit>/docs/FEATURE-FLAGS.md` shows an env-var/file provider that needs no
> external service.

> ### Different stack?
> OpenFeature has SDKs for most languages; only the evaluation call changes. See
> `<kit>/docs/FEATURE-FLAGS.md` for providers (env/file for local, LaunchDarkly/
> flagd/etc. for hosted).

A documented rollout + kill plan makes this a **Stretch** distinction item in
[RUBRIC.md](../../RUBRIC.md).
