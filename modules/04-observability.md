# Module 04 — Observability

> **Goal:** make *your* app emit telemetry and watch it land — traces in Jaeger,
> metrics in Prometheus, a Grafana dashboard showing your traffic — then define
> one SLO. Exercises: `observability/*`, `operations/SLOs.md`.

In Module 00 you watched the minimal service do this. Now it's your app. The
observability stack layers on top of *your* `docker-compose.yml` as an overlay —
you don't run a separate stack, you add to the one you already have.

## Step 1 — Confirm your app exports OTel

You added the OTel dependency in Module 02. Make sure the app actually
*initializes* the SDK (see `../assets/otel-wiring/`) and points at the collector
endpoint via env var. The reference reads `OTLP_ENDPOINT` (defaulting to
`http://jaeger:4317` inside Compose). Your `.env` should set the `OTEL_*` vars
from `.env.example`.

## Step 2 — Bring up the overlay

```bash
make obs-up      # = docker compose -f docker-compose.yml -f observability/docker-compose.observability.yml --profile observability up -d
```

If `make obs-up` complains, it's telling you a precondition is missing (no
`docker-compose.yml`, or no `observability/`) — fix that first.

## Step 3 — Generate traffic and watch it flow

```bash
# exercise your real routes, not just /health
for i in $(seq 1 50); do curl -s localhost:8000/products?q=test >/dev/null; done
```

| Open | Look for |
|------|----------|
| <http://localhost:16686> | your service name in the dropdown; a trace for a real request |
| <http://localhost:9090/targets> | your app target **UP** |
| <http://localhost:3000> (`admin`/`admin`) | the Service Overview dashboard — panels should now move |

## Step 4 — Resolve the metric-name mismatch (important)

The kit ships a **known, deliberate** inconsistency, documented in
`<kit>/docs/ASSET-CATALOG.md`:

- `observability/recording_rules.yml` uses the **pre-1.23** OTel metric name
  `http_server_duration_milliseconds`.
- `observability/grafana/dashboards/starter-dashboard.json` queries the **newer**
  `http_server_request_duration_seconds`.

Picking one is an **adopter decision** — the kit refuses to silently choose for
you. Decide based on your OTel SDK version which name your app actually emits
(check `/metrics`), then make the recording rule and the dashboard agree.
**Record your decision and why** in your repo (a note in `observability/` or
`STACK-CHOICES.md`). This is a graded reasoning step, not a copy-paste.

## Step 5 — Define one SLO

Open `operations/SLOs.md` and write at least one real SLI/SLO for your service
(e.g. "99% of `/products` requests succeed and return < 300ms over 28 days"),
and connect it to a recording rule in `recording_rules.yml`. You'll build on
this in Module 08.

> Alertmanager boots as part of the overlay. If you edit `alertmanager.yml`,
> keep the receiver URLs structurally valid — it crash-loops on a malformed URL
> even if it's just a placeholder.

> ### 🤖 Claude Code track
> - *"My /metrics output shows `<paste a few lines>`. Which metric name does my
>   app emit, and should I update recording_rules.yml or the Grafana dashboard
>   to match? Explain the tradeoff."*
> - *"Draft an SLI/SLO for my `/products` endpoint in operations/SLOs.md and the
>   matching recording rule."*

> ### 🛠️ Manual track
> - Hit `/metrics` and grep for `http_server`. Edit either the dashboard JSON or
>   the recording rule so the names match what you emit.
> - Compare your `operations/SLOs.md` against
>   `../reference-solution/operations/SLOs.md`.

> ### Different stack?
> Any OTLP-emitting service works — the collector, Prometheus, and Grafana don't
> care about your language. Non-FastAPI auto-instrumentation differs; see
> `<kit>/docs/TECH-STACK-SWAP-GUIDE.md` "observability" row and
> `<kit>/dotnet/ServiceDefaults/Extensions.cs` for the .NET equivalent.

## ✅ Checkpoint

- [ ] A Grafana panel shows request traffic **from your app** (not the minimal service).
- [ ] At least one trace for a real endpoint is visible in Jaeger.
- [ ] You resolved the metric-name mismatch **and documented why**.
- [ ] `operations/SLOs.md` has one SLI/SLO tied to a recording rule.

Next: **[Module 05 — Load testing](05-load-testing.md)**.
