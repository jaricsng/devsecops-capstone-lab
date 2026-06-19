"""Stripe webhook handler — signature-verified and idempotent.

The security exercise from Module 06. Two non-negotiables:

  1. VERIFY THE SIGNATURE. Never trust the body alone — anyone can POST
     "payment succeeded". stripe.Webhook.construct_event() checks the
     Stripe-Signature header against your endpoint's signing secret (whsec_...).
  2. BE IDEMPOTENT. Stripe retries delivery; process each event.id at most once.
     Here we use a unique row per processed event id.

Mount on your FastAPI app:  app.include_router(router)
Local testing:
  stripe listen --forward-to localhost:8000/webhooks/stripe
  stripe trigger payment_intent.succeeded
"""
import os

import stripe
from fastapi import APIRouter, Header, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

# Adapt these imports to your app's modules.
from app.database import get_db  # type: ignore
from app.models import Order, ProcessedWebhookEvent  # type: ignore  # see note below
from fastapi import Depends

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

# NOTE: add a tiny table to record handled events, e.g.
#   class ProcessedWebhookEvent(Base):
#       __tablename__ = "processed_webhook_events"
#       event_id: Mapped[str] = mapped_column(String(255), primary_key=True)
# A unique PK gives you idempotency for free (a duplicate insert raises).


@router.post("/stripe", status_code=status.HTTP_200_OK)
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    payload = await request.body()

    # 1) Verify signature — reject anything we can't authenticate.
    if not secret or not stripe_signature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unverified")
    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad signature")

    # 2) Idempotency — skip if we've already handled this event id.
    already = db.get(ProcessedWebhookEvent, event["id"])
    if already:
        return {"status": "duplicate-ignored"}
    db.add(ProcessedWebhookEvent(event_id=event["id"]))

    # 3) Act on the event type.
    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        order_id = intent.get("metadata", {}).get("order_id")
        if order_id:
            order = db.get(Order, int(order_id))
            if order and order.status == "pending":
                order.status = "paid"
    db.commit()
    return {"status": "ok"}
