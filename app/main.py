from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.users import router as user_router
from app.api.plans import router as plan_router
from app.api.subscriptions import router as subscription_router
from app.api.billing_cycles import router as billing_router
from app.api.invoices import router as invoice_router
from app.api.payments import router as payment_router
from app.api.audit_logs import router as audit_router
from app.api.webhooks import router as webhook_router
from app.api.refunds import router as refund_router
from app.api.dashboard import router as dashboard_router


app = FastAPI(
    title="Subscription Management Backend"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(user_router)

app.include_router(plan_router)

app.include_router(subscription_router)

app.include_router(billing_router)

app.include_router(payment_router)

app.include_router(invoice_router)

app.include_router(dashboard_router)

app.include_router(audit_router)

app.include_router(webhook_router)

app.include_router(refund_router)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Subscription Management Backend API"
    }