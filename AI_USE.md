# AI use and verification note

Tool: ChatGPT (GPT-6), used to help draft architecture, Flask application, tests, workflow JSON, audit, and presentation. Example instructions: "Build a synthetic-data-only Cairns tour enquiry MVP", "Avoid external credentials and default to human review for sensitive requests", "Prevent tour capacity overbooking with a transaction", "Write basic access control and tests".

Human review required before submission: run and inspect tests, review input validation and concurrency, verify n8n import in your own test instance, check business assumptions, and personally explain the code and decisions. No claim is made that a live AI model is running: current classification is transparent keyword logic. No real customer communication is sent.

AI limitations observed or anticipated: generated workflow compatibility may vary by n8n version; keyword triage misses nuance; Flask session auth lacks production controls; generated copy can overstate fictional tour facts. Mitigations: safe defaults, explicit manual approval, no invented pickup schedules or prices, synthetic-only data, and scope disclosure.
