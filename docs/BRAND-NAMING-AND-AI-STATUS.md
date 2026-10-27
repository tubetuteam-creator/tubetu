# TUBETU — naming standard

## Fixed brand names

- **Platform:** TUBETU
- **Artificial-intelligence module:** 2B2 AI
- **Exact spelling:** `2B2 AI` — digit 2, uppercase B, digit 2, space, uppercase A and uppercase I.
- Do not use `2B2 AL`, `TUBETU AI`, or other variants as the module name.

This is the agreed naming standard for the website UI, AI assistant labels, documentation, and future development.

## Outstanding technical task

The **2B2 AI** photo-analysis button in the listing form is not working reliably. Required behavior:
1. Accept up to five photos.
2. Send them to the Supabase Edge Function `tubetu-ai`.
3. Analyze the images and fill in the listing title, category, and description.
4. Show a clear loading state and a useful error if the backend is unavailable.

The frontend currently invokes `tubetu-ai` with `mode: "create_listing"`. The Edge Function source supports that mode, but source code in GitHub does not automatically deploy the function to Supabase. Verify the deployed function version and the server-side `OPENAI_API_KEY` secret in Supabase before marking the feature as operational. Never place the OpenAI secret in frontend code.
