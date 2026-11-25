const API_BASE = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
  ? "http://127.0.0.1:8000"
  : "https://arogyanav-api.onrender.com";

// ==================== BILINGUAL DICTIONARY ====================
const I18N = {
  en: {
    hdrTitle: "ArogyaNav AI — Family Hospital & Generic Medicine Companion",
    hdrSub: "Right hospital care layer + Jan Aushadhi generic medicine savings for every Indian family",
    btnLang: "हिन्दी",
    lblSavedPlan: "Saved Plan",
    btnViva: "Examiner / Viva Mode",
    tabHospitals: "1. Find Hospitals",
    tabMedicines: "2. Save on Medicines",
    tabScanner: "3. Scan Prescription",
    tabSurgery: "4. Surgery Cost",
    tabChecklist: "5. Visit Checklist",
    lblCity: "Your City",
    lblNeed: "Health Need",
    lblCard: "Your Health Card",
    lblPriority: "What Matters More?",
    lblTopFac: "Top Facilities",
    lblLowBill: "Lowest Bill",
    hospListTitle: "Recommended Hospitals",
    medSecTitle: "Compare Branded Medicines with Jan Aushadhi Generics",
    medSecSub: "Same active chemical salt, approved by Govt of India (PMBJP), up to 85% lower MRP",
    scanTitle: "Instant Prescription Salt & Generic Extractor",
    scanSub: "Paste text from your doctor's prescription or upload a prescription photo to automatically find Jan Aushadhi alternatives.",
    surgTitle: "Surgery & Hospital Admission Bill Estimator",
    surgSub: "See how much your family saves with Ayushman Bharat (PM-JAY) or State Health Card, including pre- and post-hospitalization medicines.",
    chkTitle: "Hospital Visit & Ayushman Mitra Desk Checklist",
    chkSub: "Tick off these documents before leaving home so your cashless admission is approved smoothly without delays."
  },
  hi: {
    hdrTitle: "आरोग्यनव AI — पारिवारिक अस्पताल एवं जन औषधि सहायक",
    hdrSub: "सही अस्पताल स्तर का चुनाव + जन औषधि जेनेरिक दवाइयों से हर परिवार की बड़ी बचत",
    btnLang: "English",
    lblSavedPlan: "सेव प्लान",
    btnViva: "परीक्षक / वाइवा मोड",
    tabHospitals: "1. अस्पताल खोजें",
    tabMedicines: "2. दवाइयों पर बचत",
    tabScanner: "3. पर्चा स्कैन करें",
    tabSurgery: "4. ऑपरेशन खर्च",
    tabChecklist: "5. अस्पताल चेकलिस्ट",
    lblCity: "आपका शहर",
    lblNeed: "स्वास्थ्य आवश्यकता",
    lblCard: "आपका स्वास्थ्य कार्ड",
    lblPriority: "क्या अधिक ज़रूरी है?",
    lblTopFac: "बेहतर सुविधाएं",
    lblLowBill: "सबसे कम खर्च",
    hospListTitle: "सुझाए गए सर्वश्रेष्ठ अस्पताल",
    medSecTitle: "ब्रांडेड दवाइयों की जन औषधि जेनेरिक से तुलना करें",
    medSecSub: "बिल्कुल वही सक्रिय साल्ट, भारत सरकार (PMBJP) द्वारा प्रमाणित, 85% तक कम कीमत",
    scanTitle: "डॉक्टर के पर्चे से तुरंत जेनेरिक दवा खोजें",
    scanSub: "पर्चे का टेक्स्ट पेस्ट करें या फोटो अपलोड करें — ऐप अपने आप जन औषधि विकल्प दिखा देगा।",
    surgTitle: "ऑपरेशन और भर्ती खर्च कैलकुलेटर",
    surgSub: "जानें आयुष्मान भारत (PM-JAY) कार्ड से भर्ती से 3 दिन पहले और छुट्टी के 15 दिन बाद तक मुफ्त इलाज कैसे मिलता है।",
    chkTitle: "अस्पताल जाने से पहले ज़रूरी दस्तावेज़ चेकलिस्ट",
    chkSub: "घर से निकलने से पहले इन दस्तावेज़ों पर टिक करें ताकि कैशलेस भर्ती बिना रुकावट हो सके।"
  }
};

// ==================== INLINE SVG VISUAL GENERATORS ====================
function getHospitalSVG(category) {
  if (category === "polyclinic") {
    return `<svg viewBox="0 0 80 80" width="68" height="68">
      <rect width="80" height="80" rx="12" fill="#ecfdf5"/>
      <rect x="14" y="28" width="52" height="38" rx="4" fill="#10b981"/>
      <polygon points="10,30 40,14 70,30" fill="#047857"/>
      <rect x="34" y="46" width="12" height="20" fill="#ecfdf5"/>
      <rect x="37" y="20" width="6" height="14" fill="#fff"/>
      <rect x="33" y="24" width="14" height="6" fill="#fff"/>
    </svg>`;
  }
  if (category === "charitable") {
    return `<svg viewBox="0 0 80 80" width="68" height="68">
      <rect width="80" height="80" rx="12" fill="#eff6ff"/>
      <rect x="16" y="24" width="48" height="42" rx="5" fill="#3b82f6"/>
      <rect x="24" y="16" width="32" height="10" rx="3" fill="#1d4ed8"/>
      <path d="M40 47c-6-4-10-8-10-12a6 6 0 0 1 10-4 6 6 0 0 1 10 4c0 4-4 8-10 12z" fill="#fde047"/>
      <rect x="34" y="52" width="12" height="14" fill="#dbeafe"/>
    </svg>`;
  }
  if (category === "private") {
    return `<svg viewBox="0 0 80 80" width="68" height="68">
      <rect width="80" height="80" rx="12" fill="#f1f5f9"/>
      <rect x="18" y="14" width="44" height="52" rx="4" fill="#334155"/>
      <rect x="24" y="22" width="8" height="8" fill="#38bdf8"/>
      <rect x="36" y="22" width="8" height="8" fill="#38bdf8"/>
      <rect x="48" y="22" width="8" height="8" fill="#38bdf8"/>
      <rect x="24" y="34" width="8" height="8" fill="#38bdf8"/>
      <rect x="36" y="34" width="8" height="8" fill="#38bdf8"/>
      <rect x="48" y="34" width="8" height="8" fill="#38bdf8"/>
      <rect x="34" y="50" width="12" height="16" fill="#94a3b8"/>
    </svg>`;
  }
  return `<svg viewBox="0 0 80 80" width="68" height="68">
    <rect width="80" height="80" rx="12" fill="#f0fdf4"/>
    <rect x="12" y="22" width="56" height="44" rx="4" fill="#059669"/>
    <rect x="26" y="12" width="28" height="12" rx="3" fill="#065f46"/>
    <rect x="37" y="14" width="6" height="8" fill="#fff"/>
    <rect x="36" y="15" width="8" height="6" fill="#fff"/>
    <rect x="20" y="30" width="9" height="9" fill="#d1fae5"/>
    <rect x="35" y="30" width="9" height="9" fill="#d1fae5"/>
    <rect x="50" y="30" width="9" height="9" fill="#d1fae5"/>
    <rect x="33" y="48" width="14" height="18" fill="#ecfdf5"/>
  </svg>`;
}

function getMedicineSVG(format) {
  if (format === "Capsule") {
    return `<svg viewBox="0 0 80 80" width="68" height="68">
      <rect width="80" height="80" rx="12" fill="#eff6ff"/>
      <g transform="rotate(-32 40 40)">
        <rect x="16" y="28" width="24" height="24" rx="12" fill="#2563eb"/>
        <rect x="40" y="28" width="24" height="24" rx="12" fill="#f59e0b"/>
      </g>
    </svg>`;
  }
  if (format === "Syrup") {
    return `<svg viewBox="0 0 80 80" width="68" height="68">
      <rect width="80" height="80" rx="12" fill="#fef3c7"/>
      <rect x="33" y="14" width="14" height="8" rx="2" fill="#92400e"/>
      <rect x="26" y="22" width="28" height="44" rx="6" fill="#d97706"/>
      <rect x="28" y="34" width="24" height="18" fill="#fffbeb"/>
      <rect x="38" y="38" width="4" height="10" fill="#047857"/>
      <rect x="35" y="41" width="10" height="4" fill="#047857"/>
    </svg>`;
  }
  if (format === "Inhaler" || format === "Drops") {
    return `<svg viewBox="0 0 80 80" width="68" height="68">
      <rect width="80" height="80" rx="12" fill="#f0f9ff"/>
      <path d="M30 16h16v32l12 10v10H28V48z" fill="#0284c7"/>
      <rect x="34" y="12" width="8" height="6" fill="#0369a1"/>
    </svg>`;
  }
  if (format === "Gel") {
    return `<svg viewBox="0 0 80 80" width="68" height="68">
      <rect width="80" height="80" rx="12" fill="#fdf2f8"/>
      <polygon points="24,20 56,20 50,56 30,56" fill="#db2777"/>
      <rect x="35" y="56" width="10" height="8" fill="#9d174d"/>
    </svg>`;
  }
  if (format === "Sachet") {
    return `<svg viewBox="0 0 80 80" width="68" height="68">
      <rect width="80" height="80" rx="12" fill="#ecfdf5"/>
      <rect x="20" y="16" width="40" height="48" rx="4" fill="#10b981"/>
      <text x="40" y="44" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold">ORS</text>
    </svg>`;
  }
  return `<svg viewBox="0 0 80 80" width="68" height="68">
    <rect width="80" height="80" rx="12" fill="#ecfdf5"/>
    <rect x="18" y="14" width="44" height="52" rx="6" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>
    <circle cx="31" cy="27" r="6" fill="#fff"/>
    <circle cx="49" cy="27" r="6" fill="#fff"/>
    <circle cx="31" cy="41" r="6" fill="#fff"/>
    <circle cx="49" cy="41" r="6" fill="#fff"/>
    <circle cx="31" cy="55" r="6" fill="#fff"/>
    <circle cx="49" cy="55" r="6" fill="#fff"/>
  </svg>`;
}

const CITIES = ["Gaya", "Patna", "Durgapur", "Kolkata", "Asansol", "Ranchi", "Jamshedpur", "Varanasi", "Lucknow", "Delhi NCR"];
const SPECIALTIES = [
  "General Medicine", "Cardiology", "Orthopaedics", "Diabetology",
  "Ophthalmology", "Obstetrics & Gynaecology", "Oncology", "Nephrology", "Neurology", "Pulmonology"
];

let ALL_HOSPITALS = [];
let ALL_MEDICINES = [];

const PROCEDURES = [
  { id: "angio", name: "Heart Stent / Angioplasty (1 Stent)", priv: 185000, pmjay: 65000, stay: "3–4 Days ICU + Ward", prePost: "3 days pre-admission tests + 15 days free cardiac medicines" },
  { id: "knee", name: "Total Knee Joint Replacement (Single)", priv: 165000, pmjay: 80000, stay: "4–5 Days Hospital Stay", prePost: "3 days pre-op X-ray/blood tests + 15 days pain & physio meds" },
  { id: "cataract", name: "Cataract Eye Surgery (Phaco + IOL Lens)", priv: 32000, pmjay: 12000, stay: "Same-Day / 24-Hr Care", prePost: "Pre-op eye biometry + 15 days post-op antibiotic eye drops" },
  { id: "dialysis", name: "Kidney Haemodialysis (Monthly 8 Sessions)", priv: 24000, pmjay: 14400, stay: "Day-Care / Regular", prePost: "Includes dialyzer, tubing, EPO check & routine lab monitoring" },
  { id: "delivery", name: "C-Section / High-Risk Maternity Delivery", priv: 68000, pmjay: 22000, stay: "3–4 Days Maternity Ward", prePost: "Ultrasound/blood tests + 15 days mother & newborn care meds" },
  { id: "gallbladder", name: "Laparoscopic Gallbladder Stone Removal", priv: 75000, pmjay: 28000, stay: "2–3 Days Surgical Ward", prePost: "3 days pre-op USG/LFT + 15 days post-surgery antibiotics" }
];

const CHECKLIST_DATA = [
  { id: "chk1", title: "Ayushman Bharat Golden Card / ABHA ID / State Health Card", desc: "Carry printed card or PDF on mobile phone to show at the Ayushman Mitra counter." },
  { id: "chk2", title: "Patient's Original Aadhaar Card (for Biometric / OTP e-KYC)", desc: "Required for instant fingerprint or Aadhaar-linked mobile OTP verification." },
  { id: "chk3", title: "Ration Card / PM-JAY Family Verification Letter", desc: "Helps link family members if your individual Golden Card is being generated on-site." },
  { id: "chk4", title: "Doctor's Referral Note, Old Prescriptions & Lab Reports", desc: "Needed by the hospital to submit pre-authorization package approval under PM-JAY." }
];

let state = {
  lang: "en",
  vivaMode: false,
  activeTab: "hospitals",
  careLayer: "mild_opd",
  showAllHospitals: false,
  savedHospitalIds: ["HOSP-002"],
  basketMedIds: ["MED-001", "MED-010", "MED-022"],
  medIllnessFilter: "All",
  browseAllMeds: false,
  checkedDocs: { chk1: true, chk2: true, chk3: false, chk4: false }
};

async function init() {
  const selCity = document.getElementById("selCity");
  selCity.innerHTML = `<option value="All">All 10 Cities (100 Hospitals)</option>` +
    CITIES.map(c => `<option value="${c}" ${c === "Gaya" ? "selected" : ""}>${c}</option>`).join("");

  const selSpec = document.getElementById("selSpecialty");
  selSpec.innerHTML = SPECIALTIES.map(s => `<option value="${s}">${s}</option>`).join("");

  const selScheme = document.getElementById("selScheme");
  selScheme.innerHTML = `
    <option value="PM-JAY">Ayushman Bharat Card (PM-JAY)</option>
    <option value="State Health Card">State Health Card</option>
    <option value="ESIC / CGHS">ESIC / CGHS</option>
    <option value="None / Cash">Paying Cash (No Card)</option>
  `;

  const selProc = document.getElementById("selProcedure");
  selProc.innerHTML = PROCEDURES.map(p => `<option value="${p.id}">${p.name}</option>`).join("");

  try {
    const [hospRes, medRes] = await Promise.all([
      fetch(`${API_BASE}/api/hospitals`),
      fetch(`${API_BASE}/api/medicines`)
    ]);
    ALL_HOSPITALS = await hospRes.json();
    ALL_MEDICINES = await medRes.json();
  } catch (err) {
    showToast("Backend server offline — run uvicorn main:app --reload");
  }

  const vivaSel = document.getElementById("vivaDrugSelect");
  vivaSel.innerHTML = ALL_MEDICINES.slice(0, 25).map(m =>
    `<option value="${m.id}">${m.brand} (₹${m.bMrp}) → ${m.gCode}</option>`
  ).join("");

  updateSavedBadge();
  renderCareLayers();
  renderHospitals();
  renderIllnessPills();
  renderMedicines();
  renderSurgeryEstimator();
  renderChecklist();
  renderVivaGraph();
}

function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(() => t.classList.remove("show"), 2600);
}

function toggleLang() {
  state.lang = state.lang === "en" ? "hi" : "en";
  const dict = I18N[state.lang];
  document.getElementById("hdrTitle").textContent = dict.hdrTitle;
  document.getElementById("hdrSub").textContent = dict.hdrSub;
  document.getElementById("btnLang").textContent = dict.btnLang;
  document.getElementById("lblSavedPlan").textContent = dict.lblSavedPlan;
  document.getElementById("btnViva").textContent = dict.btnViva;
  document.getElementById("tabBtnHospitals").textContent = dict.tabHospitals;
  document.getElementById("tabBtnMedicines").textContent = dict.tabMedicines;
  document.getElementById("tabBtnScanner").textContent = dict.tabScanner;
  document.getElementById("tabBtnSurgery").textContent = dict.tabSurgery;
  document.getElementById("tabBtnChecklist").textContent = dict.tabChecklist;
  document.getElementById("lblCity").textContent = dict.lblCity;
  document.getElementById("lblNeed").textContent = dict.lblNeed;
  document.getElementById("lblCard").textContent = dict.lblCard;
  document.getElementById("lblPriority").textContent = dict.lblPriority;
  document.getElementById("lblTopFac").textContent = dict.lblTopFac;
  document.getElementById("lblLowBill").textContent = dict.lblLowBill;
  document.getElementById("hospListTitle").textContent = dict.hospListTitle;
  document.getElementById("medSecTitle").textContent = dict.medSecTitle;
  document.getElementById("medSecSub").textContent = dict.medSecSub;
  document.getElementById("scanTitle").textContent = dict.scanTitle;
  document.getElementById("scanSub").textContent = dict.scanSub;
  document.getElementById("surgTitle").textContent = dict.surgTitle;
  document.getElementById("surgSub").textContent = dict.surgSub;
  document.getElementById("chkTitle").textContent = dict.chkTitle;
  document.getElementById("chkSub").textContent = dict.chkSub;
  renderCareLayers();
  renderHospitals();
}

function toggleVivaMode() {
  state.vivaMode = !state.vivaMode;
  const sec = document.getElementById("vivaSection");
  const btn = document.getElementById("btnViva");
  sec.style.display = state.vivaMode ? "block" : "none";
  btn.classList.toggle("active-viva", state.vivaMode);
  if (state.vivaMode) sec.scrollIntoView({ behavior: "smooth" });
}

function switchTab(tabName) {
  state.activeTab = tabName;
  ["hospitals", "medicines", "scanner", "surgery", "checklist"].forEach(t => {
    document.getElementById(`tab-${t}`).style.display = t === tabName ? "block" : "none";
  });
  document.querySelectorAll(".nav-tab").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tabName);
  });
}

// ==================== TAB 1: CARE LAYERS & HOSPITALS ====================
function renderCareLayers() {
  const layers = state.lang === "hi" ? [
    { id: "mild_opd", title: "1. सामान्य जांच (OPD)", desc: "खांसी, जुकाम, हल्का बुखार, गैस — नज़दीकी सरकारी/चैरिटी क्लिनिक (₹10–₹150)" },
    { id: "specialist_opd", title: "2. विशेषज्ञ डॉक्टर व जांच", desc: "दिल, शुगर, हड्डी या आंख की जांच + PM-JAY पैनल निरंतरता" },
    { id: "admission_surgery", title: "3. अस्पताल भर्ती / ऑपरेशन", desc: "24+ घंटे भर्ती और सर्जरी — आयुष्मान भारत (₹0 कैशलेस) कवर" }
  ] : [
    { id: "mild_opd", title: "1. Mild Checkup (OPD)", desc: "Cough, cold, mild fever, acidity — nearby Govt & Charitable clinics (₹10–₹150)" },
    { id: "specialist_opd", title: "2. Specialist & Tests", desc: "Heart, diabetes, bone or eye review + PM-JAY empanelled continuity" },
    { id: "admission_surgery", title: "3. Admission / Surgery", desc: "Hospital stay (24+ hrs) & surgery — full ₹0 Cashless PM-JAY matching" }
  ];

  document.getElementById("careLayerGrid").innerHTML = layers.map(l => `
    <button class="layer-card ${state.careLayer === l.id ? "active" : ""}" onclick="selectCareLayer('${l.id}')">
      <div class="layer-top">
        <span class="layer-title">${l.title}</span>
        <span class="layer-count">100 Hospitals</span>
      </div>
      <p class="layer-desc">${l.desc}</p>
    </button>
  `).join("");
}

function selectCareLayer(layerId) {
  state.careLayer = layerId;
  renderCareLayers();
  renderHospitals();
}

function toggleShowAllHospitals() {
  state.showAllHospitals = !state.showAllHospitals;
  renderHospitals();
}

function renderHospitals() {
  const city = document.getElementById("selCity").value;
  const spec = document.getElementById("selSpecialty").value;
  const scheme = document.getElementById("selScheme").value;
  const wAff = Number(document.getElementById("rngAfford").value) / 100;
  const wQual = 1 - wAff;
  const layer = state.careLayer;

  const advBox = document.getElementById("schemeAdvisoryBox");
  if (layer === "mild_opd" && (scheme === "PM-JAY" || scheme === "State Health Card")) {
    advBox.style.display = "flex";
    advBox.innerHTML = `<strong>Important Rule:</strong> <span>${
      state.lang === "hi"
        ? `${scheme} केवल 24+ घंटे अस्पताल भर्ती या ऑपरेशन पर लागू होता है, सामान्य खांसी-जुकाम की OPD पर नहीं। इसलिए ArogyaNav ने महंगे प्राइवेट अस्पतालों (₹600–₹1,100 OPD) की जगह नज़दीकी सरकारी और चैरिटी क्लिनिक (₹10–₹150) को ऊपर रखा है।`
        : `${scheme} covers inpatient hospital admission (24+ hours), NOT routine cough/cold OPD checkups. ArogyaNav automatically prioritizes nearby Government & Charitable clinics (₹10–₹150 OPD) and down-ranks expensive ₹600–₹1,100 private corporate hospitals.`
    }</span>`;
  } else if (layer === "specialist_opd" && (scheme === "PM-JAY" || scheme === "State Health Card")) {
    advBox.style.display = "flex";
    advBox.innerHTML = `<strong>Continuity Tip:</strong> <span>OPD consultation is self-paid, so ArogyaNav boosts hospitals that are <strong>also ${scheme}-empanelled</strong>—ensuring free cashless admission without shifting hospitals if further treatment is needed.</span>`;
  } else {
    advBox.style.display = "none";
  }

  const filtered = ALL_HOSPITALS.filter(h => city === "All" || h.city === city);

  const scored = filtered.map(h => {
    const hasSpec = h.specs.includes(spec);
    const schemeOk = scheme !== "None / Cash" && h.schemes.includes(scheme);
    const isPublicOrChar = h.cat === "govt" || h.cat === "polyclinic" || h.cat === "charitable";
    const proxScore = Math.exp(-0.08 * h.dist);
    const qualScore = Math.min(1, h.qual + (h.nabh ? 0.04 : 0));

    let score = 0;
    let billLabel = "";
    let reasons = [];

    if (layer === "mild_opd") {
      const opdScore = Math.max(0.05, 1 - h.opd / 1200);
      const tierBonus = isPublicOrChar ? 0.28 : -0.22;
      score = wAff * (0.68 * opdScore + 0.32 * proxScore) + wQual * (0.55 * qualScore + 0.45 * proxScore) + tierBonus;
      billLabel = `₹${h.opd} OPD Fee`;
      if (isPublicOrChar) {
        reasons.push(`Low-cost routine OPD (₹${h.opd}) ideal for cough, cold & mild fever.`);
      } else {
        reasons.push(`Private OPD fee is ₹${h.opd} (PM-JAY does not cover routine OPD).`);
      }
      reasons.push(`Quick local access: ${h.dist} km away in ${h.city}.`);
    } else if (layer === "specialist_opd") {
      const opdScore = Math.max(0.05, 1 - h.opd / 1300);
      const contBonus = schemeOk ? 0.18 : 0;
      score = wAff * (0.65 * opdScore + 0.35 * proxScore) + wQual * (0.75 * qualScore + 0.25 * proxScore) + contBonus;
      billLabel = `₹${h.opd} Specialist OPD`;
      reasons.push(`${spec} specialist consultation fee: ₹${h.opd}.`);
      if (schemeOk) {
        reasons.push(`${scheme} empanelled: seamless cashless admission if doctor advises stay.`);
      }
      if (h.nabh) reasons.push("NABH Accredited diagnostic & specialist care.");
    } else {
      const estBill = schemeOk ? 0 : h.proc;
      const costScore = schemeOk ? 1.0 : Math.max(0.05, 1 - estBill / 260000);
      score = wAff * (0.75 * costScore + 0.25 * proxScore) + wQual * (0.80 * qualScore + 0.20 * proxScore);
      billLabel = schemeOk ? `₹0 Cashless (${scheme})` : `Est. ₹${estBill.toLocaleString("en-IN")}`;
      if (schemeOk) {
        reasons.push(`Free cashless admission & surgery under ${scheme} (₹0 hospital bill).`);
      } else if (scheme !== "None / Cash") {
        reasons.push(`Not empanelled under ${scheme}; cash estimate ₹${estBill.toLocaleString("en-IN")}.`);
      } else {
        reasons.push(`Transparent cash package estimate: ₹${estBill.toLocaleString("en-IN")}.`);
      }
      if (h.nabh) reasons.push("NABH Accredited inpatient & surgical facility.");
    }

    if (!hasSpec) score *= 0.5;
    score = Math.max(0.05, Math.min(0.99, score));
    return { ...h, score: Math.round(score * 100), billLabel, schemeOk, reasons };
  });

  scored.sort((a, b) => b.score - a.score);

  const displayList = state.showAllHospitals ? scored : scored.slice(0, 12);
  document.getElementById("hospListSub").textContent =
    `Showing ${displayList.length} of ${scored.length} matching hospitals in ${city === "All" ? "all 10 cities" : city} (${ALL_HOSPITALS.length} indexed in this layer)`;
  document.getElementById("btnToggleAllHosp").textContent =
    state.showAllHospitals ? "Show Top 12" : `Show All ${scored.length} Hospitals`;

  document.getElementById("hospitalCards").innerHTML = displayList.map(h => {
    const isSaved = state.savedHospitalIds.includes(h.id);
    return `
      <article class="hosp-card">
        <div>
          <div class="hosp-top">
            <div class="visual-thumb" title="Click to inspect facility" onclick="inspectHospital('${h.id}')">
              ${getHospitalSVG(h.cat)}
            </div>
            <div style="flex:1; min-width:0;">
              <h3 class="hosp-title">${h.name}</h3>
              <p class="hosp-meta">${h.city} • ${h.type} • ${h.dist} km away</p>
              <div class="tag-row">
                <span class="tag ${h.billLabel.includes("₹0") || h.opd <= 150 ? "tag-green" : "tag-amber"}">${h.billLabel}</span>
                ${h.nabh ? `<span class="tag tag-blue">NABH Certified</span>` : ""}
                <span class="tag tag-gray">${h.score}% Match</span>
              </div>
            </div>
          </div>
          <ul class="reason-list" style="margin-top:10px;">
            ${h.reasons.map(r => `<li>${r}</li>`).join("")}
          </ul>
        </div>
        <div class="card-actions">
          <button class="btn btn-sm" onclick="inspectHospital('${h.id}')">Inspect Facility</button>
          <button class="btn btn-sm ${isSaved ? "btn-saved" : "btn-primary"}" onclick="toggleSaveHospital('${h.id}')">
            ${isSaved ? "✓ Saved in Plan" : "+ Save Hospital"}
          </button>
        </div>
      </article>
    `;
  }).join("");
}

function toggleSaveHospital(id) {
  const idx = state.savedHospitalIds.indexOf(id);
  if (idx >= 0) {
    state.savedHospitalIds.splice(idx, 1);
    showToast("Hospital removed from Saved Plan");
  } else {
    state.savedHospitalIds.push(id);
    showToast("Hospital added to Saved Family Plan");
  }
  updateSavedBadge();
  renderHospitals();
}

function inspectHospital(id) {
  const h = ALL_HOSPITALS.find(x => x.id === id);
  if (!h) return;
  document.getElementById("inspectModalTitle").textContent = h.name;
  document.getElementById("inspectModalBody").innerHTML = `
    <div style="display:flex; gap:14px; align-items:center; margin-bottom:14px;">
      <div style="border:1px solid var(--border); border-radius:14px; padding:6px; background:#f8fafc;">${getHospitalSVG(h.cat)}</div>
      <div>
        <p style="font-size:0.86rem; color:var(--text-muted);">${h.city} • ${h.type} • ${h.dist} km away</p>
        <div class="tag-row">
          <span class="tag tag-green">OPD Fee: ₹${h.opd}</span>
          <span class="tag tag-blue">Quality Score: ${Math.round(h.qual * 100)}%</span>
          ${h.nabh ? `<span class="tag tag-green">NABH Accredited</span>` : `<span class="tag tag-gray">Govt Registered</span>`}
        </div>
      </div>
    </div>
    <p style="font-size:0.85rem; margin-bottom:8px;"><strong>Accepted Health Schemes:</strong> ${h.schemes.join(", ")}</p>
    <p style="font-size:0.85rem; margin-bottom:14px;"><strong>Available Departments:</strong> ${h.specs.join(", ")}</p>
    <div style="display:flex; flex-wrap:wrap; gap:8px;">
      <a href="https://www.google.com/maps/search/${encodeURIComponent(h.name + ' ' + h.city)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">Open Directions in Google Maps ↗</a>
      <a href="https://hem.nha.gov.in/search" target="_blank" rel="noopener noreferrer" class="btn btn-sm">Verify on Official NHA HEM Portal ↗</a>
    </div>
  `;
  document.getElementById("inspectModal").classList.add("open");
}

// ==================== TAB 2: MEDICINES & JAN AUSHADHI ====================
function renderIllnessPills() {
  const cats = ["All", "Fever & Pain", "Cough & Cold", "Stomach & Acidity", "Allergy", "BP & Heart", "Diabetes", "Vitamins & First Aid"];
  document.getElementById("illnessPills").innerHTML = cats.map(c => `
    <button class="pill ${state.medIllnessFilter === c ? "active" : ""}" onclick="setIllnessFilter('${c}')">
      ${c === "All" ? "All 100 Medicines" : c}
    </button>
  `).join("");
}

function setIllnessFilter(cat) {
  state.medIllnessFilter = cat;
  state.browseAllMeds = true;
  document.getElementById("btnBrowseAllMeds").textContent = "Show Selected Basket Only";
  renderIllnessPills();
  renderMedicines();
}

function toggleMedViewMode() {
  state.browseAllMeds = !state.browseAllMeds;
  document.getElementById("btnBrowseAllMeds").textContent = state.browseAllMeds
    ? `Show Selected Basket (${state.basketMedIds.length})`
    : "Browse All 100 Medicines";
  renderMedicines();
}

function loadSampleKit(kind) {
  state.basketMedIds = kind === "fever"
    ? ["MED-001", "MED-010", "MED-012", "MED-022", "MED-046"]
    : ["MED-034", "MED-036", "MED-041", "MED-045", "MED-049"];
  state.browseAllMeds = false;
  document.getElementById("btnBrowseAllMeds").textContent = "Browse All 100 Medicines";
  updateSavedBadge();
  renderMedicines();
  showToast(kind === "fever" ? "Loaded Fever & Cold Family Kit" : "Loaded BP & Diabetes Monthly Kit");
}

function renderMedicines() {
  let totalBrand = 0, totalGen = 0;
  state.basketMedIds.forEach(id => {
    const m = ALL_MEDICINES.find(x => x.id === id);
    if (m) { totalBrand += m.bMrp; totalGen += m.gMrp; }
  });
  const monthlySave = totalBrand - totalGen;
  const pct = totalBrand > 0 ? Math.round((monthlySave / totalBrand) * 100) : 0;

  document.getElementById("savingsBar").innerHTML = `
    <div class="sav-stat"><span>Selected Medicines</span><strong>${state.basketMedIds.length} Items</strong></div>
    <div class="sav-stat"><span>Private Branded Bill</span><strong>₹${totalBrand}</strong></div>
    <div class="sav-stat"><span>Jan Aushadhi Bill</span><strong>₹${totalGen}</strong></div>
    <div class="sav-stat"><span>Monthly Savings (${pct}%)</span><strong>₹${monthlySave} / mo</strong></div>
    <div class="sav-stat"><span>Yearly Family Savings</span><strong>₹${(monthlySave * 12).toLocaleString("en-IN")} / yr</strong></div>
  `;

  const query = document.getElementById("medSearchInput").value.trim().toLowerCase();
  const city = document.getElementById("selCity").value === "All" ? "India" : document.getElementById("selCity").value;

  let list = ALL_MEDICINES;
  if (query) {
    list = list.filter(m =>
      m.brand.toLowerCase().includes(query) ||
      m.salt.toLowerCase().includes(query) ||
      m.gName.toLowerCase().includes(query) ||
      m.cat.toLowerCase().includes(query)
    );
  } else if (!state.browseAllMeds && state.medIllnessFilter === "All") {
    const basketItems = ALL_MEDICINES.filter(m => state.basketMedIds.includes(m.id));
    const popularExtras = ALL_MEDICINES.filter(m => !state.basketMedIds.includes(m.id)).slice(0, 9);
    list = [...basketItems, ...popularExtras];
  } else if (state.medIllnessFilter !== "All") {
    list = list.filter(m => m.cat === state.medIllnessFilter);
  }

  document.getElementById("medicineCards").innerHTML = list.map(m => {
    const inBasket = state.basketMedIds.includes(m.id);
    const save = m.bMrp - m.gMrp;
    const savePct = Math.round((save / m.bMrp) * 100);
    const encodedSalt = encodeURIComponent(m.salt);
    const mapsUrl = `https://www.google.com/maps/search/Jan+Aushadhi+Kendra+${encodeURIComponent(city)}`;

    return `
      <article class="med-card ${inBasket ? "in-basket" : ""}">
        <div class="hosp-top">
          <div class="visual-thumb" title="Inspect Medicine & Salt" onclick="inspectMedicine('${m.id}')">
            ${getMedicineSVG(m.fmt)}
          </div>
          <div style="flex:1; min-width:0;">
            <div style="display:flex; justify-content:space-between; gap:6px; align-items:flex-start;">
              <h3 class="hosp-title">${m.brand}</h3>
              <span class="tag tag-green">Save ₹${save} (${savePct}%)</span>
            </div>
            <p class="hosp-meta">${m.cat} • ${m.fmt} (${m.pack})</p>
            <div class="tag-row">
              <span class="tag tag-blue">${m.gCode}</span>
              <span class="tag tag-gray">${m.gName}</span>
            </div>
          </div>
        </div>

        <div class="salt-pill">Active Salt: ${m.salt}</div>

        <div class="price-compare">
          <div class="price-box">
            <span>Branded Shop MRP</span>
            <strong class="strike">₹${m.bMrp}</strong>
          </div>
          <div class="price-box">
            <span>Jan Aushadhi MRP</span>
            <strong style="color:var(--primary);">₹${m.gMrp}</strong>
          </div>
        </div>

        <div class="card-actions">
          <button class="btn btn-sm ${inBasket ? "btn-saved" : "btn-primary"}" onclick="toggleBasketMed('${m.id}')">
            ${inBasket ? "✓ Added to Slip" : "+ Add to Slip"}
          </button>
          <button class="btn btn-sm" onclick="inspectMedicine('${m.id}')">Inspect &amp; Buy</button>
          <button class="btn btn-sm" onclick="copySingleMedSlip('${m.id}')">Copy Slip</button>
        </div>

        <div class="link-grid">
          <a href="${mapsUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-sm">Nearest Jan Aushadhi ↗</a>
          <a href="https://janaushadhi.gov.in/" target="_blank" rel="noopener noreferrer" class="btn btn-sm">Govt PMBI Portal ↗</a>
          <a href="https://www.1mg.com/search/all?name=${encodedSalt}" target="_blank" rel="noopener noreferrer" class="btn btn-sm">Salt on Tata 1mg ↗</a>
          <a href="https://pharmeasy.in/search/all?name=${encodedSalt}" target="_blank" rel="noopener noreferrer" class="btn btn-sm">Salt on PharmEasy ↗</a>
        </div>
      </article>
    `;
  }).join("");
}

function toggleBasketMed(id) {
  const idx = state.basketMedIds.indexOf(id);
  if (idx >= 0) {
    state.basketMedIds.splice(idx, 1);
    showToast("Removed from Jan Aushadhi Slip");
  } else {
    state.basketMedIds.push(id);
    showToast("Added to Jan Aushadhi Slip");
  }
  updateSavedBadge();
  renderMedicines();
}

function copySingleMedSlip(id) {
  const m = ALL_MEDICINES.find(x => x.id === id);
  if (!m) return;
  const text = `Jan Aushadhi Generic Request:\n- Brand Prescribed: ${m.brand} (MRP ₹${m.bMrp})\n- Active Salt: ${m.salt}\n- Jan Aushadhi Code: ${m.gCode} (${m.gName})\n- Govt Generic MRP: ₹${m.gMrp} (Saves ₹${m.bMrp - m.gMrp})`;
  copyTextFallback(text, "Copied pharmacist slip for " + m.brand);
}

function inspectMedicine(id) {
  const m = ALL_MEDICINES.find(x => x.id === id);
  if (!m) return;
  const city = document.getElementById("selCity").value === "All" ? "India" : document.getElementById("selCity").value;
  const encodedSalt = encodeURIComponent(m.salt);
  document.getElementById("inspectModalTitle").textContent = `${m.brand} → ${m.gCode}`;
  document.getElementById("inspectModalBody").innerHTML = `
    <div style="display:flex; gap:14px; align-items:center; margin-bottom:14px;">
      <div style="border:1px solid var(--border); border-radius:14px; padding:6px; background:#f8fafc;">${getMedicineSVG(m.fmt)}</div>
      <div>
        <p style="font-size:0.9rem; font-weight:800;">${m.gName}</p>
        <p style="font-size:0.82rem; color:var(--text-muted);">${m.fmt} • Pack Size: ${m.pack}</p>
        <div class="tag-row">
          <span class="tag tag-green">Govt MRP: ₹${m.gMrp} (vs ₹${m.bMrp})</span>
          <span class="tag tag-blue">WHO-GMP Certified</span>
        </div>
      </div>
    </div>
    <div class="salt-pill" style="margin-bottom:14px;">Exact Chemical Composition: ${m.salt}</div>
    <p style="font-size:0.82rem; color:var(--text-muted); margin-bottom:14px;">
      Show product code <strong>${m.gCode}</strong> at any Pradhan Mantri Bhartiya Janaushadhi Kendra or search the exact salt online:
    </p>
    <div class="link-grid">
      <a href="https://www.google.com/maps/search/Jan+Aushadhi+Kendra+${encodeURIComponent(city)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">Find Nearest Kendra (Maps) ↗</a>
      <a href="https://janaushadhi.gov.in/" target="_blank" rel="noopener noreferrer" class="btn btn-sm">Official PMBI Portal ↗</a>
      <a href="https://www.1mg.com/search/all?name=${encodedSalt}" target="_blank" rel="noopener noreferrer" class="btn btn-sm">Buy Salt on Tata 1mg ↗</a>
      <a href="https://pharmeasy.in/search/all?name=${encodedSalt}" target="_blank" rel="noopener noreferrer" class="btn btn-sm">Buy Salt on PharmEasy ↗</a>
    </div>
  `;
  document.getElementById("inspectModal").classList.add("open");
}

// ==================== TAB 3: SCAN PRESCRIPTION ====================
function fillSampleRx(type) {
  document.getElementById("rxTextInput").value = type === "fever"
    ? "Rx:\n1. Tab Dolo 650mg - 1 tab SOS for fever\n2. Tab Sinarest New - 1 tab twice daily x 3 days\n3. Cap Pan-D - 1 cap empty stomach morning\n4. Syrup Benadryl Cough Formula - 5ml thrice daily\n5. Tab Limcee 500mg - 1 daily"
    : "Rx (Chronic Care):\n1. Tab Telma-H 40mg - 1 tab morning after breakfast\n2. Tab Atorva 10mg - 1 tab at night\n3. Tab Amaryl M1 - 1 tab before breakfast\n4. Tab Shelcal 500 - 1 tab after lunch";
  scanPrescriptionText();
}

function handleRxPhoto(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  const box = document.getElementById("rxPhotoPreviewBox");
  const img = document.getElementById("rxPhotoImg");
  const cap = document.getElementById("rxPhotoCaption");
  img.src = URL.createObjectURL(file);
  box.style.display = "block";
  cap.textContent = `Uploaded: ${file.name} — Verify or edit detected medicine names below:`;
  if (!document.getElementById("rxTextInput").value.trim()) {
    fillSampleRx("fever");
  }
}

async function scanPrescriptionText() {
  const text = document.getElementById("rxTextInput").value;
  if (!text.trim()) {
    showToast("Please paste prescription text or click a sample button first.");
    return;
  }

  let matched = [];
  try {
    const res = await fetch(`${API_BASE}/api/scan-prescription`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    matched = data.matched || [];
  } catch (e) {
    const raw = text.toLowerCase();
    matched = ALL_MEDICINES.filter(m => {
      const firstWord = m.brand.toLowerCase().split(/[\s-(]/)[0];
      return raw.includes(m.brand.toLowerCase()) || (firstWord.length >= 4 && raw.includes(firstWord));
    });
  }

  const out = document.getElementById("scanResultsBox");
  if (matched.length === 0) {
    out.innerHTML = `<div class="card"><p style="font-size:0.88rem; color:var(--text-muted);">No exact brand names matched in the text. Try typing common names like <strong>Dolo 650, Augmentin, Pantocid, Sinarest, Telma-H, or Amaryl</strong>.</p></div>`;
    return;
  }

  const bSum = matched.reduce((s, m) => s + m.bMrp, 0);
  const gSum = matched.reduce((s, m) => s + m.gMrp, 0);
  window._lastScannedIds = matched.map(m => m.id);

  out.innerHTML = `
    <div class="card" style="border:2px solid var(--primary);">
      <div class="list-header">
        <div>
          <h3 class="section-title">Found ${matched.length} Medicines in Prescription</h3>
          <p class="section-sub" style="margin-bottom:0;">Branded Total: <strong>₹${bSum}</strong> → Jan Aushadhi Total: <strong style="color:var(--primary);">₹${gSum}</strong> (Save <strong>₹${bSum - gSum}</strong>)</p>
        </div>
        <button class="btn btn-primary" onclick="loadScannedIntoBasket()">Load All ${matched.length} into Medicine Basket</button>
      </div>
      <div style="display:flex; flex-direction:column; gap:10px; margin-top:12px;">
        ${matched.map(m => `
          <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:10px; padding:10px 12px; background:#f8fafc; border:1px solid var(--border); border-radius:10px;">
            <div>
              <strong>${m.brand}</strong> <span class="strike" style="font-size:0.82rem;">₹${m.bMrp}</span>
              → <strong style="color:var(--primary);">${m.gCode}: ${m.gName} (₹${m.gMrp})</strong>
              <div style="font-size:0.78rem; color:#1e40af;">Salt: ${m.salt}</div>
            </div>
            <span class="tag tag-green">Save ₹${m.bMrp - m.gMrp}</span>
          </div>
        `).join("")}
      </div>
    </div>
  `;
}

function loadScannedIntoBasket() {
  if (!window._lastScannedIds) return;
  state.basketMedIds = Array.from(new Set([...state.basketMedIds, ...window._lastScannedIds]));
  updateSavedBadge();
  renderMedicines();
  switchTab("medicines");
  showToast("All scanned medicines added to your Jan Aushadhi list!");
}

// ==================== TAB 4: SURGERY COST ESTIMATOR ====================
function renderSurgeryEstimator() {
  const pid = document.getElementById("selProcedure").value;
  const scheme = document.getElementById("selSurgScheme").value;
  const proc = PROCEDURES.find(p => p.id === pid) || PROCEDURES[0];
  const isCovered = scheme !== "None / Cash";

  document.getElementById("surgeryOutput").innerHTML = `
    <div class="surgery-grid">
      <div class="bill-card private">
        <span class="tag tag-amber">Without Health Card (Private Cash)</span>
        <h3 style="font-size:1.5rem; font-weight:800; color:#991b1b; margin:10px 0 4px;">₹${proc.priv.toLocaleString("en-IN")}</h3>
        <p style="font-size:0.83rem; color:#7f1d1d;">Includes surgeon fee, ICU/ward stay (${proc.stay}), implants, and discharge medicines paid out of pocket.</p>
      </div>
      <div class="bill-card covered">
        <span class="tag tag-green">${isCovered ? `With ${scheme} (Empanelled Hospital)` : "Tip: Apply for Ayushman Card"}</span>
        <h3 style="font-size:1.5rem; font-weight:800; color:#065f46; margin:10px 0 4px;">
          ${isCovered ? "₹0 Hospital Bill" : `₹${proc.priv.toLocaleString("en-IN")} Cash`}
        </h3>
        <p style="font-size:0.83rem; color:#064e3b;">
          ${isCovered
            ? `Govt package rate (₹${proc.pmjay.toLocaleString("en-IN")}) is 100% cashless. Also covers <strong>${proc.prePost}</strong>.`
            : `Eligible families save ₹${proc.priv.toLocaleString("en-IN")} by enrolling under Ayushman Bharat PM-JAY before planned admission.`}
        </p>
      </div>
    </div>
  `;
}

// ==================== TAB 5: VISIT CHECKLIST ====================
function renderChecklist() {
  const doneCount = Object.values(state.checkedDocs).filter(Boolean).length;
  const pct = Math.round((doneCount / CHECKLIST_DATA.length) * 100);
  document.getElementById("chkProgressLabel").textContent = `${doneCount} / ${CHECKLIST_DATA.length} Ready (${pct}%)`;
  document.getElementById("chkProgressFill").style.width = `${pct}%`;

  document.getElementById("checklistItems").innerHTML = CHECKLIST_DATA.map(item => {
    const checked = !!state.checkedDocs[item.id];
    return `
      <label class="check-item ${checked ? "checked" : ""}">
        <input type="checkbox" ${checked ? "checked" : ""} onchange="toggleCheckItem('${item.id}')" />
        <div>
          <div style="font-weight:800; font-size:0.9rem;">${item.title}</div>
          <div style="font-size:0.8rem; color:var(--text-muted); margin-top:2px;">${item.desc}</div>
        </div>
      </label>
    `;
  }).join("");
}

function toggleCheckItem(id) {
  state.checkedDocs[id] = !state.checkedDocs[id];
  renderChecklist();
}

// ==================== SAVED PLAN MODAL ====================
function updateSavedBadge() {
  document.getElementById("savedCountBadge").textContent = state.savedHospitalIds.length + state.basketMedIds.length;
}

function openSavedModal() {
  const savedHosps = ALL_HOSPITALS.filter(h => state.savedHospitalIds.includes(h.id));
  const savedMeds = ALL_MEDICINES.filter(m => state.basketMedIds.includes(m.id));
  const bTot = savedMeds.reduce((s, m) => s + m.bMrp, 0);
  const gTot = savedMeds.reduce((s, m) => s + m.gMrp, 0);

  document.getElementById("savedModalBody").innerHTML = `
    <div style="background:#f0fdf4; border:1px solid #bbf7d0; padding:12px; border-radius:10px; margin-bottom:14px; font-size:0.83rem;">
      <strong>Official Toll-Free Helplines:</strong><br/>
      - Ayushman Bharat (PM-JAY) 24×7 Helpline: <strong>14555</strong><br/>
      - Jan Aushadhi Kendra &amp; Medicine Helpline: <strong>1800-180-8080</strong>
    </div>

    <h4 style="font-size:0.92rem; font-weight:800; margin-bottom:6px;">Saved Hospitals (${savedHosps.length})</h4>
    ${savedHosps.length === 0 ? `<p style="font-size:0.82rem; color:var(--text-muted); margin-bottom:12px;">No hospitals saved yet.</p>` : `
      <ul style="list-style:none; display:flex; flex-direction:column; gap:6px; margin-bottom:14px;">
        ${savedHosps.map(h => `
          <li style="padding:8px 10px; border:1px solid var(--border); border-radius:8px; font-size:0.83rem;">
            <strong>${h.name}</strong> (${h.city} • ${h.dist} km) — OPD: ₹${h.opd} | Schemes: ${h.schemes.join(", ")}
          </li>
        `).join("")}
      </ul>
    `}

    <h4 style="font-size:0.92rem; font-weight:800; margin-bottom:6px;">Jan Aushadhi Generic Pharmacy List (${savedMeds.length})</h4>
    ${savedMeds.length === 0 ? `<p style="font-size:0.82rem; color:var(--text-muted);">No medicines in slip yet.</p>` : `
      <ul style="list-style:none; display:flex; flex-direction:column; gap:6px; margin-bottom:12px;">
        ${savedMeds.map(m => `
          <li style="padding:8px 10px; border:1px solid var(--border); border-radius:8px; font-size:0.82rem;">
            <strong>${m.gCode} — ${m.gName}</strong> (Generic MRP: ₹${m.gMrp})<br/>
            <span style="color:var(--text-muted);">Replaces: ${m.brand} (₹${m.bMrp}) • Salt: ${m.salt}</span>
          </li>
        `).join("")}
      </ul>
      <div style="font-weight:800; font-size:0.92rem; color:var(--primary);">
        Total Jan Aushadhi Bill: ₹${gTot} (You Save ₹${bTot - gTot} per refill!)
      </div>
    `}
  `;
  document.getElementById("savedModal").classList.add("open");
}

function closeSavedModal() { document.getElementById("savedModal").classList.remove("open"); }
function closeInspectModal() { document.getElementById("inspectModal").classList.remove("open"); }

function copySavedPlan() {
  const savedHosps = ALL_HOSPITALS.filter(h => state.savedHospitalIds.includes(h.id));
  const savedMeds = ALL_MEDICINES.filter(m => state.basketMedIds.includes(m.id));
  const lines = [
    "=== ArogyaNav Family Care & Jan Aushadhi Slip ===",
    "Hospitals:",
    ...savedHosps.map(h => `- ${h.name} (${h.city}, ${h.dist} km) | Schemes: ${h.schemes.join(", ")}`),
    "\nJan Aushadhi Medicines:",
    ...savedMeds.map(m => `- [${m.gCode}] ${m.gName} (₹${m.gMrp}) | Salt: ${m.salt} | Replaces ${m.brand} (₹${m.bMrp})`),
    "\nHelplines: PM-JAY 14555 | Jan Aushadhi 1800-180-8080"
  ];
  copyTextFallback(lines.join("\n"), "Copied complete Family Care & Pharmacy Slip!");
}

// ==================== VIVA KNOWLEDGE GRAPH VISUALIZER ====================
function renderVivaGraph() {
  const id = document.getElementById("vivaDrugSelect").value;
  const m = ALL_MEDICINES.find(x => x.id === id) || ALL_MEDICINES[0];
  if (!m) return;
  document.getElementById("vivaGraphBox").innerHTML = `
    <div class="kg-node" style="background:#fee2e2; color:#991b1b; border:1px solid #fca5a5;">
      Branded Node<br/>${m.brand}<br/><small>MRP ₹${m.bMrp}</small>
    </div>
    <span style="font-weight:800; color:#475569;">── HAS_ACTIVE_SALT ──▶</span>
    <div class="kg-node" style="background:#dbeafe; color:#1e40af; border:1px solid #93c5fd;">
      Chemical Salt Entity<br/>${m.salt}
    </div>
    <span style="font-weight:800; color:#475569;">── BIO_EQUIVALENT_TO ──▶</span>
    <div class="kg-node" style="background:#dcfce7; color:#166534; border:1px solid #86efac;">
      PMBJP Generic Node<br/>${m.gCode}: ${m.gName}<br/><small>Govt MRP ₹${m.gMrp} (-${Math.round(((m.bMrp - m.gMrp) / m.bMrp) * 100)}%)</small>
    </div>
  `;
}

function copyTextFallback(text, msg) {
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.style.position = "fixed";
  ta.style.opacity = "0";
  document.body.appendChild(ta);
  ta.select();
  try {
    document.execCommand("copy");
    showToast(msg);
  } catch (e) {
    showToast("Unable to copy automatically");
  }
  document.body.removeChild(ta);
}

window.onload = init;