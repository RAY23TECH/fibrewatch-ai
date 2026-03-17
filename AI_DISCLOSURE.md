# 🤖 AI / Tool Disclosure

> **3MTT Knowledge Showcase 2026 — Required Submission Document**  
> Submitter: [Your Full Name] | State: [Your State] | Track: Data / AI / ML

---

## Overview

In accordance with the 3MTT Knowledge Showcase rules, this document discloses all AI tools and third-party platforms used during the development of **FibreWatch AI**.

---

## AI Tools Used

### 1. Claude (Anthropic)
- **Purpose:** Initial project ideation, code scaffolding for the Streamlit dashboard, README and documentation drafting
- **What I did myself:** All feature engineering decisions, model tuning (hyperparameters, threshold selection), data pipeline design, dashboard UX decisions, and final code validation and testing
- **Extent of use:** High — used as a starting point and documentation assistant

### 2. scikit-learn (Machine Learning Library)
- **Purpose:** Random Forest classifier training, DBSCAN clustering, model evaluation metrics
- **Nature:** Open-source Python library, not generative AI
- **Extent of use:** Core to the ML pipeline

### 3. Streamlit (Dashboard Framework)
- **Purpose:** Building the interactive web dashboard
- **Nature:** Open-source Python framework, not generative AI
- **Extent of use:** Core to the frontend presentation layer

### 4. Folium (Geospatial Visualisation Library)
- **Purpose:** Rendering the interactive Nigeria risk heatmap
- **Nature:** Open-source Python library, not generative AI
- **Extent of use:** Used for map visualisation

---

## What Was Built Independently

The following were designed, implemented, and validated entirely by the submitter:

- Problem framing and real-world relevance (Airtel fibre cut crisis)
- Choice of FEED pillar and alignment justification
- Feature selection and engineering for the risk model
- DBSCAN parameter tuning (epsilon radius, min_samples)
- Random Forest hyperparameter tuning and evaluation
- Risk tier threshold decisions (Low / Medium / High)
- Dashboard layout and user experience design
- Deployment to Streamlit Community Cloud
- All submission materials (brief, video, pitch)

---

## Data Sources

| Source | Type | Usage |
|---|---|---|
| Synthetic generator (custom) | Generated | Model training and demo |
| NCC public incident reports | Public | Planned for production version |
| OpenStreetMap Overpass API | Public | Planned for production version |
| FERMA road construction data | Public | Planned for production version |

---

## Statement of Originality

I confirm that:
- This submission is my own individual work
- No team members contributed to this submission
- AI tools were used as assistants, not as the primary builder
- All code has been reviewed, understood, and validated by me personally
- The problem, solution design, and impact framing are original to this submission

**Signed:** [Your Full Name]  
**Date:** March 24, 2026  
**State:** [Your State]

---

*Submitted in compliance with 3MTT Knowledge Showcase 2026 Rules & Guidelines.*
