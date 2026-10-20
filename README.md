# Reef & Ranges — Premium Tourism MVP

A polished, mobile-responsive fictional Cairns tour website plus a working Flask operations backend, prepared for the Getup Solutions assessment.

## Features
- Editorial tourism landing page with tours, curated experiences, responsive layouts and enquiries
- Working enquiry submission and rules-based classification, including human escalation
- Safe FAQ assistant (predefined responses, no invented policies)
- Password-protected staff dashboard, enquiry list, metrics and staff booking confirmation
- Server-side capacity checks, duplicate-booking protection and demo availability lookup
- SQLite persistence for local demos; synthetic data only
- `/health` for deployment checks; automated API tests

## Run locally
`python -m pip install -r requirements.txt`
Set `SESSION_SECRET` and `ADMIN_PASSWORD` in your environment, then `python main.py`. Open http://127.0.0.1:5000. Run `pytest -q` for tests.

## Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md).

## Transparency
This is a functional **rules-based** MVP, not a live generative-AI integration. No external customer emails, payments, or real tour inventory are connected. The tour operator and all customer records are fictional. Tourism photos are externally loaded from Unsplash and may require internet access. Do not claim production readiness.

## AI-use note
AI assistance was used to draft the Flask app, UI, documentation and tests. Human review is needed for security, integration and deployment, and the applicant must personally test, explain and disclose the assistance.
