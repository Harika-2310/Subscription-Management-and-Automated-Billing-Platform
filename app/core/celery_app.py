from celery import Celery

celery_app = Celery(
    "subscription_backend",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.tasks.billing_tasks"]
)

celery_app.conf.timezone = "Asia/Kolkata"

celery_app.conf.beat_schedule = {
    "generate-invoices-every-day": {
        "task": "app.tasks.billing_tasks.generate_invoices",
        "schedule": 86400.0,
    }
}