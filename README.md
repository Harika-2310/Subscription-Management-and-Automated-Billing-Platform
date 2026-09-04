# Subscription Management Backend

## 📌 Problem Statement

SaaS businesses require a reliable billing infrastructure to manage subscription plans, automate recurring billing, handle payment failures, and maintain accurate financial records.

This project is a Subscription Management Backend built using FastAPI and PostgreSQL. It provides REST APIs for user authentication, subscription lifecycle management, billing automation, and plan management.

---

# 🚀 Features

## Authentication
- User Registration
- User Login
- JWT Authentication
- Protected APIs

## Plan Management
- Create Plan
- Update Plan
- Archive/Delete Plan
- List Plans
- Monthly & Annual Billing
- Trial Period Configuration
- Feature Management

## Subscription Management
- Create Subscription
- Trial Subscription
- Subscription State Machine
- Change Plan
- Pause Subscription
- Resume Subscription
- Cancel Subscription
- End-of-Cycle Cancellation

## Billing
- Billing Cycle Management
- Invoice Generation
- Payment Records
- Audit Logs

## Background Processing
- Redis
- Celery Worker
- Celery Beat Scheduler
- Automatic Invoice Generation

---

# 🛠 Tech Stack

- Python 3.10
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Celery
- Redis
- ReportLab
- Uvicorn

---

# 📂 Project Structure

```
SMABP/
│
├── app/
│   ├── api/
│   ├── auth/
│   ├── core/
│   ├── crud/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   ├── utils/
│   ├── workers/
│   ├── config.py
│   ├── dependencies.py
│   └── main.py
│
├── tests/
├── logs/
├── uploads/
├── create_tables.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🗄 Database Tables

- users
- plans
- subscriptions
- billing_cycles
- invoices
- payments
- audit_logs

---

# 🔄 Subscription Lifecycle

```
Trial
   │
   ▼
Active
   │
   ▼
Past Due
   │
   ▼
Cancelled
```

Also supports:

```
Trial → Cancelled
```

---

# 📌 REST APIs

## User APIs

| Method | Endpoint | Description |
|----------|----------------|----------------|
| POST | /users/register | Register User |
| POST | /users/login | Login |
| GET | /users/me | Current User |

---

## Plan APIs

| Method | Endpoint | Description |
|----------|----------------|----------------|
| GET | /plans | List Plans |
| POST | /plans | Create Plan |
| PUT | /plans/{id} | Update Plan |
| DELETE | /plans/{id} | Archive/Delete Plan |

---

## Subscription APIs

| Method | Endpoint | Description |
|----------|-----------------------------|----------------|
| POST | /subscriptions | Create Subscription |
| PUT | /subscriptions/{id}/status | Update Status |
| PUT | /subscriptions/{id}/change-plan | Change Plan |
| PUT | /subscriptions/{id}/pause | Pause |
| PUT | /subscriptions/{id}/resume | Resume |
| PUT | /subscriptions/{id}/cancel | Cancel |

---

# ⚙ Installation

## Clone Repository

```bash
git clone <repository-url>
cd subscription-management-backend
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Run FastAPI

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# ▶ Run Celery Worker

```bash
celery -A app.core.celery_app worker --loglevel=info
```

---

# ▶ Run Celery Beat

```bash
celery -A app.core.celery_app beat --loglevel=info
```

---

# ✅ Week 1–2 Milestone Completed

✔ PostgreSQL Database Schema

✔ User Authentication

✔ Plan Management APIs

✔ Subscription Management APIs

✔ Subscription State Machine

✔ Pause / Resume / Cancel Subscription

✔ Change Subscription Plan

✔ Billing Cycle Engine

✔ Celery Beat Scheduler

✔ Invoice Generation Task

✔ Swagger API Documentation

---

## Weeks 3–4 Completed

- Proration calculation
- Invoice generation
- Tax calculation
- Mock payment gateway
- Payment webhook handling
- Refund processing

  ## Week 5–6: Billing & Payment Automation

- Implemented invoice generation with tax and usage charges.
- Added tax calculation and tax reporting.
- Added invoice PDF generation using ReportLab.
- Implemented payment processing and failed payment handling.
- Added payment retry mechanism with a maximum of 3 retries.
- Added retry scheduling and subscription cancellation after failed retries.
- Developed React-based billing dashboard.
- Added MRR, churn rate, trial conversion, and failed payment metrics.
- Integrated React frontend with FastAPI backend.
- Tested invoice, payment, retry, tax, PDF, and dashboard features successfully.
  ## Weeks 7–8: System Integration, Testing & Project Finalization

- Conducted end-to-end integration testing across subscription, billing, invoice, payment, retry,      tax, PDF, and dashboard modules.
- Performed load testing using Locust with 10 concurrent users.
- Processed 162 requests with **0 failures**, an average response time of **16.65 ms**, and average    throughput of **5.3 requests/second**.
- Improved React frontend loading and error handling.
- Added responsive design for desktop, tablet, and mobile devices.
- Verified dashboard, tax report, failed payments, and invoice PDF functionality.
- Prepared system architecture, data flow, API, database, and deployment documentation.
- Finalized the project implementation and prepared the project for mentor review and submission.

## Future Enhancements

- Integration with a real payment gateway such as Stripe or Razorpay
- Advanced PDF invoice generation and customization
- Automated tax calculation based on location and applicable tax rules
- Advanced usage-based billing and metered charges
- Automatic retry and dunning logic for failed payments
- React-based admin dashboard
- Email/SMS notifications for payment and subscription events
- Advanced billing analytics and reporting
---

# Author

**Harika Podakandla**

B.Tech – Computer Science Engineering

Subscription Management and Automated Billing Platform  – Internship Project
