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

# Future Enhancements

- Payment Gateway Integration
- PDF Invoice Generation
- Tax Calculation
- Usage-Based Billing
- Retry Logic for Failed Payments
- React Admin Dashboard

---

# Author

**Harika Podakandla**

B.Tech – Computer Science Engineering

Subscription Management Backend – Internship Project