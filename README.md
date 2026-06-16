# MIRAGE

AI-Based Unified Browser Extension for Real-Time Social Engineering Attack Detection

---

# Overview

MIRAGE is a browser-native phishing detection platform designed to identify and explain social engineering attacks in real time.

The system combines:

- Email Analysis
- URL Analysis
- Threat Intelligence
- Brand Impersonation Detection
- Domain Trust Analysis
- Reputation Analysis
- Campaign Correlation

to provide explainable risk assessments directly inside the browser.

Unlike traditional security tools that treat threats independently, MIRAGE correlates suspicious events into larger phishing campaigns, helping users understand not only individual threats but also coordinated attack activity.

---

# Key Features

## Email Intelligence

- DistilBERT-based phishing detection
- Gmail integration
- Risk score generation
- Human-readable explanations
- Campaign correlation support

---

## URL Intelligence

- XGBoost URL Model V3
- Brand impersonation detection
- Suspicious keyword analysis
- Brand-context correlation
- WHOIS-based domain trust evaluation
- Domain reputation analysis
- Threat intelligence integration
- Explainable findings

---

## Campaign Correlation Engine

- Event-driven campaign detection
- Brand-based correlation
- Temporal correlation windows
- Campaign risk scoring
- Analyst-friendly explanations

---

## Browser Extension

- Chrome Manifest V3
- Gmail monitoring
- URL monitoring
- Explainability dashboard
- Risk breakdown visualization
- Campaign visibility

---

# Architecture

Chrome Extension
│
├── Popup UI
├── Content Scripts
├── Background Service Worker
│
▼
FastAPI Backend
│
├── Email Intelligence Pipeline
├── URL Intelligence Pipeline
├── Threat Correlation Engine
├── Risk Fusion Engine
└── SQLite Storage

---

# URL Intelligence Pipeline

URL
│
├── Threat Intelligence Layer
├── Brand Impersonation Engine
├── Context Analysis Engine
├── Brand/Context Correlation Engine
├── Domain Trust Layer (WHOIS)
├── Reputation Layer
├── URL Model V3 (XGBoost)
└── Risk Fusion Engine
│
▼
Final Risk Score

---

# Current Status

## Implemented

### Email Analysis

- DistilBERT Email Model
- FastAPI Integration
- Gmail Integration
- Risk Scoring

### URL Analysis

- URL Model V3
- Threat Intelligence Layer
- Brand Impersonation Engine
- Context Analysis Engine
- Correlation Engine
- Domain Trust Layer
- Reputation Layer
- Risk Fusion Engine

### Correlation

- Campaign Detection
- Brand Correlation
- Campaign Risk Scoring

### User Interface

- Explainability Dashboard
- Risk Breakdown Display
- Threat Explanations
- Campaign Information Display

---

## Known Limitations

- Automatic page-level warning injection is currently under refinement due to Chrome Manifest V3 content-script lifecycle constraints.
- Live external threat feeds are not yet integrated.
- Campaign visualization remains under active development.

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLite

## Machine Learning

### Email

- DistilBERT

### URL

- XGBoost
- TF-IDF
- Lexical Feature Engineering

## Browser Extension

- TypeScript
- React
- Vite
- Chrome Manifest V3

---

# Getting Started

## Prerequisites

Install:

- Python 3.12+
- Node.js 20+
- Google Chrome

---

# Clone Repository

```bash
git clone <repository-url>
cd MIRAGE--AI-EL
```

---

# Backend Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

# Extension Setup

Install frontend dependencies:

```bash
npm install
```

Build the extension:

```bash
npm run build
```

---

# Load the Extension

Open:

```text
chrome://extensions
```

Enable:

```text
Developer Mode
```

Click:

```text
Load Unpacked
```

Select:

```text
dist/
```

generated after:

```bash
npm run build
```

---

# Testing URL Analysis

Open:

```text
http://localhost:8000/docs
```

Use:

```json
POST /analyze-url

{
  "url": "https://google-security.com"
}
```

Expected Response:

```json
{
  "risk_score": 0.63,
  "reasons": [
    "Brand detected: Google",
    "Brand mismatch detected",
    "Keywords found: security"
  ]
}
```

---

# Testing Email Analysis

1. Start the backend.
2. Load the extension.
3. Open Gmail.
4. Open an email.
5. Click the MIRAGE extension icon.

Expected:

- Email Risk Score
- Risk Level
- Detection Reasons
- Campaign Information (if available)

---

# Project Structure

```text
backend/
│
├── api/
├── services/
├── models/
├── intelligence/
├── factory/
└── tests/

src/
│
├── popup/
├── content/
├── background/
└── components/

public/
│
└── manifest.json

Email-model-main/
│
└── Email model training artifacts

URL_MODEL V3/
│
└── URL model training artifacts
```

---

# Notes

The following folders are included primarily for reproducibility and research purposes:

```text
Email-model-main
URL_MODEL V3
```

The production system uses the integrated models stored under:

```text
backend/models/
```

No retraining is required to run MIRAGE.

---

# Core Innovation

The primary innovation of MIRAGE is the Threat Correlation Engine.

Instead of treating:

- Emails
- URLs
- Browser Events

as isolated detections, MIRAGE groups related events into campaigns using:

- Brand Similarity
- Risk Thresholds
- Temporal Correlation

This enables campaign-level visibility and provides users with explainable intelligence rather than isolated threat scores. The campaign-based approach follows the MIRAGE Threat Correlation Engine specification. :contentReference[oaicite:0]{index=0}

---

# Design Philosophy

MIRAGE does not rely solely on Artificial Intelligence.

Instead, it combines:

- Threat Intelligence
- Brand Detection
- Context Analysis
- Domain Trust
- Reputation Signals
- Machine Learning

through a layered risk assessment strategy, consistent with the approved hybrid architecture. :contentReference[oaicite:1]{index=1}

The goal is to provide:

- Better Explainability
- Reduced False Positives
- Improved Maintainability
- Future Extensibility

while remaining transparent and user-friendly.

---

# Team

- Atharva Gupta
- Amogh D Acharya
- Prajwal V Jois
- Shaurya Khanna

RV College of Engineering

Department of Computer Science and Engineering (Artificial Intelligence & Machine Learning)

2026
