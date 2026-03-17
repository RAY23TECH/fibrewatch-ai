"""
FibreWatch AI — Predictive Fibre Cut Risk Dashboard
3MTT Knowledge Showcase | NextGen Cohort | February 2026
Author: [Your Name]
Track: Data / AI / ML
FEED Pillar: Digital Inclusion
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.cluster import DBSCAN
import streamlit as st
import folium
from streamlit_folium import st_folium
import json

# ─────────────────────────────────────────────
# 1. SYNTHETIC DATA GENERATOR
#    Replace this with real NCC/Airtel data when available.
#    Data fields mirror what a real incident log would contain.
# ─────────────────────────────────────────────

def generate_sample_data(n=500, seed=42):
    """
    Generates synthetic fibre cut incident records for Nigeria.
    In production, replace with:
      - NCC public incident reports (CSV/API)
      - Airtel internal NOC logs
      - State road construction permit data
    """
    np.random.seed(seed)
    
    # Nigeria bounding box: lat 4.2–13.9, lon 2.7–14.7
    lats = np.random.uniform(4.2, 13.9, n)
    lons = np.random.uniform(2.7, 14.7, n)
    
    # Features that predict fibre cut risk
    data = pd.DataFrame({
        "latitude": lats,
        "longitude": lons,
        "construction_proximity_m": np.random.exponential(500, n),  # metres to nearest active construction
        "road_works_active": np.random.randint(0, 2, n),            # 1 = active road works nearby
        "past_incidents_6mo": np.random.poisson(2, n),              # historical cuts at this location
        "vandalism_zone": np.random.randint(0, 2, n),               # 1 = classified high-vandalism area
        "days_since_last_patrol": np.random.randint(1, 90, n),
        "cable_age_years": np.random.uniform(1, 15, n),
        "urban_rural": np.random.randint(0, 2, n),                  # 1 = urban, 0 = rural
        "month": np.random.randint(1, 13, n),                       # seasonality signal
    })
    
    # Target: 1 = cut occurred, 0 = no cut
    # Logic: higher risk when construction nearby, vandalism zone, old cable, many past incidents
    risk_score = (
        (data["construction_proximity_m"] < 300).astype(int) * 3 +
        data["road_works_active"] * 2 +
        (data["past_incidents_6mo"] > 3).astype(int) * 2 +
        data["vandalism_zone"] * 2 +
        (data["cable_age_years"] > 10).astype(int) +
        (data["days_since_last_patrol"] > 60).astype(int)
    )
    data["cut_occurred"] = (risk_score + np.random.randint(0, 3, n) > 5).astype(int)
    
    return data


# ─────────────────────────────────────────────
# 2. GEOSPATIAL CLUSTERING
#    DBSCAN finds spatial hotspots — corridors
#    where cuts cluster together historically.
# ─────────────────────────────────────────────

def find_hotspots(df):
    """
    Uses DBSCAN to cluster incident locations.
    Returns original df with cluster labels.
    - Cluster >= 0: a hotspot zone
    - Cluster == -1: noise / isolated incident
    """
    coords = df[df["cut_occurred"] == 1][["latitude", "longitude"]].values
    
    # epsilon in radians (~50km radius), min 3 incidents to form a cluster
    epsilon = 50 / 6371  # 50km / Earth radius
    db = DBSCAN(eps=epsilon, min_samples=3, algorithm="ball_tree", metric="haversine")
    
    labels = db.fit_predict(np.radians(coords))
    
    hotspot_df = df[df["cut_occurred"] == 1].copy()
    hotspot_df["cluster"] = labels
    return hotspot_df


# ─────────────────────────────────────────────
# 3. RISK PREDICTION MODEL
#    Random Forest trained on historical features.
#    Outputs probability of cut per corridor.
# ─────────────────────────────────────────────

FEATURES = [
    "construction_proximity_m",
    "road_works_active",
    "past_incidents_6mo",
    "vandalism_zone",
    "days_since_last_patrol",
    "cable_age_years",
    "urban_rural",
    "month"
]

def train_model(df):
    """Trains Random Forest risk classifier."""
    X = df[FEATURES]
    y = df["cut_occurred"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    return model, report


def predict_risk(model, df):
    """Adds risk probability column to dataframe."""
    df = df.copy()
    df["risk_probability"] = model.predict_proba(df[FEATURES])[:, 1]
    df["risk_tier"] = pd.cut(
        df["risk_probability"],
        bins=[0, 0.33, 0.66, 1.0],
        labels=["🟢 Low", "🟡 Medium", "🔴 High"]
    )
    return df


# ─────────────────────────────────────────────
# 4. HEATMAP VISUALISATION
#    Folium map with colour-coded risk markers.
# ─────────────────────────────────────────────

def build_heatmap(df):
    """Builds interactive Folium heatmap of Nigeria."""
    nigeria_map = folium.Map(location=[9.0, 8.0], zoom_start=6, tiles="CartoDB dark_matter")
    
    color_map = {"🔴 High": "red", "🟡 Medium": "orange", "🟢 Low": "green"}
    
    for _, row in df.iterrows():
        color = color_map.get(str(row["risk_tier"]), "blue")
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6 if color == "red" else 4,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"""
                <b>Risk Tier:</b> {row['risk_tier']}<br>
                <b>Probability:</b> {row['risk_probability']:.0%}<br>
                <b>Past Incidents (6mo):</b> {int(row['past_incidents_6mo'])}<br>
                <b>Construction Nearby:</b> {'Yes' if row['road_works_active'] else 'No'}<br>
                <b>Days Since Patrol:</b> {int(row['days_since_last_patrol'])}
                """,
                max_width=200
            )
        ).add_to(nigeria_map)
    
    return nigeria_map


# ─────────────────────────────────────────────
# 5. STREAMLIT DASHBOARD
#    Run with: streamlit run fibrewatch_ai.py
# ─────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="FibreWatch AI — Airtel Nigeria",
        page_icon="📡",
        layout="wide"
    )

    # Header
    st.markdown("""
    <div style='background:#0D1B2A; padding:20px; border-radius:8px; margin-bottom:20px;'>
        <h1 style='color:#E8670A; margin:0;'>📡 FibreWatch AI</h1>
        <p style='color:#AAAAAA; margin:4px 0 0 0;'>Predictive Fibre Cut Risk Intelligence | Airtel Nigeria Network Operations</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar controls
    st.sidebar.header("⚙️ Controls")
    show_high_only = st.sidebar.checkbox("Show HIGH RISK zones only", value=False)
    max_patrol_days = st.sidebar.slider("Alert: Days since last patrol >", 0, 90, 60)
    risk_threshold = st.sidebar.slider("Risk probability threshold", 0.0, 1.0, 0.5)

    # Load + train
    with st.spinner("Loading data and training model..."):
        df = generate_sample_data()
        model, report = train_model(df)
        df = predict_risk(model, df)
        hotspots = find_hotspots(df)

    # KPI row
    high_risk = df[df["risk_tier"] == "🔴 High"]
    needs_patrol = df[df["days_since_last_patrol"] > max_patrol_days]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔴 High Risk Zones", len(high_risk))
    col2.metric("⚠️ Overdue Patrols", len(needs_patrol))
    col3.metric("📍 Hotspot Clusters", hotspots["cluster"].nunique() - (1 if -1 in hotspots["cluster"].values else 0))
    col4.metric("🎯 Model Accuracy", f"{report['accuracy']:.0%}")

    st.markdown("---")

    # Map + table
    map_col, table_col = st.columns([2, 1])

    with map_col:
        st.subheader("🗺️ Network Risk Heatmap — Nigeria")
        display_df = high_risk if show_high_only else df[df["risk_probability"] >= risk_threshold]
        fmap = build_heatmap(display_df)
        st_folium(fmap, width=700, height=480)

    with table_col:
        st.subheader("🚨 Top Priority Zones")
        top_zones = df.nlargest(15, "risk_probability")[[
            "latitude", "longitude", "risk_tier", "risk_probability",
            "past_incidents_6mo", "days_since_last_patrol"
        ]].copy()
        top_zones["risk_probability"] = top_zones["risk_probability"].apply(lambda x: f"{x:.0%}")
        top_zones.columns = ["Lat", "Lon", "Tier", "Risk %", "Incidents", "Patrol Gap"]
        st.dataframe(top_zones, use_container_width=True, height=480)

    st.markdown("---")

    # Feature importance
    st.subheader("📊 What Drives Risk? — Feature Importance")
    importance_df = pd.DataFrame({
        "Feature": FEATURES,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False)

    st.bar_chart(importance_df.set_index("Feature")["Importance"])

    # Footer
    st.markdown("""
    <div style='text-align:center; color:#888; margin-top:20px; font-size:12px;'>
    FibreWatch AI | 3MTT Knowledge Showcase 2026 | FEED Pillar: Digital Inclusion | Built by [Your Name]
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
