# Reef & Ranges Tours — AI Digital Transformation Assessment

Fictional Cairns tour operator demonstration. All example records are synthetic. No external AI account, API key, real customer data, payment or email integration is used.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
export ADMIN_PASSWORD='replace-with-your-own-strong-demo-password'  # Windows PowerShell: $env:ADMIN_PASSWORD='...'
export SESSION_SECRET='replace-with-long-random-secret'
python app/main.py
```

Visit http://127.0.0.1:5000 . Admin uses JSON APIs: POST `/login` with `{"password":"..."}`; GET `/admin/enquiries`, POST `/admin/bookings`, GET `/admin/report`. Public POST `/api/enquiries` and GET `/api/faq?topic=weather`.

## Tests
`pytest -q`

## Scope / safety
- Rules-based enquiry classification is an **AI-ready stand-in**, not a live LLM. Unknown, sensitive and refund questions go to human review.
- Bookings are staff-confirmed only, with transactional seat capacity checks and one booking per enquiry.
- Admin session required for private data. This is a local MVP, **not production hardened**: add CSRF protection, rate limiting, TLS, persistent secret management, audit logging and data retention policy before internet deployment.
- No automated outgoing customer communications; the workflow export models a manual approval queue.
- No credentials included. Do not use ChatGPT session credentials or production accounts.
- Commit history must be created by the applicant when they initialize and commit to their own repository. Do not represent generated files as past commits.

## Workflow
Import `workflow/enquiry_triage_n8n.json` into your own n8n test instance. It uses a webhook, a Code node and a webhook response. No credentials required. The output identifies classification and whether staff review is required. The app and workflow are separate demonstrations; connecting them requires explicit authorization and a secure endpoint.

## AI use disclosure
Drafted with ChatGPT (GPT-6) for architecture, code, tests, written audit, creative assets planning and presentation. No external LLM was connected. See `docs/AI_USE.md`. Review and customize all materials before claiming personal work.
