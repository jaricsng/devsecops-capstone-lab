"""Feature-flag-gated decision point (Module 08).

Demonstrates decoupling *deploy* from *release*: the checkout code can be live
(deployed) while the feature is off (not released), and you flip it without a
redeploy.

This shows the vendor-neutral OpenFeature shape with a tiny env/config provider
so it runs locally with no external service. Swap the provider for flagd /
LaunchDarkly / etc. in production — see <kit>/docs/FEATURE-FLAGS.md. The
reference solution uses the same idea via Settings.feature_checkout_enabled.
"""
import os
from dataclasses import dataclass


@dataclass
class FlagContext:
    user_id: int | None = None
    # add attributes you target on (plan, country, %-rollout bucket, ...)


class EnvFlagProvider:
    """Minimal boolean-flag provider backed by env vars. SAFE DEFAULT = off."""

    def get_boolean(self, key: str, default: bool, _ctx: FlagContext) -> bool:
        raw = os.environ.get(f"FLAG_{key.upper()}")
        if raw is None:
            return default
        return raw.strip().lower() in {"1", "true", "yes", "on"}


_provider = EnvFlagProvider()


def is_enabled(key: str, ctx: FlagContext, default: bool = False) -> bool:
    return _provider.get_boolean(key, default, ctx)


# --- Usage at the decision point -------------------------------------------
# Default OFF: if the flag system is unreachable, we fail safe (no charge).
def checkout(user_id: int) -> dict:
    ctx = FlagContext(user_id=user_id)
    if not is_enabled("checkout_enabled", ctx, default=False):
        # Don't charge; tell the client it's unavailable. Reversible in one toggle.
        return {"status": "unavailable", "reason": "feature flag off"}

    # ... real checkout (create order, PaymentIntent) ...
    return {"status": "ok"}


# Rollout plan (write yours into operations/):
#   1. Deploy with FLAG_CHECKOUT_ENABLED unset -> off for everyone (dark ship).
#   2. Enable for internal users / a 10% bucket; watch the SLO.
#   3. Ramp to 100%.  Kill switch: set the flag off — no redeploy, instant undo.
