# Render deployment

1. Upload the contents of this folder to the root of your GitHub repository. Keep `templates/index.html` in the templates folder.
2. Render: Python 3, branch `main`, build `pip install -r requirements.txt`, start `gunicorn main:app`, Free instance.
3. Set `SESSION_SECRET` to a securely generated random value and `ADMIN_PASSWORD` to a unique strong password in Render environment variables. Never put secrets in GitHub.
4. Check `/health`, submit a fictional enquiry, sign in through Staff access, confirm a demo booking, and check demo seat availability.
5. Render Free has ephemeral disk: SQLite records may disappear on restart/deploy. This is NOT production-grade persistence. For a real deployment use a managed database, stronger staff authentication and CSRF protection.
6. Do not claim an external AI service or n8n is integrated. The FAQ and classification are rules-based.
