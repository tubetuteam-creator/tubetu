# TUBETU AI Core — backend scaffold

This is a self-hostable, rules-based API. It makes **no external LLM calls**. It is not a trained generative model.

## Run locally / on your server
1. Install Python 3.11+.
2. `python -m venv .venv` then activate it.
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`; fill `SUPABASE_URL` and the **server-only** `SUPABASE_SERVICE_ROLE_KEY`.
5. `uvicorn main:app --host 127.0.0.1 --port 8000` (use a reverse proxy with HTTPS for production).
6. Check `/health` and `/docs`.

Never expose the service-role key to browser JavaScript or commit a real secret. Restrict `ALLOWED_ORIGINS`, add an upstream reverse-proxy rate limit/WAF, monitoring, backups and TLS before production.

## API
- `GET /health`
- `POST /ai/query` body `{"text":"Продам перфоратор за 25000 тенге в Алматы"}`
- `POST /ai/publish` requires `Authorization: Bearer <Supabase access token>`, body `{"text":"confirm","confirm_publish":true,"draft":{...}}`
- `GET /ai/store-stats` intentionally returns 501 until the actual store, billing and view-event schema is verified.

The API uses the existing `posts(title,text,category,author_id)` shape seen in the current frontend. Verify schema and RLS in a staging project before production. Publication must only be invoked from an explicit user confirmation.

## Security notes
- Server-side token validation; service key is server-only.
- Per-process rate limiting is a basic fallback, not DDoS protection. Put a gateway/WAF in front and use a shared limiter for multi-worker deployments.
- SQL injection is mitigated by Supabase/PostgREST parameterized operations, not by deleting suspicious strings from user content.
- The rules engine is not a generative model. It does not provide perfect Russian/Kazakh understanding, reliable price valuation, or a guarantee against every attack.
- Local speech-to-text is not bundled; Vosk/Whisper deployment requires model files, compute, and integration.
- Payment provider, subscription enforcement, storefront CRUD, analytics events, Kazakh translations and full integration tests remain to be configured against real project infrastructure.
