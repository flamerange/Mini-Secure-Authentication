# 🔐 Mini Secure Authentication Server

A robust, enterprise-grade authentication and authorization system built with FastAPI, SQLAlchemy, and JWT security — featuring RBAC, token refresh, rate limiting, and a premium glassmorphism UI.

---

## 👥 Project Team

**Submitted by:**
| Name | Roll Number |
|---|---|
| MAYANK BAJETHA | 2401010206 |
| VISHAL TAKKAR | 2401010200 |
| SMRITI ARYA | 2401010302 |
| AMAN JAKHAR | 2401010261 |
| KRISH JANGRA | 2401010227 |
| SATVIK CHAUHAN | 2401010026 |

**Faculty Mentor:** MS. JYOTI KAURAV

---

## 🚀 All Implemented Features

- **Secure Registration** — Form-based user/admin provisioning.
- **JWT Authentication** — Secure login generating Access and Refresh Tokens.
- **Token Refresh System** — Obtain new access tokens without re-logging in.
- **Logout with Blacklisting** — Invalidates the JWT server-side securely.
- **Role-Based Access Control (RBAC)** — Strict separation between Standard Users and System Administrators.
- **Admin User Registry** — Admin-only API and UI to list all connected network operators.
- **Rate Limiting** — 5 requests/minute on sensitive routes like `/login` and `/register`.
- **Security Middleware** — CORS + TrustedHost integration.
- **Automated API Documentation** — Interactive Swagger UI available at `/docs`.
- **Premium User Interface** — Glassmorphism-inspired design crafted with Tailwind CSS and Jinja2 templates.

---

## 💻 How to Run Locally

### 1. Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the project root:
```env
JWT_SECRET_KEY=superSecretKeyForMiniAuthServer2026_RishavProject_1234567890
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Launch Server
```bash
uvicorn main:app --reload
```
Navigate to:
- **Application**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Reference**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🌐 How to Deploy on Render.com

This project is prepared for easy deployment on Render.
Please see the `DEPLOYMENT.md` file for exact step-by-step guidance.

**Live Render URL:** *(Add the live url once deployed)*

---
*Final Submission Draft — 2026*

