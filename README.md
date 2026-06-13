# ⚖️ RightsAI — Know Before You Sign

> **An AI-powered legal document risk analyzer that detects dangerous clauses, scores document risk, and explains your rights in plain language.**

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red?style=flat-square&logo=streamlit)
![SpaCy](https://img.shields.io/badge/SpaCy-NLP-09A3D5?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🚨 The Problem

Every day, ordinary people sign documents they don't understand:

- Job offer letters with hidden non-compete clauses
- Rent agreements that illegally forfeit your deposit
- Freelance contracts where the client owns all your work
- Loan documents with buried liability traps

Hiring a lawyer costs ₹2000–5000 for a 10-minute read. Most people can't afford that — so they sign blindly.

**RightsAI changes that.**

---

## ✨ What RightsAI Does

Upload any PDF or text document → get a full risk report in seconds.

| Feature | Description |
|---|---|
| 🎯 **Risk Score (0–100)** | ML-weighted score telling you how safe the document is |
| 🔴 **Red Flag Detection** | Identifies dangerous clauses — non-compete, IP grabs, forced arbitration |
| 🟡 **Yellow Flag Detection** | Flags clauses that need careful review |
| 🟢 **Safe Clause Detection** | Highlights protective clauses already in your favor |
| 🔍 **NLP Entity Extraction** | Automatically extracts salary, notice period, company name, dates using SpaCy |
| 💬 **Chat with Document** | Ask anything about your document in plain language (GPT-powered) |
| 📝 **Plain Language Summary** | Full document explained like a friend would — no legal jargon |

---

## 🛠️ Tech Stack

```
Frontend        →  Streamlit
NLP             →  SpaCy (en_core_web_sm)
Risk Scoring    →  Custom ML weighted scoring model
AI Summary      →  OpenAI GPT-4o-mini
PDF Parsing     →  PyMuPDF + pytesseract (OCR)
Language        →  Python 3.12
```

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/shantanutech7/rightsai.git
cd rightsai
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**3. Run the app**
```bash
streamlit run app.py
```

**4. Optional — Add OpenAI API key in the sidebar** for AI summary and chat features.

---

## 📸 Screenshots

### Risk Score + NLP Extraction
- Instant 0–100 risk score with color-coded verdict
- Key information automatically extracted — salary, notice period, probation, dates

### Clause Detection
- Red flags: Non-compete, IP ownership, forced arbitration, instant termination
- Yellow flags: Notice period gaps, confidentiality scope, variable pay
- Green flags: Clear salary, leave policy, grievance mechanism

---

## 🗂️ Project Structure

```
rightsai/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Dependencies
├── sample_offer_letter.txt # Sample document for testing
└── utils/
    ├── analyzer.py         # Rule-based clause detection engine
    ├── extractor.py        # PDF & text extraction (PyMuPDF + OCR)
    ├── nlp_extractor.py    # NLP entity extraction (SpaCy)
    ├── risk_scorer.py      # ML-weighted risk scoring model
    └── ai_explainer.py     # GPT-powered plain language summary & chat
```

---

## 🧠 How the ML Risk Scorer Works

Each detected clause carries a **risk weight**:

| Clause | Weight |
|---|---|
| Non-Compete Clause | -20 pts |
| IP Ownership of Side Projects | -18 pts |
| Forced Arbitration | -15 pts |
| Immediate Termination | -17 pts |
| Clear Salary Mentioned | +8 pts |
| Leave Policy Defined | +6 pts |

Final score is clamped between 0–100. The model starts at a base of 60 and adjusts based on what's found in the document.

---

## 🎯 Supported Document Types

- ✅ Job Offer Letters
- ✅ Rent / Lease Agreements
- ✅ Freelance Contracts
- ✅ Loan Documents
- ✅ App Terms of Service
- ✅ Any PDF or TXT legal document

---

## ⚠️ Disclaimer

RightsAI is for **informational purposes only** and does not constitute legal advice. Always consult a qualified lawyer for important legal decisions.

---

## 👨‍💻 Built By

**Shantanu Bawane** — Data Science Student, Startup Founder, Product Builder

- 🔗 [GitHub](https://github.com/shantanutech7)
- 💼 B.Tech Data Science — RTMNU, Nagpur

---

*"Don't sign what you don't understand."*
