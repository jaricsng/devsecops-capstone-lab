# OpenTelemetry wiring

A copy-paste-able OTel setup so [Module 02](../../modules/02-build-app.md)'s
`doctor.py` OTel check passes and [Module 04](../../modules/04-observability.md)'s
dashboards light up.

It mirrors the kit's reference: `<kit>/examples/minimal-service/telemetry.py`
(read it alongside this). The pattern, in any language:

1. Read config from env (`OTEL_SERVICE_NAME`, `OTLP_ENDPOINT` /
   `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_ENABLED`).
2. Set up a **tracer provider** with an OTLP exporter → Jaeger (`:4317`).
3. Set up a **metrics** exporter → Prometheus (`/metrics` scrape endpoint).
4. Auto-instrument the web framework, then call the setup once at app startup.

> **Code template:** `telemetry.py` (FastAPI/Python) is added in the lab's asset
> phase. Until then, copy `<kit>/examples/minimal-service/telemetry.py` directly
> — it is the canonical shape and already works with the observability overlay.

`.env` keys you'll set (from your scaffold's `.env.example`):

```
OTEL_ENABLED=true
OTEL_SERVICE_NAME=shopkit
OTLP_ENDPOINT=http://jaeger:4317   # inside docker compose; localhost:4317 outside
```

> ### Different stack?
> See `<kit>/docs/TECH-STACK-SWAP-GUIDE.md` "observability" row and
> `<kit>/dotnet/ServiceDefaults/Extensions.cs` for the .NET equivalent. The
> collector/Prometheus/Grafana side is unchanged — only SDK setup differs.
