# Veracity: Full Project Context Export
> Date: June 1, 2026 | Session: Final Build & Deployment | Node: tupu-macbook

## 1. Project Overview
**Veracity** is a high-speed, zero-trust fact-checking engine built for real-time RAG analysis. It cross-references user claims against global news telemetry via NewsAPI.

## 2. Technical Architecture
- **Backend:** Python/Flask serverless architecture.
- **AI Models:** 
  - Groq LPU (Primary): Llama 3.3 70B (Analysis) & Llama 3.1 8B (Keywords).
  - Google Gemini (Alternative): Gemini 2.0 Flash.
  - Custom: Supports any OpenAI-compatible endpoint (OpenRouter, local Ollama).
- **Security (BYOK):** "Bring Your Own Key" model. API keys are stored in the user's browser `localStorage` and sent via request headers. The backend never logs or persists keys.
- **RAG Pipeline:** 
  1. User input -> AI keyword extraction.
  2. NewsAPI fetch (12 latest articles).
  3. AI "Autopsy" (Cross-examination of news vs. claim).
  4. Adaptive Search: "Feeling Lucky" retry logic broadens the query if the first search yields 0 results.

## 3. UI/UX Design
- **Theme:** Midnight Obsidian (Dark Mode).
- **Layout:** Bento Grid 2.0 with 28px rounded corners.
- **Aesthetic:** Glassmorphism (30px blur), Geist Mono typography, and Apple-style stagger-reveal animations.
- **History:** Persistent local history sidebar using browser storage.

## 4. Key Implementation Details
- **Environment Sanitization:** `app.py` explicitly pops proxy environment variables (`HTTP_PROXY`, etc.) to prevent `httpx` initialization crashes in modern AI SDKs.
- **Deployment:** Live on Vercel with automatic CI/CD via GitHub.
- **Domain:** `arnishsarkar.com` (Cloudflare-managed DNS).
- **Vercel Config:** `vercel.json` maps all routes to `app.py` as a serverless function.

## 5. File Registry
- `app.py`: Flask routes and AI orchestration logic.
- `templates/index.html`: Main SPA interface with Vanilla JS logic.
- `templates/privacy.html`: Zero-trust digital constitution.
- `templates/terms.html`: Usage protocols.
- `templates/api_docs.html`: Key acquisition guide (including Ngrok/Ollama setup).
- `requirements.txt`: Project dependencies (`flask`, `groq`, `google-genai`).
- `.gitignore`: Protects `.env` and `venv/`.

## 6. Financial & Career Context (May 2026)
- **DA Arrears:** West Bengal government initiated payments for retired staff (2008-2015). Active GIA teachers (Mom) currently excluded/stalled (potential 24-month GPF lock-in).
- **Portfolio:** ₹2.50 lakh deployed in Mutual Funds.
- **Identity:** Tupu (Arnish Sarkar), B.Tech CSE (AI/ML), MAKAUT, aiming for Australia migration.

## 7. Next Steps for Next AI
- Implement "Follow-up" chat history memory (requires passing previous context back to Groq).
- Add "Social Share" feature for verdicts.
- Monitor June 1st meeting results for Mom's DA inclusion.
