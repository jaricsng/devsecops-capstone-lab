# Stripe webhook handler (security exercise)

Confirming a payment via a **webhook** — not just the client-side redirect — is
how you avoid trusting the browser. It's also a classic source of critical
vulnerabilities, which makes it a great target for
[Module 06](../../modules/06-security-pentest.md).

Two properties the handler **must** have:

1. **Signature verification** — verify the `Stripe-Signature` header with your
   endpoint's signing secret (`whsec_...`). An endpoint that mutates orders
   without verifying the signature lets anyone forge "payment succeeded".
2. **Idempotency** — Stripe retries events; process each `event.id` at most once
   (store processed IDs / use a unique constraint) so a retry doesn't double-fulfil.

## Local testing

```bash
stripe listen --forward-to localhost:8000/webhooks/stripe
# copy the printed whsec_... into your .env as STRIPE_WEBHOOK_SECRET
stripe trigger payment_intent.succeeded
```

> **Code template:** a FastAPI handler (`handler.py`) is added in the lab's asset
> phase. The security review is the point — whichever way you implement it,
> verify the signature and make it idempotent, then record the review in
> `SECURITY-FINDINGS.md`.

This is a **Stretch / guided exercise** (see [RUBRIC.md](../../RUBRIC.md)), not
required for a core pass — but if you handle payments, your security review
should cover it.
