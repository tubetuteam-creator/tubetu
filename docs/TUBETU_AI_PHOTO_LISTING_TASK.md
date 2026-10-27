# TUBETU AI: technical task — photo-to-listing without paid external AI APIs

## Goal
When a person opens **Подать**, selects one or more photos, TUBETU should automatically prepare an editable listing draft. Do not publish automatically.

## Required user flow
1. User adds up to 5 photos.
2. The browser validates and resizes photos, then sends them to the TUBETU-owned backend.
3. The backend's self-hosted vision model identifies only facts reasonably visible in the photos.
4. TUBETU AI returns a structured draft and category suggestion.
5. The form fills title, description, section/category, and any clearly supported fields. Price, location, condition, brand/model must remain blank unless the user provided them or they are confidently visible.
6. User edits the draft, enters price and other details, then explicitly publishes.
7. If recognition fails or confidence is low, keep the photos and let the user fill the form manually; show a useful, non-technical message.

## Non-negotiable architecture
- No OpenAI API, no paid third-party LLM API, and no API key in browser JavaScript.
- Reuse the existing `ai-core/` Python FastAPI service as the TUBETU-owned API layer where practical.
- The current `ai-core/main.py` is a rules-based text engine; it does **not** perform visual recognition. Do not label rules/keywords as image recognition.
- A real photo-recognition model must run on infrastructure controlled/selected for TUBETU (self-hosted open-weight vision model, e.g. a compatible Qwen-VL class model), or use a genuinely local on-device model. Choose the smallest model that meets accuracy/latency requirements after measuring the available host. If no inference host/model is deployed, return a clear `recognition_unavailable` state; never pretend to have recognized a photo.
- Supabase remains the database/auth layer. Never expose `SUPABASE_SERVICE_ROLE_KEY`, model credentials, or server secrets to the frontend.
- Preserve existing TUBETU UI, branding, categories and unrelated functionality.

## API contract
Add a protected/abuse-limited endpoint such as `POST /ai/photo-listing` to `ai-core/main.py`.
Request: multipart upload or JSON with up to 5 validated image data URLs; optional user note, preferred intent and current form context. Enforce request-size limits, MIME/signature checks, rate limiting, and safe image decoding.
Response JSON:
```json
{
  "ok": true,
  "recognizedObject": "string",
  "confidence": 0.0,
  "category": "one of the exact TUBETU sections",
  "sectionId": "stable internal section id",
  "title": "editable suggested title",
  "description": "editable factual draft",
  "location": null,
  "price": null,
  "intent": "Предложение",
  "suggestions": [],
  "recognitionSource": "self_hosted_model"
}
```
On low confidence, invalid/unsupported image, timeout, model unavailable or overload, return a typed error with an actionable message; do not fabricate fields. Do not return base64 photos in the response or persist images unless a separate explicit product requirement exists.

## Category mapping
Use the exact 13 top-level TUBETU sections already present in the site:
Проекты и идеи; Игры; Контент; Товары и ресурсы; Услуги; Логистика и перевозки; Финансы; Недвижимость; Транспорт; Сельское хозяйство; Техника и оборудование; Образование и опыт; Сообщества.
Map to existing section IDs only where those IDs are verified in the frontend/database. A model may suggest a category but must not invent a subcategory that does not exist in the app.

## Frontend integration
- Replace the current `db.functions.invoke('tubetu-ai', ...)` photo-listing path with a configured TUBETU AI Core endpoint only after the backend is deployed and reachable over HTTPS.
- Use a single endpoint configuration; never hardcode private keys in `index.html`.
- Trigger analysis automatically after photo selection and when photos change; prevent duplicate concurrent requests and ignore stale responses if the user replaces photos.
- Show states: preparing, analyzing, draft ready, low confidence, unavailable/error. Keep selected photos on failure.
- Populate title/description/category only after validating response fields. Never auto-publish.
- Keep existing manual editing, price input and submit flow unchanged.

## Deployment and secrets
- Deploy the FastAPI service to a server/container with HTTPS, resource limits, monitoring and rate limiting.
- Deploy/download the selected open-weight vision model on that host and record model/version, hardware, memory requirements and license.
- Configure `SUPABASE_URL`, server-only `SUPABASE_SERVICE_ROLE_KEY`, `ALLOWED_ORIGINS`, request-size limits and model path as server environment variables.
- Do not use the current Supabase Edge Function as a proxy to OpenAI. Either retire the OpenAI-dependent `tubetu-ai` path after cutover or leave it unused until the replacement passes tests.
- GitHub Actions currently has no repository Actions secrets. Do not assume a deployment secret exists or ask for a new token unless a deployment method actually requires it. Prefer a deployment method supported by the chosen host.

## Acceptance tests
1. One clear object photo produces a plausible title, factual description and correct top-level category.
2. Multiple photos of the same object are considered together without duplicating the listing.
3. Changing/removing photos cannot cause an old request to overwrite the current draft.
4. Unclear photo yields low confidence and no invented brand/model/price/location/condition.
5. Invalid file, oversized payload, timeout, rate limit and unavailable model produce understandable errors; form remains usable.
6. No publication occurs without the user's explicit submit action.
7. No OpenAI API calls occur; browser bundle contains no server secrets.
8. Unit tests cover category mapping, validation, response schema and failure states; integration test covers browser → backend → model.
9. Verify Russian and Kazakh labels/messages and test on mobile.
10. Test against staging Supabase schema/RLS before production publishing.

## Work plan
1. Audit current `ai-core/`, form IDs/handlers and existing Supabase schema.
2. Select and document a realistic inference host/model based on available compute; do not promise deployment before access exists.
3. Implement image validation, model adapter, structured response and tests in `ai-core/`.
4. Deploy backend/model with HTTPS and verify `/health` plus a real image test.
5. Integrate the frontend and preserve manual form behaviour.
6. Run acceptance tests, then cut over the photo-listing path.
7. Update `ai-core/UNIMPLEMENTED.md` only after each item is actually verified.

## Current known state (do not misrepresent)
- `ai-core/` exists and is a rules-based FastAPI scaffold; README says it makes no external LLM calls.
- `ai-core/UNIMPLEMENTED.md` says the Python API is not deployed and the frontend is not connected to it.
- Supabase Edge Function `tubetu-ai` currently calls `https://api.openai.com/v1/responses`, requires server secret `OPENAI_API_KEY`, and is not the no-paid-API solution requested.
- GitHub Actions repository secrets page was checked and showed no repository or environment secrets. The Edge Function deployment workflow therefore fails before deploy because `SUPABASE_ACCESS_TOKEN` is absent.
- The function test with no images returns HTTP 400 as expected. A 1-pixel image test returns HTTP 502 from the OpenAI call; this does not validate a self-hosted model.
