import json
import sqlite3
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = Path(__file__).resolve().parent / "arogyanav.db"

app = FastAPI(title="ArogyaNav AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CITIES = [
    "Gaya", "Patna", "Durgapur", "Kolkata", "Asansol",
    "Ranchi", "Jamshedpur", "Varanasi", "Lucknow", "Delhi NCR",
]

SPECIALTIES = [
    "General Medicine", "Cardiology", "Orthopaedics", "Diabetology",
    "Ophthalmology", "Obstetrics & Gynaecology", "Oncology",
    "Nephrology", "Neurology", "Pulmonology",
]

BASE_HOSPITALS = [
    {"name": "Anugrah Narayan Magadh Medical College (ANMMCH)", "city": "Gaya", "type": "Public / Government", "cat": "govt", "nabh": True, "dist": 3.8, "opd": 10, "proc": 25000, "qual": 0.86, "specs": ["General Medicine", "Cardiology", "Orthopaedics", "Obstetrics & Gynaecology", "Pulmonology"], "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"name": "Manpur Primary & Referral Health Polyclinic", "city": "Gaya", "type": "Public / Government", "cat": "polyclinic", "nabh": False, "dist": 1.4, "opd": 10, "proc": 8000, "qual": 0.79, "specs": ["General Medicine", "Diabetology", "Pulmonology", "Obstetrics & Gynaecology"], "schemes": ["PM-JAY", "State Health Card"]},
    {"name": "Bodhgaya Charitable Eye & General Hospital", "city": "Gaya", "type": "Charitable Non-Profit", "cat": "charitable", "nabh": True, "dist": 7.2, "opd": 100, "proc": 18000, "qual": 0.91, "specs": ["Ophthalmology", "General Medicine", "Diabetology"], "schemes": ["PM-JAY", "State Health Card"]},
    {"name": "Magadh Heart & Critical Care Institute", "city": "Gaya", "type": "Private Empanelled", "cat": "private", "nabh": True, "dist": 3.5, "opd": 500, "proc": 120000, "qual": 0.89, "specs": ["Cardiology", "Pulmonology", "General Medicine"], "schemes": ["PM-JAY", "ESIC / CGHS"]},
    {"name": "Indira Gandhi Institute of Medical Sciences (IGIMS)", "city": "Patna", "type": "Public / Autonomous", "cat": "govt", "nabh": True, "dist": 4.8, "opd": 50, "proc": 35000, "qual": 0.94, "specs": ["Cardiology", "Oncology", "Nephrology", "Neurology", "General Medicine"], "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"name": "Mahavir Cancer Sansthan & Research Centre", "city": "Patna", "type": "Charitable Non-Profit", "cat": "charitable", "nabh": True, "dist": 6.1, "opd": 100, "proc": 65000, "qual": 0.93, "specs": ["Oncology", "General Medicine"], "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"name": "Paras HMRI Superspeciality Hospital", "city": "Patna", "type": "Private Corporate", "cat": "private", "nabh": True, "dist": 4.3, "opd": 1000, "proc": 230000, "qual": 0.95, "specs": ["Cardiology", "Neurology", "Orthopaedics", "Oncology"], "schemes": ["ESIC / CGHS"]},
    {"name": "District Sadar & PM-JAY Referral Hospital", "city": "Durgapur", "type": "Public / Government", "cat": "govt", "nabh": True, "dist": 3.2, "opd": 20, "proc": 30000, "qual": 0.85, "specs": ["General Medicine", "Cardiology", "Orthopaedics", "Diabetology"], "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"name": "Vivekananda Mission Charitable Multispeciality", "city": "Durgapur", "type": "Charitable Non-Profit", "cat": "charitable", "nabh": True, "dist": 4.9, "opd": 200, "proc": 75000, "qual": 0.91, "specs": ["Cardiology", "Orthopaedics", "Neurology", "Diabetology", "General Medicine"], "schemes": ["PM-JAY", "State Health Card"]},
    {"name": "S.S.K.M. (IPGMER) Government Referral Hospital", "city": "Kolkata", "type": "Public / Government", "cat": "govt", "nabh": True, "dist": 4.0, "opd": 10, "proc": 20000, "qual": 0.93, "specs": ["Cardiology", "Neurology", "Nephrology", "Diabetology", "General Medicine"], "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"name": "Ramakrishna Mission Seva Pratishthan", "city": "Kolkata", "type": "Charitable Non-Profit", "cat": "charitable", "nabh": True, "dist": 3.1, "opd": 150, "proc": 48000, "qual": 0.92, "specs": ["General Medicine", "Orthopaedics", "Obstetrics & Gynaecology", "Ophthalmology"], "schemes": ["PM-JAY", "State Health Card"]},
    {"name": "Sankara Nethralaya Eye Care Centre", "city": "Kolkata", "type": "Charitable Non-Profit", "cat": "charitable", "nabh": True, "dist": 5.8, "opd": 250, "proc": 26000, "qual": 0.96, "specs": ["Ophthalmology"], "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"name": "ESIC Model Hospital & Urban Polyclinic", "city": "Asansol", "type": "Public / ESIC", "cat": "polyclinic", "nabh": True, "dist": 2.9, "opd": 20, "proc": 28000, "qual": 0.84, "specs": ["General Medicine", "Orthopaedics", "Pulmonology", "Diabetology"], "schemes": ["ESIC / CGHS", "PM-JAY"]},
    {"name": "Rajendra Institute of Medical Sciences (RIMS)", "city": "Ranchi", "type": "Public / Autonomous", "cat": "govt", "nabh": True, "dist": 4.5, "opd": 20, "proc": 30000, "qual": 0.89, "specs": ["Cardiology", "Neurology", "Oncology", "Orthopaedics", "General Medicine"], "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"name": "Tata Main Hospital (TMH)", "city": "Jamshedpur", "type": "Trust / Corporate", "cat": "charitable", "nabh": True, "dist": 3.1, "opd": 550, "proc": 135000, "qual": 0.95, "specs": ["Cardiology", "General Medicine", "Orthopaedics", "Oncology"], "schemes": ["ESIC / CGHS", "PM-JAY"]},
    {"name": "Sir Sunderlal Hospital (IMS-BHU)", "city": "Varanasi", "type": "Public / Central Govt", "cat": "govt", "nabh": True, "dist": 4.2, "opd": 20, "proc": 25000, "qual": 0.94, "specs": ["Cardiology", "Oncology", "Neurology", "Nephrology", "General Medicine", "Ophthalmology"], "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"name": "King George's Medical University (KGMU)", "city": "Lucknow", "type": "Public / Government", "cat": "govt", "nabh": True, "dist": 3.9, "opd": 10, "proc": 22000, "qual": 0.94, "specs": ["Cardiology", "Orthopaedics", "Neurology", "Obstetrics & Gynaecology", "General Medicine"], "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"name": "Safdarjung & VMMC Central Govt Hospital", "city": "Delhi NCR", "type": "Public / Central Govt", "cat": "govt", "nabh": True, "dist": 4.4, "opd": 10, "proc": 18000, "qual": 0.93, "specs": ["General Medicine", "Cardiology", "Orthopaedics", "Pulmonology", "Obstetrics & Gynaecology"], "schemes": ["PM-JAY", "ESIC / CGHS"]},
]

TEMPLATES = [
    {"suffix": "Urban Mohalla Polyclinic", "type": "Public / Government", "cat": "polyclinic", "nabh": False, "opd": 10, "proc": 12000, "qual": 0.80, "schemes": ["PM-JAY", "State Health Card"]},
    {"suffix": "District Sadar Referral Hospital", "type": "Public / Government", "cat": "govt", "nabh": True, "opd": 20, "proc": 28000, "qual": 0.86, "schemes": ["PM-JAY", "State Health Card", "ESIC / CGHS"]},
    {"suffix": "Seva Mission Charitable Hospital", "type": "Charitable Non-Profit", "cat": "charitable", "nabh": True, "opd": 150, "proc": 55000, "qual": 0.90, "schemes": ["PM-JAY", "State Health Card"]},
    {"suffix": "Heart, Ortho & Trauma Care Centre", "type": "Private Empanelled", "cat": "private", "nabh": True, "opd": 600, "proc": 130000, "qual": 0.89, "schemes": ["PM-JAY", "ESIC / CGHS"]},
    {"suffix": "Mother, Child & Eye Care Institute", "type": "Private Empanelled", "cat": "private", "nabh": True, "opd": 450, "proc": 65000, "qual": 0.91, "schemes": ["PM-JAY", "State Health Card"]},
    {"suffix": "Nephro, Neuro & Urology Superspeciality", "type": "Private Empanelled", "cat": "private", "nabh": True, "opd": 750, "proc": 165000, "qual": 0.92, "schemes": ["PM-JAY", "ESIC / CGHS"]},
    {"suffix": "Metro Corporate Multispeciality", "type": "Private Corporate", "cat": "private", "nabh": True, "opd": 1100, "proc": 245000, "qual": 0.96, "schemes": ["ESIC / CGHS"]},
    {"suffix": "ESIC & Labour Welfare Dispensary", "type": "Public / ESIC", "cat": "polyclinic", "nabh": False, "opd": 20, "proc": 24000, "qual": 0.82, "schemes": ["ESIC / CGHS", "PM-JAY"]},
    {"suffix": "Lions Charitable Eye & Diabetes Clinic", "type": "Charitable Non-Profit", "cat": "charitable", "nabh": True, "opd": 120, "proc": 22000, "qual": 0.90, "schemes": ["PM-JAY", "State Health Card"]},
]

CORE_MEDICINES = [
    {"id": "MED-001", "brand": "Dolo 650", "salt": "Paracetamol 650mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 34, "gCode": "PMBJP-0201", "gName": "Paracetamol Tablets IP 650mg", "gMrp": 10, "pack": "15 Tablets"},
    {"id": "MED-002", "brand": "Crocin Advance 500", "salt": "Paracetamol 500mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 22, "gCode": "PMBJP-0200", "gName": "Paracetamol Tablets IP 500mg", "gMrp": 7, "pack": "15 Tablets"},
    {"id": "MED-003", "brand": "Calpol 650", "salt": "Paracetamol 650mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 33, "gCode": "PMBJP-0201", "gName": "Paracetamol Tablets IP 650mg", "gMrp": 10, "pack": "15 Tablets"},
    {"id": "MED-004", "brand": "Combiflam", "salt": "Ibuprofen 400mg + Paracetamol 325mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 45, "gCode": "PMBJP-0204", "gName": "Ibuprofen & Paracetamol Tablets IP", "gMrp": 8, "pack": "10 Tablets"},
    {"id": "MED-005", "brand": "Saridon", "salt": "Paracetamol 250mg + Propyphenazone 150mg + Caffeine 50mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 44, "gCode": "PMBJP-0212", "gName": "Analgesic Headache Relief Tablets", "gMrp": 11, "pack": "10 Tablets"},
    {"id": "MED-006", "brand": "Meftal-Spas", "salt": "Mefenamic Acid 250mg + Dicyclomine 10mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 54, "gCode": "PMBJP-0718", "gName": "Mefenamic Acid & Dicyclomine Tablets", "gMrp": 12, "pack": "10 Tablets"},
    {"id": "MED-007", "brand": "Voveran SR 100", "salt": "Diclofenac Sodium 100mg SR", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 112, "gCode": "PMBJP-0731", "gName": "Diclofenac Prolonged Release Tablets 100mg", "gMrp": 14, "pack": "10 Tablets"},
    {"id": "MED-008", "brand": "Zerodol-SP", "salt": "Aceclofenac 100mg + Paracetamol 325mg + Serratiopeptidase 15mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 118, "gCode": "PMBJP-0744", "gName": "Aceclofenac, Paracetamol & Serratiopeptidase", "gMrp": 20, "pack": "10 Tablets"},
    {"id": "MED-009", "brand": "Volini Pain Relief Gel", "salt": "Diclofenac Diethylamine + Methyl Salicylate + Menthol", "cat": "Fever & Pain", "fmt": "Gel", "bMrp": 145, "gCode": "PMBJP-0752", "gName": "Diclofenac Pain Relief Gel 30g", "gMrp": 28, "pack": "30g Tube"},
    {"id": "MED-010", "brand": "Sinarest New", "salt": "Paracetamol 500mg + Phenylephrine 10mg + Chlorpheniramine 2mg", "cat": "Cough & Cold", "fmt": "Tablet", "bMrp": 72, "gCode": "PMBJP-0695", "gName": "Cold & Flu Relief Combination Tablets", "gMrp": 12, "pack": "10 Tablets"},
    {"id": "MED-011", "brand": "Cheston Cold", "salt": "Cetirizine 5mg + Phenylephrine 10mg + Paracetamol 325mg", "cat": "Cough & Cold", "fmt": "Tablet", "bMrp": 65, "gCode": "PMBJP-0696", "gName": "Anti-Cold Cetirizine Paracetamol Tablets", "gMrp": 11, "pack": "10 Tablets"},
    {"id": "MED-012", "brand": "Benadryl Cough Formula", "salt": "Diphenhydramine 14.08mg + Ammonium Chloride 138mg", "cat": "Cough & Cold", "fmt": "Syrup", "bMrp": 138, "gCode": "PMBJP-0670", "gName": "Diphenhydramine Cough Syrup 100ml", "gMrp": 26, "pack": "100ml Bottle"},
    {"id": "MED-013", "brand": "Ascoril LS Expectorant", "salt": "Levosalbutamol 1mg + Ambroxol 30mg + Guaiphenesin 50mg", "cat": "Cough & Cold", "fmt": "Syrup", "bMrp": 142, "gCode": "PMBJP-0674", "gName": "Ambroxol & Levosalbutamol Cough Syrup", "gMrp": 29, "pack": "100ml Bottle"},
    {"id": "MED-014", "brand": "Grilinctus-BM", "salt": "Terbutaline 2.5mg + Bromhexine 8mg", "cat": "Cough & Cold", "fmt": "Syrup", "bMrp": 128, "gCode": "PMBJP-0678", "gName": "Bromhexine & Terbutaline Syrup 100ml", "gMrp": 24, "pack": "100ml Bottle"},
    {"id": "MED-015", "brand": "Otrivin Oxy Nasal Drops", "salt": "Oxymetazoline Hydrochloride 0.05%", "cat": "Cough & Cold", "fmt": "Drops", "bMrp": 98, "gCode": "PMBJP-0699", "gName": "Oxymetazoline Nasal Solution 10ml", "gMrp": 18, "pack": "10ml Drops"},
    {"id": "MED-016", "brand": "Foracort 200 Inhaler", "salt": "Budesonide 200mcg + Formoterol 6mcg", "cat": "Cough & Cold", "fmt": "Inhaler", "bMrp": 485, "gCode": "PMBJP-1120", "gName": "Formoterol & Budesonide Inhaler 120 MDI", "gMrp": 160, "pack": "120 Doses"},
    {"id": "MED-017", "brand": "Allegra 120mg", "salt": "Fexofenadine Hydrochloride 120mg", "cat": "Allergy", "fmt": "Tablet", "bMrp": 218, "gCode": "PMBJP-0688", "gName": "Fexofenadine Hydrochloride Tablets IP 120mg", "gMrp": 28, "pack": "10 Tablets"},
    {"id": "MED-018", "brand": "Okacet (Cetirizine 10mg)", "salt": "Cetirizine Hydrochloride 10mg", "cat": "Allergy", "fmt": "Tablet", "bMrp": 22, "gCode": "PMBJP-0680", "gName": "Cetirizine Hydrochloride Tablets IP 10mg", "gMrp": 5, "pack": "10 Tablets"},
    {"id": "MED-019", "brand": "Avil 25", "salt": "Pheniramine Maleate 25mg", "cat": "Allergy", "fmt": "Tablet", "bMrp": 14, "gCode": "PMBJP-0681", "gName": "Pheniramine Maleate Tablets IP 25mg", "gMrp": 4, "pack": "15 Tablets"},
    {"id": "MED-020", "brand": "Montair-LC", "salt": "Montelukast 10mg + Levocetirizine 5mg", "cat": "Allergy", "fmt": "Tablet", "bMrp": 210, "gCode": "PMBJP-0682", "gName": "Montelukast & Levocetirizine Tablets IP", "gMrp": 19, "pack": "10 Tablets"},
    {"id": "MED-021", "brand": "Omez 20 Capsule", "salt": "Omeprazole 20mg", "cat": "Stomach & Acidity", "fmt": "Capsule", "bMrp": 64, "gCode": "PMBJP-0520", "gName": "Omeprazole Gastro-Resistant Capsules IP 20mg", "gMrp": 11, "pack": "15 Capsules"},
    {"id": "MED-022", "brand": "Pantocid 40", "salt": "Pantoprazole 40mg", "cat": "Stomach & Acidity", "fmt": "Tablet", "bMrp": 155, "gCode": "PMBJP-0529", "gName": "Pantoprazole Gastro-Resistant Tablets IP 40mg", "gMrp": 14, "pack": "10 Tablets"},
    {"id": "MED-023", "brand": "Pan-D Capsule", "salt": "Pantoprazole 40mg + Domperidone 30mg SR", "cat": "Stomach & Acidity", "fmt": "Capsule", "bMrp": 199, "gCode": "PMBJP-0532", "gName": "Pantoprazole & Domperidone SR Capsules", "gMrp": 24, "pack": "10 Capsules"},
    {"id": "MED-024", "brand": "Rantac 150", "salt": "Ranitidine 150mg", "cat": "Stomach & Acidity", "fmt": "Tablet", "bMrp": 42, "gCode": "PMBJP-0515", "gName": "Ranitidine Hydrochloride Tablets IP 150mg", "gMrp": 9, "pack": "30 Tablets"},
    {"id": "MED-025", "brand": "Digene Antacid Gel", "salt": "Magnesium Hydroxide + Simethicone + Aluminium Hydroxide", "cat": "Stomach & Acidity", "fmt": "Syrup", "bMrp": 148, "gCode": "PMBJP-0510", "gName": "Antacid & Anti-Gas Oral Suspension 200ml", "gMrp": 32, "pack": "200ml Bottle"},
    {"id": "MED-026", "brand": "Gelusil MPS Liquid", "salt": "Activated Dimethicone + Magnesium & Aluminium Hydroxide", "cat": "Stomach & Acidity", "fmt": "Syrup", "bMrp": 135, "gCode": "PMBJP-0511", "gName": "Simethicone Antacid Suspension 200ml", "gMrp": 30, "pack": "200ml Bottle"},
    {"id": "MED-027", "brand": "Norflox-TZ", "salt": "Norfloxacin 400mg + Tinidazole 600mg", "cat": "Stomach & Acidity", "fmt": "Tablet", "bMrp": 96, "gCode": "PMBJP-0148", "gName": "Norfloxacin & Tinidazole Tablets", "gMrp": 22, "pack": "10 Tablets"},
    {"id": "MED-028", "brand": "Eldoper Capsule", "salt": "Loperamide Hydrochloride 2mg", "cat": "Stomach & Acidity", "fmt": "Capsule", "bMrp": 32, "gCode": "PMBJP-0555", "gName": "Loperamide Capsules IP 2mg", "gMrp": 7, "pack": "10 Capsules"},
    {"id": "MED-029", "brand": "Electral ORS Powder", "salt": "Sodium Chloride + Potassium Chloride + Dextrose (WHO Formula)", "cat": "Stomach & Acidity", "fmt": "Sachet", "bMrp": 22, "gCode": "PMBJP-0560", "gName": "Oral Rehydration Salts IP (WHO Formula)", "gMrp": 6, "pack": "21.8g Sachet"},
    {"id": "MED-030", "brand": "Augmentin 625 Duo", "salt": "Amoxicillin 500mg + Clavulanic Acid 125mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 204, "gCode": "PMBJP-0115", "gName": "Amoxicillin & Potassium Clavulanate Tablets IP", "gMrp": 45, "pack": "10 Tablets"},
    {"id": "MED-031", "brand": "Azithral 500", "salt": "Azithromycin 500mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 132, "gCode": "PMBJP-0138", "gName": "Azithromycin Tablets IP 500mg", "gMrp": 35, "pack": "5 Tablets"},
    {"id": "MED-032", "brand": "Cifran 500", "salt": "Ciprofloxacin 500mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 48, "gCode": "PMBJP-0122", "gName": "Ciprofloxacin Tablets IP 500mg", "gMrp": 14, "pack": "10 Tablets"},
    {"id": "MED-033", "brand": "Taxim-O 200", "salt": "Cefixime 200mg", "cat": "Fever & Pain", "fmt": "Tablet", "bMrp": 116, "gCode": "PMBJP-0130", "gName": "Cefixime Tablets IP 200mg", "gMrp": 28, "pack": "10 Tablets"},
    {"id": "MED-034", "brand": "Telma-H 40mg", "salt": "Telmisartan 40mg + Hydrochlorothiazide 12.5mg", "cat": "BP & Heart", "fmt": "Tablet", "bMrp": 285, "gCode": "PMBJP-1042", "gName": "Telmisartan & Hydrochlorothiazide Tablets IP", "gMrp": 32, "pack": "10 Tablets"},
    {"id": "MED-035", "brand": "Stamlo 5", "salt": "Amlodipine 5mg", "cat": "BP & Heart", "fmt": "Tablet", "bMrp": 115, "gCode": "PMBJP-0311", "gName": "Amlodipine Tablets IP 5mg", "gMrp": 7, "pack": "10 Tablets"},
    {"id": "MED-036", "brand": "Atorva 10mg", "salt": "Atorvastatin 10mg", "cat": "BP & Heart", "fmt": "Tablet", "bMrp": 195, "gCode": "PMBJP-0418", "gName": "Atorvastatin Tablets IP 10mg", "gMrp": 18, "pack": "10 Tablets"},
    {"id": "MED-037", "brand": "Rosuvas 10", "salt": "Rosuvastatin 10mg", "cat": "BP & Heart", "fmt": "Tablet", "bMrp": 182, "gCode": "PMBJP-1019", "gName": "Rosuvastatin Tablets IP 10mg", "gMrp": 21, "pack": "10 Tablets"},
    {"id": "MED-038", "brand": "Ecosprin AV 75/10", "salt": "Aspirin 75mg + Atorvastatin 10mg", "cat": "BP & Heart", "fmt": "Capsule", "bMrp": 65, "gCode": "PMBJP-0954", "gName": "Atorvastatin & Aspirin Capsules", "gMrp": 14, "pack": "10 Capsules"},
    {"id": "MED-039", "brand": "Clopitab-A 75", "salt": "Clopidogrel 75mg + Aspirin 75mg", "cat": "BP & Heart", "fmt": "Tablet", "bMrp": 98, "gCode": "PMBJP-0961", "gName": "Clopidogrel & Aspirin Tablets IP", "gMrp": 16, "pack": "10 Tablets"},
    {"id": "MED-040", "brand": "Metolar XR 50", "salt": "Metoprolol Succinate 50mg ER", "cat": "BP & Heart", "fmt": "Tablet", "bMrp": 135, "gCode": "PMBJP-0348", "gName": "Metoprolol Succinate ER Tablets IP 50mg", "gMrp": 19, "pack": "10 Tablets"},
    {"id": "MED-041", "brand": "Amaryl M1", "salt": "Glimepiride 1mg + Metformin 500mg SR", "cat": "Diabetes", "fmt": "Tablet", "bMrp": 145, "gCode": "PMBJP-0891", "gName": "Glimepiride & Metformin Prolonged Release", "gMrp": 19, "pack": "10 Tablets"},
    {"id": "MED-042", "brand": "Glycomet-GP 1", "salt": "Glimepiride 1mg + Metformin 500mg", "cat": "Diabetes", "fmt": "Tablet", "bMrp": 95, "gCode": "PMBJP-0891", "gName": "Glimepiride & Metformin Prolonged Release", "gMrp": 18, "pack": "10 Tablets"},
    {"id": "MED-043", "brand": "Galvus Met 50/500", "salt": "Vildagliptin 50mg + Metformin 500mg", "cat": "Diabetes", "fmt": "Tablet", "bMrp": 245, "gCode": "PMBJP-1412", "gName": "Vildagliptin & Metformin Hydrochloride Tablets", "gMrp": 47, "pack": "10 Tablets"},
    {"id": "MED-044", "brand": "Janumet 50/500", "salt": "Sitagliptin 50mg + Metformin 500mg", "cat": "Diabetes", "fmt": "Tablet", "bMrp": 310, "gCode": "PMBJP-1508", "gName": "Sitagliptin & Metformin Hydrochloride Tablets", "gMrp": 58, "pack": "10 Tablets"},
    {"id": "MED-045", "brand": "Thyronorm 50mcg", "salt": "Levothyroxine Sodium 50mcg", "cat": "Diabetes", "fmt": "Tablet", "bMrp": 160, "gCode": "PMBJP-0590", "gName": "Thyroxine Sodium Tablets IP 50mcg", "gMrp": 24, "pack": "100 Tablets"},
    {"id": "MED-046", "brand": "Limcee 500mg Chewable", "salt": "Ascorbic Acid (Vitamin C) 500mg", "cat": "Vitamins & First Aid", "fmt": "Tablet", "bMrp": 25, "gCode": "PMBJP-0601", "gName": "Vitamin C Chewable Tablets 500mg", "gMrp": 8, "pack": "15 Tablets"},
    {"id": "MED-047", "brand": "Zincovit Tablet", "salt": "Multivitamins + Multiminerals + Grape Seed Extract", "cat": "Vitamins & First Aid", "fmt": "Tablet", "bMrp": 110, "gCode": "PMBJP-0608", "gName": "Multivitamin & Multimineral Tablets", "gMrp": 18, "pack": "15 Tablets"},
    {"id": "MED-048", "brand": "Becosules Z Capsule", "salt": "Vitamin B-Complex + Vitamin C + Zinc", "cat": "Vitamins & First Aid", "fmt": "Capsule", "bMrp": 55, "gCode": "PMBJP-0605", "gName": "Vitamin B Complex with Vitamin C Capsules", "gMrp": 12, "pack": "20 Capsules"},
    {"id": "MED-049", "brand": "Shelcal 500", "salt": "Elemental Calcium 500mg + Vitamin D3 250 IU", "cat": "Vitamins & First Aid", "fmt": "Tablet", "bMrp": 144, "gCode": "PMBJP-0612", "gName": "Calcium Carbonate & Vitamin D3 Tablets IP", "gMrp": 18, "pack": "15 Tablets"},
    {"id": "MED-050", "brand": "Uprise-D3 60K", "salt": "Cholecalciferol 60000 IU", "cat": "Vitamins & First Aid", "fmt": "Capsule", "bMrp": 298, "gCode": "PMBJP-0634", "gName": "Cholecalciferol Softgel Capsules 60000 IU", "gMrp": 60, "pack": "4 Capsules"},
    {"id": "MED-051", "brand": "Neurobion Forte", "salt": "Vitamin B1 + B2 + B3 + B5 + B6 + B12", "cat": "Vitamins & First Aid", "fmt": "Tablet", "bMrp": 42, "gCode": "PMBJP-0605", "gName": "Vitamin B Complex with Vitamin B12 Tablets", "gMrp": 11, "pack": "30 Tablets"},
    {"id": "MED-052", "brand": "Betadine 5% Ointment", "salt": "Povidone-Iodine 5% w/w", "cat": "Vitamins & First Aid", "fmt": "Gel", "bMrp": 115, "gCode": "PMBJP-0910", "gName": "Povidone Iodine Antiseptic Ointment 20g", "gMrp": 22, "pack": "20g Tube"},
]

EXTRA_MEDS = [
    ("Calpol 500", "Paracetamol 500mg", "Fever & Pain", "Tablet", 16, "PMBJP-0200", "Paracetamol Tablets IP 500mg", 6, "15 Tablets"),
    ("Sumo Tablet", "Nimesulide 100mg + Paracetamol 325mg", "Fever & Pain", "Tablet", 125, "PMBJP-0218", "Nimesulide & Paracetamol Tablets", 16, "15 Tablets"),
    ("Disprin Regular", "Aspirin 350mg", "Fever & Pain", "Tablet", 15, "PMBJP-0208", "Acetylsalicylic Acid Soluble Tablets", 5, "10 Tablets"),
    ("Brufen 400", "Ibuprofen 400mg", "Fever & Pain", "Tablet", 24, "PMBJP-0203", "Ibuprofen Tablets IP 400mg", 7, "15 Tablets"),
    ("Flexon Tablet", "Ibuprofen 400mg + Paracetamol 325mg", "Fever & Pain", "Tablet", 30, "PMBJP-0204", "Ibuprofen & Paracetamol Tablets IP", 8, "15 Tablets"),
    ("Diclomol Tablet", "Diclofenac 50mg + Paracetamol 325mg", "Fever & Pain", "Tablet", 78, "PMBJP-0735", "Diclofenac & Paracetamol Tablets", 11, "15 Tablets"),
    ("Ultracet Tablet", "Tramadol 37.5mg + Paracetamol 325mg", "Fever & Pain", "Tablet", 185, "PMBJP-0760", "Tramadol & Paracetamol Tablets", 26, "15 Tablets"),
    ("Alex Cough Syrup", "Phenylephrine 5mg + Chlorpheniramine 2mg + Dextromethorphan 10mg", "Cough & Cold", "Syrup", 136, "PMBJP-0672", "Dextromethorphan Dry Cough Syrup 100ml", 25, "100ml Bottle"),
    ("TusQ-DX Syrup", "Dextromethorphan 10mg + Chlorpheniramine 2mg", "Cough & Cold", "Syrup", 118, "PMBJP-0672", "Dextromethorphan Cough Syrup 100ml", 24, "100ml Bottle"),
    ("Mucolite Syrup", "Ambroxol Hydrochloride 30mg/5ml", "Cough & Cold", "Syrup", 98, "PMBJP-0675", "Ambroxol Oral Liquid 100ml", 19, "100ml Bottle"),
    ("Asthalin Inhaler", "Salbutamol 100mcg", "Cough & Cold", "Inhaler", 165, "PMBJP-1110", "Salbutamol Inhaler IP 200 MDI", 58, "200 Doses"),
    ("Budecort 200 Inhaler", "Budesonide 200mcg", "Cough & Cold", "Inhaler", 365, "PMBJP-1115", "Budesonide Inhaler 200mcg", 115, "200 Doses"),
    ("Deriphyllin Retard 150", "Etofylline 115mg + Theophylline 35mg", "Cough & Cold", "Tablet", 32, "PMBJP-1104", "Etofylline & Theophylline Tablets", 9, "30 Tablets"),
    ("Zyrtec 10mg", "Cetirizine Hydrochloride 10mg", "Allergy", "Tablet", 42, "PMBJP-0680", "Cetirizine Tablets IP 10mg", 5, "10 Tablets"),
    ("Levocet 5mg", "Levocetirizine Hydrochloride 5mg", "Allergy", "Tablet", 68, "PMBJP-0684", "Levocetirizine Tablets IP 5mg", 7, "10 Tablets"),
    ("Atarax 25mg", "Hydroxyzine Hydrochloride 25mg", "Allergy", "Tablet", 92, "PMBJP-0690", "Hydroxyzine Tablets IP 25mg", 14, "15 Tablets"),
    ("Omnacortil 10", "Prednisolone 10mg", "Allergy", "Tablet", 16, "PMBJP-0480", "Prednisolone Tablets IP 10mg", 6, "10 Tablets"),
    ("Razo-D Capsule", "Rabeprazole 20mg + Domperidone 30mg SR", "Stomach & Acidity", "Capsule", 235, "PMBJP-0541", "Rabeprazole & Domperidone SR Capsules", 38, "10 Capsules"),
    ("Rablet 20", "Rabeprazole Sodium 20mg", "Stomach & Acidity", "Tablet", 148, "PMBJP-0538", "Rabeprazole Gastro-Resistant Tablets 20mg", 15, "10 Tablets"),
    ("Sompraz 40", "Esomeprazole 40mg", "Stomach & Acidity", "Tablet", 178, "PMBJP-0545", "Esomeprazole Tablets IP 40mg", 22, "10 Tablets"),
    ("Sucrafil O Gel", "Sucralfate 1g + Oxetacaine 20mg", "Stomach & Acidity", "Syrup", 215, "PMBJP-0548", "Sucralfate & Oxetacaine Suspension 200ml", 45, "200ml Bottle"),
    ("Cremaffin Plus", "Liquid Paraffin + Milk of Magnesia + Sodium Picosulfate", "Stomach & Acidity", "Syrup", 240, "PMBJP-0565", "Laxative Oral Emulsion 200ml", 48, "200ml Bottle"),
    ("Dulcoflex 5mg", "Bisacodyl 5mg", "Stomach & Acidity", "Tablet", 15, "PMBJP-0568", "Bisacodyl Gastro-Resistant Tablets 5mg", 4, "10 Tablets"),
    ("Sporlac DS", "Lactic Acid Bacillus 120 Million Spores", "Stomach & Acidity", "Tablet", 95, "PMBJP-0572", "Lactic Acid Bacillus Probiotic Tablets", 16, "15 Tablets"),
    ("Econorm 250mg", "Saccharomyces Boulardii 250mg", "Stomach & Acidity", "Sachet", 56, "PMBJP-0575", "Probiotic Anti-Diarrhoeal Sachet", 14, "1 Sachet"),
    ("Cyclopam Tablet", "Dicyclomine 20mg + Paracetamol 500mg", "Stomach & Acidity", "Tablet", 58, "PMBJP-0715", "Dicyclomine & Paracetamol Tablets", 10, "10 Tablets"),
    ("Telma 40", "Telmisartan 40mg", "BP & Heart", "Tablet", 230, "PMBJP-1040", "Telmisartan Tablets IP 40mg", 22, "15 Tablets"),
    ("Losar 50", "Losartan Potassium 50mg", "BP & Heart", "Tablet", 132, "PMBJP-1032", "Losartan Tablets IP 50mg", 14, "15 Tablets"),
    ("Olmezest 20", "Olmesartan Medoxomil 20mg", "BP & Heart", "Tablet", 185, "PMBJP-1048", "Olmesartan Tablets IP 20mg", 24, "10 Tablets"),
    ("Cilacar 10", "Cilnidipine 10mg", "BP & Heart", "Tablet", 168, "PMBJP-0322", "Cilnidipine Tablets IP 10mg", 19, "15 Tablets"),
    ("Concor 5", "Bisoprolol Fumarate 5mg", "BP & Heart", "Tablet", 142, "PMBJP-0352", "Bisoprolol Tablets IP 5mg", 18, "10 Tablets"),
    ("Lasix 40", "Furosemide 40mg", "BP & Heart", "Tablet", 18, "PMBJP-0381", "Furosemide Tablets IP 40mg", 5, "15 Tablets"),
    ("Dytor 10", "Torasemide 10mg", "BP & Heart", "Tablet", 88, "PMBJP-0385", "Torasemide Tablets IP 10mg", 14, "15 Tablets"),
    ("Ecosprin 75", "Aspirin 75mg Gastro-Resistant", "BP & Heart", "Tablet", 8, "PMBJP-0950", "Aspirin Gastro-Resistant Tablets 75mg", 3, "14 Tablets"),
    ("Glycomet 500 SR", "Metformin Hydrochloride 500mg SR", "Diabetes", "Tablet", 46, "PMBJP-0880", "Metformin Prolonged Release Tablets 500mg", 11, "20 Tablets"),
    ("Glycomet-GP 2", "Glimepiride 2mg + Metformin 500mg", "Diabetes", "Tablet", 135, "PMBJP-0892", "Glimepiride 2mg & Metformin 500mg Tablets", 24, "10 Tablets"),
    ("Vogliboz 0.3", "Voglibose 0.3mg", "Diabetes", "Tablet", 148, "PMBJP-0901", "Voglibose Tablets IP 0.3mg", 21, "10 Tablets"),
    ("Teneligliptin 20 (Teneza)", "Teneligliptin 20mg", "Diabetes", "Tablet", 145, "PMBJP-1420", "Teneligliptin Tablets IP 20mg", 22, "10 Tablets"),
    ("Istamet 50/500", "Sitagliptin 50mg + Metformin 500mg", "Diabetes", "Tablet", 295, "PMBJP-1508", "Sitagliptin & Metformin Tablets", 58, "10 Tablets"),
    ("Eltroxin 50mcg", "Levothyroxine Sodium 50mcg", "Diabetes", "Tablet", 155, "PMBJP-0590", "Thyroxine Sodium Tablets IP 50mcg", 24, "100 Tablets"),
    ("Evion 400", "Tocopheryl Acetate (Vitamin E) 400mg", "Vitamins & First Aid", "Capsule", 42, "PMBJP-0620", "Vitamin E Softgel Capsules 400mg", 12, "10 Capsules"),
    ("Supradyn Daily", "Multivitamin + Multiminerals + Trace Elements", "Vitamins & First Aid", "Tablet", 62, "PMBJP-0608", "Multivitamin & Multimineral Tablets", 18, "15 Tablets"),
    ("Autrin Capsule", "Ferrous Fumarate + Folic Acid + Vitamin B12", "Vitamins & First Aid", "Capsule", 158, "PMBJP-0640", "Iron, Folic Acid & B12 Capsules", 24, "30 Capsules"),
    ("Folvite 5mg", "Folic Acid 5mg", "Vitamins & First Aid", "Tablet", 78, "PMBJP-0644", "Folic Acid Tablets IP 5mg", 9, "45 Tablets"),
    ("Shelcal HD", "Elemental Calcium 500mg + Vitamin D3 500 IU", "Vitamins & First Aid", "Tablet", 156, "PMBJP-0614", "Calcium & Vitamin D3 500 IU Tablets", 21, "15 Tablets"),
    ("Soframycin Skin Cream", "Framycetin Sulphate 1% w/w", "Vitamins & First Aid", "Gel", 62, "PMBJP-0915", "Framycetin Skin Cream 30g", 16, "30g Tube"),
    ("Candid Clotrimazole Cream", "Clotrimazole 1% w/w", "Vitamins & First Aid", "Gel", 98, "PMBJP-0920", "Clotrimazole Antifungal Cream 30g", 18, "30g Tube"),
    ("Urimax 0.4 Capsule", "Tamsulosin Hydrochloride 0.4mg MR", "BP & Heart", "Capsule", 265, "PMBJP-0772", "Tamsulosin MR Capsules 0.4mg", 28, "10 Capsules"),
]


def build_100_hospitals() -> list[dict]:
    items = []
    for i, h in enumerate(BASE_HOSPITALS, start=1):
        items.append({"id": f"HOSP-{i:03d}", **h})
    t_cursor = 0
    while len(items) < 100:
        city = CITIES[t_cursor % len(CITIES)]
        tpl = TEMPLATES[t_cursor % len(TEMPLATES)]
        sector_num = (t_cursor // len(CITIES)) + 1
        items.append({
            "id": f"HOSP-{len(items) + 1:03d}",
            "name": f"{city} Sector-{sector_num} {tpl['suffix']}",
            "city": city,
            "type": tpl["type"],
            "cat": tpl["cat"],
            "nabh": tpl["nabh"],
            "dist": round(1.8 + ((t_cursor * 7) % 75) / 10, 1),
            "opd": tpl["opd"],
            "proc": tpl["proc"],
            "qual": tpl["qual"],
            "specs": list(SPECIALTIES),
            "schemes": list(tpl["schemes"]),
        })
        t_cursor += 1
    return items


def build_100_medicines() -> list[dict]:
    items = list(CORE_MEDICINES)
    for m in EXTRA_MEDS:
        items.append({
            "id": f"MED-{len(items) + 1:03d}",
            "brand": m[0],
            "salt": m[1],
            "cat": m[2],
            "fmt": m[3],
            "bMrp": m[4],
            "gCode": m[5],
            "gName": m[6],
            "gMrp": m[7],
            "pack": m[8],
        })
    return items


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS hospitals (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                type TEXT NOT NULL,
                cat TEXT NOT NULL,
                nabh INTEGER NOT NULL,
                dist REAL NOT NULL,
                opd INTEGER NOT NULL,
                proc INTEGER NOT NULL,
                qual REAL NOT NULL,
                specs_json TEXT NOT NULL,
                schemes_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS medicines (
                id TEXT PRIMARY KEY,
                brand TEXT NOT NULL,
                salt TEXT NOT NULL,
                cat TEXT NOT NULL,
                fmt TEXT NOT NULL,
                bMrp INTEGER NOT NULL,
                gCode TEXT NOT NULL,
                gName TEXT NOT NULL,
                gMrp INTEGER NOT NULL,
                pack TEXT NOT NULL
            )
            """
        )

        if conn.execute("SELECT COUNT(*) AS cnt FROM hospitals").fetchone()["cnt"] == 0:
            for h in build_100_hospitals():
                conn.execute(
                    """
                    INSERT INTO hospitals (
                        id, name, city, type, cat, nabh, dist, opd, proc, qual, specs_json, schemes_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        h["id"], h["name"], h["city"], h["type"], h["cat"],
                        1 if h["nabh"] else 0, h["dist"], h["opd"], h["proc"],
                        h["qual"], json.dumps(h["specs"]), json.dumps(h["schemes"]),
                    ),
                )

        if conn.execute("SELECT COUNT(*) AS cnt FROM medicines").fetchone()["cnt"] == 0:
            for m in build_100_medicines():
                conn.execute(
                    """
                    INSERT INTO medicines (
                        id, brand, salt, cat, fmt, bMrp, gCode, gName, gMrp, pack
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        m["id"], m["brand"], m["salt"], m["cat"], m["fmt"],
                        m["bMrp"], m["gCode"], m["gName"], m["gMrp"], m["pack"],
                    ),
                )


class PrescriptionInput(BaseModel):
    text: str


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def health_check():
    with get_connection() as conn:
        h_count = conn.execute("SELECT COUNT(*) AS cnt FROM hospitals").fetchone()["cnt"]
        m_count = conn.execute("SELECT COUNT(*) AS cnt FROM medicines").fetchone()["cnt"]
    return {
        "app": "ArogyaNav AI",
        "status": "Connected",
        "hospital_count": h_count,
        "medicine_count": m_count,
    }


@app.get("/api/hospitals")
def get_all_hospitals():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM hospitals ORDER BY id").fetchall()
    return [
        {
            "id": r["id"],
            "name": r["name"],
            "city": r["city"],
            "type": r["type"],
            "cat": r["cat"],
            "nabh": bool(r["nabh"]),
            "dist": r["dist"],
            "opd": r["opd"],
            "proc": r["proc"],
            "qual": r["qual"],
            "specs": json.loads(r["specs_json"]),
            "schemes": json.loads(r["schemes_json"]),
        }
        for r in rows
    ]


@app.get("/api/medicines")
def get_all_medicines():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM medicines ORDER BY id").fetchall()
    return [
        {
            "id": r["id"],
            "brand": r["brand"],
            "salt": r["salt"],
            "cat": r["cat"],
            "fmt": r["fmt"],
            "bMrp": r["bMrp"],
            "gCode": r["gCode"],
            "gName": r["gName"],
            "gMrp": r["gMrp"],
            "pack": r["pack"],
        }
        for r in rows
    ]


@app.post("/api/scan-prescription")
def scan_prescription(payload: PrescriptionInput):
    raw = payload.text.lower()
    meds = get_all_medicines()
    matched = []
    for m in meds:
        first_word = m["brand"].lower().replace("-", " ").replace("(", " ").split()[0]
        if m["brand"].lower() in raw or (len(first_word) >= 4 and first_word in raw):
            matched.append(m)
    return {"matched": matched}