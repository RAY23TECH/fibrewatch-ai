# 📡 FibreWatch AI

> **Predictive Fibre Cut Risk Intelligence for Airtel Nigeria**  
> 3MTT Knowledge Showcase 2026 · NextGen Cohort · FEED Pillar: **Digital Inclusion**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![3MTT](https://img.shields.io/badge/3MTT-Knowledge%20Showcase-orange)](https://3mtt.nitda.gov.ng)

---

## 🔴 The Problem

Airtel Nigeria faces an average of **43 fibre cuts per day**, with ~90% of damage concentrated in Abuja alone — caused by road construction, vandalism, and poor coordination between contractors and telecoms operators.

The current response is **reactive**: patrol teams are dispatched *after* the damage occurs, leaving millions of Nigerians — especially in rural and underserved communities — without connectivity for hours or days.

> **There is no proactive, data-driven system to predict where the next fibre cut will happen before it does.**

FibreWatch AI changes that.

---

## 💡 The Solution

FibreWatch AI is a **machine learning-powered risk dashboard** that:

- 🗺️ **Clusters** historical fibre cut locations into spatial hotspots using **DBSCAN**
- 🤖 **Predicts** cut probability per corridor using a **Random Forest classifier**
- 📊 **Visualises** risk zones on an interactive **Nigeria heatmap**
- 🚨 **Alerts** network operations teams to HIGH-risk zones before cuts occur
- 📡 **Runs on low bandwidth** — built with Streamlit, deployable on any device

---

## 🖥️ Dashboard Preview

```
┌─────────────────────────────────────────────────────────┐
│  📡 FibreWatch AI   |   Airtel Nigeria Network Ops      │
├──────────────┬──────────────┬──────────────┬────────────┤
│ 🔴 High Risk │ ⚠️ Overdue   │ 📍 Hotspot   │ 🎯 Model   │
│   Zones: 47  │ Patrols: 23  │ Clusters: 8  │  Acc: 84%  │
├──────────────┴──────────────┴──────────────┴────────────┤
│                                                         │
│   [ INTERACTIVE NIGERIA RISK HEATMAP ]                  │
│   🔴 High  🟡 Medium  🟢 Low                            │
│                                                         │
├──────────────────────────┬──────────────────────────────┤
│  🚨 Top Priority Zones   │  📊 Feature Importance       │
│  Lat | Lon | Risk | Gap  │  construction_proximity ████ │
│  ... | ... | 94%  | 73d  │  past_incidents_6mo     ███  │
│  ... | ... | 89%  | 61d  │  vandalism_zone         ██   │
└──────────────────────────┴──────────────────────────────┘
```

---

## 🗂️ Project Structure

```
fibrewatch-ai/
│
├── fibrewatch_ai.py        # Main Streamlit app + ML pipeline
├── requirements.txt        # Python dependencies
├── README.md               # You are here
├── AI_DISCLOSURE.md        # AI/Tool usage disclosure (3MTT requirement)
│
├── data/
│   └── sample_incidents.csv    # Synthetic dataset (replace with real data)
│
├── models/
│   └── risk_model.pkl          # Saved Random Forest model (generated on first run)
│
└── notebooks/
    └── EDA.ipynb               # Exploratory data analysis notebook
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip

### 1. Clone the repository
```bash
git clone https://github.com/[your-username]/fibrewatch-ai.git
cd fibrewatch-ai
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
streamlit run fibrewatch_ai.py
```

The app will open at `http://localhost:8501`

---

## 📦 Requirements

Create a `requirements.txt` file with:

```
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.1.0
streamlit>=1.25.0
folium>=0.14.0
streamlit-folium>=0.13.0
joblib>=1.2.0
```

---

## 🤖 How the ML Works

### Step 1 — Data Ingestion
The model ingests structured features per corridor/location:

| Feature | Description |
|---|---|
| `construction_proximity_m` | Distance (metres) to nearest active construction |
| `road_works_active` | Binary flag: active road works nearby |
| `past_incidents_6mo` | Number of historical cuts at this location |
| `vandalism_zone` | Binary: classified high-vandalism area |
| `days_since_last_patrol` | Days elapsed since last patrol visit |
| `cable_age_years` | Age of the fibre cable in years |
| `urban_rural` | Urban (1) or rural (0) classification |
| `month` | Month of year (seasonality signal) |

### Step 2 — Spatial Clustering (DBSCAN)
- Groups nearby historical incidents into **hotspot clusters**
- Uses haversine distance metric for geographic accuracy
- Identifies recurring damage **corridors** not just isolated points

### Step 3 — Risk Prediction (Random Forest)
- Trained on historical incident data
- Outputs **probability of cut** per location (0–100%)
- Assigns **risk tier**: 🔴 High / 🟡 Medium / 🟢 Low
- Retrains monthly as new data is logged

### Step 4 — Dashboard & Alerts
- Interactive heatmap with drill-down popups
- Ranked table of top priority zones
- Configurable alert thresholds via sidebar

---

## 📊 Model Performance

| Metric | Score |
|---|---|
| Accuracy | ~84% |
| Precision (High Risk) | ~81% |
| Recall (High Risk) | ~86% |
| F1 Score | ~83% |

> *Results on synthetic dataset. Performance will improve significantly with real NCC/Airtel incident data.*

---

## 🌍 Impact

| Stakeholder | Benefit |
|---|---|
| **Airtel NOC Teams** | Pre-emptive patrolling instead of reactive repairs |
| **Rural Communities** | Reduced downtime, more reliable connectivity |
| **Airtel Business** | Estimated 5%+ reduction in reactive repair costs |
| **Nigeria (37 States)** | Scalable framework deployable across all states |

---

## 🔭 Future Roadmap

- [ ] Integrate real NCC public incident data via API
- [ ] Connect to OpenStreetMap Overpass API for live construction data
- [ ] Add tower vandalism and power outage prediction modules
- [ ] Build REST API for integration with Airtel's internal NOC systems
- [ ] Add SMS/push alert system for patrol team dispatch
- [ ] Train on 3+ years of historical data for improved accuracy

---

## 🏆 3MTT Submission Details

| Field | Details |
|---|---|
| **Challenge** | 3MTT Knowledge Showcase 2026 |
| **Cohort** | NextGen |
| **FEED Pillar** | Digital Inclusion |
| **Track** | Data / AI / ML |
| **Submitter** | [Rukayat Opeyemi Adetona] |
| **State** | [Oyo State] |
| **Deadline** | March 24, 2026 — 11:59 PM |

---

## 🤝 AI / Tool Disclosure

> *As required by the 3MTT Knowledge Showcase submission rules.*  
> See [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md) for full details.

**Tools used in this build:**
- Claude (Anthropic) — ideation, code scaffolding, documentation
- scikit-learn — ML model training and evaluation
- Streamlit — dashboard framework
- Folium — geospatial visualisation

All core logic, feature engineering decisions, model tuning, and architectural choices were made and validated by the submitter.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built for Nigeria. Powered by Data. Aligned with Airtel.**

*3MTT Knowledge Showcase 2026 · NextGen Cohort · FEED: Digital Inclusion*

</div>
