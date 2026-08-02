from app.core.celery_app import celery_app


@celery_app.task
def generate_invoices():
    print("Checking active subscriptions...")
    print("Generating invoices...")