# ArogyaNav AI — Family Hospital & Generic Medicine Companion

A full-stack healthcare navigation and out-of-pocket cost-reduction web application for Indian families. It combines a **3-layer hospital care triage engine** with a **bipartite branded-to-generic medicine knowledge graph** (PMBJP Jan Aushadhi), helping households find nearby hospitals, check health card support, compare cheaper generic medicines, and estimate treatment costs in English and Hindi.

## Live Links
- **Live Web App (Frontend):** `https://nandinikumari1.github.io/arogyanav-ai/frontend/index.html`
- **Live Backend API (FastAPI):** `https://arogyanav-api.onrender.com`
- **Interactive API Docs (Swagger UI):** `https://arogyanav-api.onrender.com/docs`

## Key Features
- **3-Layer Care Triage & Hospital Ranking:** Prioritizes low-cost Government & Charitable clinics (₹10–₹150 OPD) for routine checkups, matches specialists with PM-JAY continuity, and filters ₹0 cashless admission/surgery facilities across 100 hospitals in 10 Indian cities.
- **Jan Aushadhi Generic Medicine Comparator:** Maps 100 popular branded medicines to their exact active chemical salts and Govt of India PMBJP codes, calculating monthly and annual savings alongside Google Maps, Tata 1mg, and PharmEasy links.
- **Instant Prescription Scanner:** Extracts prescribed brands from pasted doctor notes or uploaded prescription images to find generic equivalents in one click.
- **Surgery & Hospital Admission Cost Estimator:** Compares private cash bills against cashless Ayushman Bharat (PM-JAY) and State Health Card coverage (including 3-day pre-op and 15-day post-discharge medicines).
- **Hospital Visit Checklist & Printable Slip:** Readiness tracker for Ayushman Mitra verification plus a printable/copyable pharmacy slip with toll-free helplines (`14555` and `1800-180-8080`).
- **Bilingual UI & Examiner / Viva Mode:** Instant English / हिन्दी toggle and an academic evaluation dashboard (`NDCG@4: 0.942`, hybrid scoring equation, and interactive Drug–Salt–Generic Knowledge Graph).

## Tech Stack
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python 3, FastAPI, Uvicorn, Pydantic
- **Database:** SQLite (`arogyanav.db`)
- **Hosting:** GitHub Pages (Frontend) + Render (FastAPI Backend)

## Run Locally
1. **Start the backend:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload