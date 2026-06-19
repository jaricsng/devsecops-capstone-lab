# Module 05 — Load testing

> **Goal:** adapt the kit's load scenarios to *your* routes, run them, and read
> the results against the telemetry you wired in Module 04. Exercises:
> `load-testing/k6/*`, `load-testing/locust/*`.

A load test is only useful if it exercises your real user journeys and declares
explicit pass/fail thresholds. The kit ships three k6 scenarios (smoke, load,
spike) and a Locust equivalent — but their endpoints are from the original
reference app (`/auth/register`, `/projects`, …), so you must point them at
*your* API.

## Step 1 — Read the shipped scenario

```bash
cat load-testing/k6/smoke.js
```

Notice the pieces you'll reuse: `BASE_URL` parameterization (`__ENV.BASE_URL`),
a `setup()` that registers + logs in to get a token, a token-passed default
function, and **named thresholds** in `export const options`.

## Step 2 — Adapt it to your journeys

Replace the endpoint calls with your domain's. For the e-commerce reference, a
realistic smoke journey is: register → login → `GET /products?q=` → `POST
/cart/items` → `GET /cart`. Keep the threshold block — that's what turns a load
test into a gate:

```js
export const options = {
  thresholds: {
    http_req_failed: ["rate<0.01"],      // <1% errors
    http_req_duration: ["p(95)<400"],     // 95th percentile under 400ms
  },
};
```

## Step 3 — Run it (with the app + observability up)

```bash
make obs-up                                   # so you can watch it in Grafana
k6 run load-testing/k6/smoke.js -e BASE_URL=http://localhost:8000
# heavier: k6 run load-testing/k6/load.js -e BASE_URL=http://localhost:8000
```

k6 prints whether each threshold passed. While it runs, watch the Grafana
dashboard and Jaeger — **correlating the load with the latency/trace data is the
point**, not just the k6 summary.

## Step 4 — Find one bottleneck

Use the traces to identify the slowest span under load (a missing DB index on
`products.name` for search is the classic one). Note it; you don't have to fix
everything, but a capstone should *observe* the system under stress and reason
about it.

> ### 🤖 Claude Code track
> - `/load-test smoke` — runs a scenario and correlates results with
>   Prometheus/Jaeger, calling out bottlenecks.
> - *"Rewrite load-testing/k6/smoke.js for my endpoints: `<list them>`, keeping
>   the threshold and token-pool patterns."*

> ### 🛠️ Manual track
> - Edit `smoke.js` by hand using your routes; diff against
>   `../reference-solution/load-testing/k6/smoke.js`.
> - Prefer Python? Adapt `load-testing/locust/locustfile.py` instead and run
>   `locust -f load-testing/locust/locustfile.py`.

> ### Different stack?
> k6/Locust hit HTTP, so they're language-agnostic — only the paths/payloads
> change. If your auth isn't bearer-token JWT, adapt the `setup()` login step
> (see `<kit>/docs/TECH-STACK-SWAP-GUIDE.md` if your auth scheme differs).

## ✅ Checkpoint

- [ ] A k6 (or Locust) scenario hits your real routes and **all declared
      thresholds pass**.
- [ ] You watched the load show up in Grafana/Jaeger.
- [ ] You noted at least one bottleneck or confirmed there isn't one.

Next: **[Module 06 — Security review & pen-test](06-security-pentest.md)**.
