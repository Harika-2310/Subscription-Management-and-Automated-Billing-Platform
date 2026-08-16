from fastapi import FastAPI
from app.api.users import router as user_router
from app.api.plans import router as plan_router
from app.api.subscriptions import router as subscription_router
from app.api.billing_cycles import router as billing_router
from app.api.invoices import router as invoice_router
from app.api.payments import router as payment_router
from app.api.audit_logs import router as audit_router
from app.api.webhooks import router as webhook_router
from app.api.refunds import router as refund_router
app = FastAPI(title="Subscription Management Backend")

app.include_router(user_router)
app.include_router(plan_router)
app.include_router(subscription_router)
app.include_router(billing_router)
app.include_router(invoice_router)
app.include_router(payment_router)
app.include_router(audit_router)
app.include_router(webhook_router)
app.include_router(refund_router)
@app.get("/")
def root():
    return {"message": "Subscription Management Backend API"}