from app.database.database import engine
from app.database.base import Base
from app.models.plan import Plan
# Import all models
from app.models.invoice import Invoice
from app.models.user import User
from app.models.subscription import Subscription
from app.models.billing_cycle import BillingCycle
from app.models.payment import Payment
from app.models.refund import Refund
from app.models.audit_log import AuditLog
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")