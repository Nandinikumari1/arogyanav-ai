import hashlib
import json
import secrets
import sqlite3
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = Path(__file__).resolve().parent / "arogyanav.db"

app = FastAPI(title="ArogyaNav AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

INITIAL_HOSPITALS = [
    {
        "name": "Gaya District & Referral Hospital",
        "city": "Gaya",
        "tier": "Government / Public",
        "pmjay_supported": 1,
        "supports_opd": 1,
        "supports_admission": 1,
        "est_opd_inr": 50,
        "est_admission_inr": 0,
        "note": "Low-cost OPD and inpatient care; verify PM-JAY e-card at Ayushman desk for eligible admission.",
    },
    {
        "name": "Anugrah Narayan Magadh Medical College & Hospital",
        "city": "Gaya",
        "tier": "Government Medical College",
        "pmjay_supported": 1,
        "supports_opd": 1,
        "supports_admission": 1,
        "est_opd_inr": 100,
        "est_admission_inr": 0,
        "note": "Broad specialty and inpatient departments; carry Aadhaar and scheme card for admission checks.",
    },
    {
        "name": "Patna City Care & Diagnostic Centre",
        "city": "Patna",
        "tier": "Private Multi-Specialty",
        "pmjay_supported": 0,
        "supports_opd": 1,
        "supports_admission": 1,
        "est_opd_inr": 500,
        "est_admission_inr": 35000,
        "note": "Faster appointment slots; out-of-pocket charges apply if no private insurance covers the visit.",
    },
    {
        "name": "IGIMS & Public Specialty Hub",
        "city": "Patna",
        "tier": "Government Specialty",
        "pmjay_supported": 1,
        "supports_opd": 1,
        "supports_admission": 1,
        "est_opd_inr": 150,
        "est_admission_inr": 0,
        "note": "Strong specialist and test setup; confirm package eligibility with Ayushman Mitra before admission.",
    },
]

INITIAL_MEDICINES = [
    {
        "brand_example": "Augmentin 625 Duo",
        "salt": "Amoxicillin + Clavulanic Acid",
        "use_note": "Antibiotic prescribed by a doctor for bacterial infections.",
        "branded_inr": 220,
        "generic_inr": 65,
        "keywords": ["augmentin", "amoxicillin", "clavulanic", "625"],
    },
    {
        "brand_example": "Pan-D Capsule",
        "salt": "Pantoprazole + Domperidone",
        "use_note": "Used for acidity and reflux when advised by a clinician.",
        "branded_inr": 160,
        "generic_inr": 32,
        "keywords": ["pan-d", "pand", "pantoprazole", "domperidone"],
    },
    {
        "brand_example": "Atorva 10mg",
        "salt": "Atorvastatin 10mg",
        "use_note": "Cholesterol-lowering medicine; take only as prescribed.",
        "branded_inr": 140,
        "generic_inr": 20,
        "keywords": ["atorva", "atorvastatin", "10mg"],
    },
    {
        "brand_example": "Dolo 650",
        "salt": "Paracetamol 650mg",
        "use_note": "Commonly used for fever or mild pain relief.",
        "branded_inr": 35,
        "generic_inr": 10,
        "keywords": ["dolo", "650", "paracetamol"],
    },
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored_hash: str) -> bool:
    if "$" not in stored_hash:
        return False
    salt, _ = stored_hash.split("$", 1)
    return secrets.compare_digest(hash_password(password, salt), stored_hash)


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS hospitals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                tier TEXT NOT NULL,
                pmjay_supported INTEGER NOT NULL,
                supports_opd INTEGER NOT NULL,
                supports_admission INTEGER NOT NULL,
                est_opd_inr INTEGER NOT NULL,
                est_admission_inr INTEGER NOT NULL,
                note TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_example TEXT NOT NULL,
                salt TEXT NOT NULL,
                use_note TEXT NOT NULL,
                branded_inr INTEGER NOT NULL,
                generic_inr INTEGER NOT NULL,
                keywords_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                saved_city TEXT NOT NULL DEFAULT 'All',
                has_pmjay INTEGER NOT NULL DEFAULT 0,
                session_token TEXT
            )
            """
        )

        hospital_count = conn.execute("SELECT COUNT(*) AS cnt FROM hospitals").fetchone()["cnt"]
        if hospital_count == 0:
            for h in INITIAL_HOSPITALS:
                conn.execute(
                    """
                    INSERT INTO hospitals (
                        name, city, tier, pmjay_supported, supports_opd,
                        supports_admission, est_opd_inr, est_admission_inr, note
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        h["name"],
                        h["city"],
                        h["tier"],
                        h["pmjay_supported"],
                        h["supports_opd"],
                        h["supports_admission"],
                        h["est_opd_inr"],
                        h["est_admission_inr"],
                        h["note"],
                    ),
                )

        medicine_count = conn.execute("SELECT COUNT(*) AS cnt FROM medicines").fetchone()["cnt"]
        if medicine_count == 0:
            for m in INITIAL_MEDICINES:
                conn.execute(
                    """
                    INSERT INTO medicines (
                        brand_example, salt, use_note, branded_inr, generic_inr, keywords_json
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        m["brand_example"],
                        m["salt"],
                        m["use_note"],
                        m["branded_inr"],
                        m["generic_inr"],
                        json.dumps(m["keywords"]),
                    ),
                )


class PrescriptionInput(BaseModel):
    text: str


class RegisterInput(BaseModel):
    full_name: str
    email: str
    password: str


class LoginInput(BaseModel):
    email: str
    password: str


class ProfileUpdateInput(BaseModel):
    saved_city: str
    has_pmjay: bool


@app.on_event("startup")
def on_startup():
    init_db()


def get_user_by_token(authorization: str | None) -> sqlite3.Row | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        return None
    with get_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE session_token = ?", (token,)).fetchone()


def score_hospital(hospital: dict, care_type: str, has_pmjay: bool) -> tuple[int, str]:
    score = 50
    reasons = []

    if care_type == "opd" and hospital["supports_opd"]:
        score += 20
        reasons.append("Covers routine OPD checkups")
    elif care_type == "tests" and hospital["supports_opd"]:
        score += 18
        reasons.append("Has OPD & diagnostic evaluation")
    elif care_type == "admission" and hospital["supports_admission"]:
        score += 22
        reasons.append("Supports inpatient admission")

    if has_pmjay:
        if hospital["pmjay_supported"] and care_type == "admission":
            score += 25
            reasons.append("PM-JAY aligned for eligible inpatient admission")
        elif hospital["pmjay_supported"] and care_type != "admission":
            score += 10
            reasons.append("PM-JAY empaneled (note: scheme mainly targets eligible inpatient care, not routine OPD)")
        else:
            score -= 20
            reasons.append("No PM-JAY coverage shown here—higher out-of-pocket risk")
    else:
        if hospital["est_opd_inr"] <= 200:
            score += 12
            reasons.append("Budget-friendly base visit cost")

    return min(score, 99), "; ".join(reasons)


def fetch_all_medicines() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM medicines ORDER BY id").fetchall()
    result = []
    for row in rows:
        result.append(
            {
                "id": row["id"],
                "brand_example": row["brand_example"],
                "salt": row["salt"],
                "use_note": row["use_note"],
                "branded_inr": row["branded_inr"],
                "generic_inr": row["generic_inr"],
                "keywords": json.loads(row["keywords_json"]),
            }
        )
    return result


@app.get("/")
def home():
    return {
        "app": "ArogyaNav AI",
        "status": "Backend server is running with SQLite + Auth!",
        "step": 6,
    }


@app.post("/api/auth/register")
def register_user(payload: RegisterInput):
    email = payload.email.strip().lower()
    name = payload.full_name.strip()
    if len(name) < 2 or "@" not in email or len(payload.password) < 4:
        raise HTTPException(status_code=400, detail="Enter valid name, email, and password (4+ chars).")

    token = secrets.token_hex(24)
    pw_hash = hash_password(payload.password)

    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO users (full_name, email, password_hash, session_token)
                VALUES (?, ?, ?, ?)
                """,
                (name, email, pw_hash, token),
            )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="This email is already registered. Please log in.")

    return {
        "token": token,
        "user": {
            "full_name": name,
            "email": email,
            "saved_city": "All",
            "has_pmjay": False,
        },
    }


@app.post("/api/auth/login")
def login_user(payload: LoginInput):
    email = payload.email.strip().lower()
    with get_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not user or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password.")

        token = secrets.token_hex(24)
        conn.execute("UPDATE users SET session_token = ? WHERE id = ?", (token, user["id"]))

    return {
        "token": token,
        "user": {
            "full_name": user["full_name"],
            "email": user["email"],
            "saved_city": user["saved_city"],
            "has_pmjay": bool(user["has_pmjay"]),
        },
    }


@app.get("/api/auth/me")
def get_current_user(authorization: str | None = Header(default=None)):
    user = get_user_by_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Not logged in.")
    return {
        "full_name": user["full_name"],
        "email": user["email"],
        "saved_city": user["saved_city"],
        "has_pmjay": bool(user["has_pmjay"]),
    }


@app.post("/api/auth/profile")
def update_profile(payload: ProfileUpdateInput, authorization: str | None = Header(default=None)):
    user = get_user_by_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Please log in first to save your family profile.")
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET saved_city = ?, has_pmjay = ? WHERE id = ?",
            (payload.saved_city, 1 if payload.has_pmjay else 0, user["id"]),
        )
    return {
        "message": "Family preferences saved to database!",
        "saved_city": payload.saved_city,
        "has_pmjay": payload.has_pmjay,
    }


@app.post("/api/auth/logout")
def logout_user(authorization: str | None = Header(default=None)):
    user = get_user_by_token(authorization)
    if user:
        with get_connection() as conn:
            conn.execute("UPDATE users SET session_token = NULL WHERE id = ?", (user["id"],))
    return {"message": "Logged out safely."}


@app.get("/api/hospitals")
def get_hospitals(
    city: str = "All",
    care_type: str = "opd",
    has_pmjay: bool = False,
):
    query = "SELECT * FROM hospitals"
    params: list = []
    if city != "All":
        query += " WHERE LOWER(city) = LOWER(?)"
        params.append(city)

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    results = []
    for row in rows:
        h = {
            "id": row["id"],
            "name": row["name"],
            "city": row["city"],
            "tier": row["tier"],
            "pmjay_supported": bool(row["pmjay_supported"]),
            "supports_opd": bool(row["supports_opd"]),
            "supports_admission": bool(row["supports_admission"]),
            "est_opd_inr": row["est_opd_inr"],
            "est_admission_inr": row["est_admission_inr"],
            "note": row["note"],
        }
        match_score, reason = score_hospital(h, care_type, has_pmjay)
        results.append({
            **h,
            "match_score": match_score,
            "match_reason": reason,
        })

    results.sort(key=lambda item: item["match_score"], reverse=True)
    return {"count": len(results), "hospitals": results}


@app.get("/api/medicines")
def search_medicines(q: str = ""):
    query = q.strip().lower()
    all_meds = fetch_all_medicines()
    matches = []
    for med in all_meds:
        haystack = " ".join([med["brand_example"], med["salt"], *med["keywords"]]).lower()
        if not query or query in haystack:
            savings = max(med["branded_inr"] - med["generic_inr"], 0)
            matches.append({
                **med,
                "savings_inr": savings,
            })
    return {"count": len(matches), "medicines": matches}


@app.post("/api/scan-prescription")
def scan_prescription(payload: PrescriptionInput):
    lower_text = payload.text.lower()
    all_meds = fetch_all_medicines()
    matched_items = []
    total_branded = 0
    total_generic = 0

    for med in all_meds:
        if any(kw in lower_text for kw in med["keywords"]):
            savings = max(med["branded_inr"] - med["generic_inr"], 0)
            matched_items.append({
                **med,
                "savings_inr": savings,
            })
            total_branded += med["branded_inr"]
            total_generic += med["generic_inr"]

    return {
        "matched_count": len(matched_items),
        "total_branded_inr": total_branded,
        "total_generic_inr": total_generic,
        "total_savings_inr": max(total_branded - total_generic, 0),
        "items": matched_items,
    }