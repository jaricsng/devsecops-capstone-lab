# Module 00 — Orientation: see the kit work first

> **Goal:** prove your environment works and *see* the end state — a
> containerized service emitting traces and metrics into a running
> observability stack — before you build anything. Exercises:
> `examples/minimal-service/` + `observability/`.

Don't adopt a platform on faith. The kit ships a throwaway service whose only
job is to prove the extracted pieces still fit together. You'll boot it, watch
telemetry flow, and tear it down. That picture is what *your* app will look like
by Module 04.

## Step 1 — Boot the reference stack

From the **root of your kit clone** (`<kit>`). The `--project-directory .` is
required — Compose resolves the two files' relative paths against it.

```bash
cd <kit>
docker compose --project-directory . \
  -f examples/minimal-service/docker-compose.yml \
  -f observability/docker-compose.observability.yml \
  --profile observability up --build -d
```

## Step 2 — Confirm it's alive

```bash
curl -sf http://localhost:8000/health   # {"status":"ok"}
curl -sf http://localhost:8000/ready    # {"status":"ready"}
curl -sL  http://localhost:8000/metrics | head   # Prometheus text format
```

Generate a little traffic so there's something to look at:

```bash
for i in $(seq 1 30); do curl -s localhost:8000/health >/dev/null; done
```

## Step 3 — Look at the three windows of observability

| Open | What you should see |
|------|---------------------|
| <http://localhost:16686> (Jaeger) | Pick service **`minimal-service`** → traces for `health-check` / `readiness-check` spans |
| <http://localhost:9090/targets> (Prometheus) | scrape targets **UP** |
| <http://localhost:3000> (Grafana, `admin`/`admin`) | the provisioned **Service Overview** dashboard with request-rate / latency panels |

Spend five minutes clicking around. This is the payoff you're wiring up for your
own service later.

## Step 4 — Tear down

```bash
docker compose --project-directory . \
  -f examples/minimal-service/docker-compose.yml \
  -f observability/docker-compose.observability.yml \
  --profile observability down -v
```

## Step 5 — Decide what you're building

The reference solution is *ShopKit* (e-commerce). **You build whatever you
want**, as long as it's a containerized HTTP service. Good capstone candidates:
a task tracker, a URL shortener with analytics, a notes API with sharing, a
bookmarking service. Write a one-paragraph description and a rough endpoint list
into a new `STACK-CHOICES.md` in the repo you'll create next module — you'll
flesh it out as you go.

> ### 🤖 Claude Code track
> Open Claude Code in your kit clone and ask:
> *"Read README.md and docs/ARCHITECTURE-FIT.md. I want to build `<your idea>`.
> Is it a good fit for this kit, and what shape should it take (endpoints, data
> model, deploy target)?"* Capture the answer in `STACK-CHOICES.md`.

> ### 🛠️ Manual track
> Read `<kit>/README.md` (capability map) and `<kit>/docs/ARCHITECTURE-FIT.md`
> (what fits / what doesn't). If your idea isn't a containerized HTTP service
> with a relational DB, note which rows of ARCHITECTURE-FIT you'll be fighting.

> ### Different stack?
> The minimal service is Python/FastAPI, but the *shape* (a `/health` + `/ready`
> + `/metrics` container emitting OTLP) is language-agnostic. See
> `<kit>/dotnet/ServiceDefaults/Extensions.cs` for the same shape in C#, and
> `<kit>/docs/TECH-STACK-SWAP-GUIDE.md` for other languages.

## ✅ Checkpoint

- [ ] The Compose stack booted and `/health` returned `{"status":"ok"}`.
- [ ] You saw a trace in Jaeger and a non-empty panel in Grafana.
- [ ] You tore the stack down (`down -v`).
- [ ] You wrote a one-paragraph app idea + endpoint sketch into `STACK-CHOICES.md`.

Next: **[Module 01 — Scaffold your repo](01-scaffold.md)**.
