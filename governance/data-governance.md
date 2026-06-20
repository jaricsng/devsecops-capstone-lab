# Data Governance, Retention & Privacy

> Template. Fill `TODO`s. Owner: `TODO-DPO/eng-lead` · Review: annually + on data-model change.

## 1. Data classification

Classify every data store/field. ShopKit example:

| Data | Class | Store | Notes |
|------|-------|-------|-------|
| Email, full/display name | **PII** | `users` (Postgres) | Identifies a person |
| Password | **Secret** | `users.hashed_password` | PBKDF2 hash, never plaintext |
| Cart, orders, order items | **Confidential** (financial) | `cart_items`,`orders` | Purchase history |
| Stripe PaymentIntent id | **Confidential** | `orders.stripe_payment_intent_id` | Card data never touches us — held by Stripe (PCI scope minimized) |
| Catalog (products) | **Public** | `products` | Non-sensitive |
| Telemetry (traces/metrics) | **Internal** | Jaeger/Prometheus | Must not contain PII or secrets |

**Rule:** logs, traces, and metrics carry **no PII or secrets** (e.g. don't log
request bodies, tokens, or `log_min_duration_statement` of query contents — the
IaC sets it to `-1` for this reason).

## 2. Retention schedule

| Data | Retention | Disposal |
|------|-----------|----------|
| Account/PII | Life of account + `TODO` (e.g. 30d) after deletion | Hard-delete / crypto-erase |
| Orders (financial) | `TODO` (often 7y for tax) | Archive then purge |
| Audit logs | `TODO` (≥ 1y recommended) | Immutable store, then purge |
| App logs / telemetry | `TODO` (e.g. 30–90d) | Auto-expire |
| Backups | Cloud SQL: 7d (staging) / 30d (prod) — see IaC | Auto-expire |

## 3. Encryption

- **In transit:** TLS enforced (`ssl_mode = ENCRYPTED_ONLY` on Cloud SQL; HTTPS at the edge).
- **At rest:** GCP default encryption; for regulated data use **CMEK** (`TODO`).
- **Secrets:** Secret Manager / env, never in code (enforced by detect-secrets).

## 4. Privacy (GDPR/CCPA shape)

- **Right to erasure (Art. 17):** `DELETE /users/me` removes the account + invalidates the token. Extend to cascade-delete or anonymize related orders per legal advice (`TODO`).
- **Right of access / portability (Art. 15/20):** `TODO` — provide an export endpoint/process.
- **Lawful basis & consent:** `TODO` — record at signup.
- **Breach notification:** see [incident-and-breach-response.md](incident-and-breach-response.md) (72h to the supervisory authority under GDPR).
- **Records of processing (Art. 30):** maintain in [third-party-register.md](third-party-register.md) + this doc.
