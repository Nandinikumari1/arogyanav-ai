# ArogyaNav AI

A simple full-stack healthcare helper web app for families to find nearby hospitals, check health card support, compare cheaper generic medicines, and estimate treatment costs in easy English and Hindi.

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI, Uvicorn
- **Database:** SQLite

## Run Locally
1. Start backend:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload