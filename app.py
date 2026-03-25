import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Fazaila Tracker", page_icon="🩺", layout="centered")

# PWA manifest (makes it installable)
st.markdown("""
    <link rel="manifest" href="manifest.json">
    <style>
    .stApp { max-width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Fazaila Symptom & Vitals Tracker")
st.caption("Metastatic Gastric Cancer • Cycle 6 (13 Mar 2026) • Nadir Week 20–27 Mar")

# Data handling
if "df" not in st.session_state:
    try:
        df = pd.read_csv("fazaila_data.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Time", "Stomach_Empty", "Borborygmi", "BP_Sys", "BP_Dia", 
                                   "Tongue_Burning", "Jaw_Scapula_Pain", "Meal_Readiness", "Notes"])
    st.session_state.df = df

date_today = datetime.now().strftime("%Y-%m-%d %H:%M")

st.subheader(f"Daily Entry — {date_today}")

with st.form("daily_entry"):
    stomach_empty = st.slider("Morning empty-stomach stomach readiness (0-5)", 0, 5, 3)
    borborygmi = st.slider("Borborygmi / stomach gurgles (0-5)", 0, 5, 2)
    bp_sys = st.number_input("BP Systolic", 70, 160, 100)
    bp_dia = st.number_input("BP Diastolic", 40, 100, 60)
    tongue_burning = st.slider("Tongue burning (0-5)", 0, 5, 1)
    jaw_pain = st.slider("Jaw / scapula / ear pain (0-5)", 0, 5, 2)
    meal_readiness = st.slider("Meal timing readiness now (0-5)", 0, 5, 3)
    notes = st.text_area("Notes (meals, symptoms, etc.)", "")

    submitted = st.form_submit_button("✅ Save Entry")
    
    if submitted:
        new_row = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Time": datetime.now().strftime("%H:%M"),
            "Stomach_Empty": stomach_empty,
            "Borborygmi": borborygmi,
            "BP_Sys": bp_sys,
            "BP_Dia": bp_dia,
            "Tongue_Burning": tongue_burning,
            "Jaw_Scapula_Pain": jaw_pain,
            "Meal_Readiness": meal_readiness,
            "Notes": notes
        }])
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.session_state.df.to_csv("fazaila_data.csv", index=False)
        st.success("✅ Saved!")

# History & Charts
st.subheader("History & Trends")
if not st.session_state.df.empty:
    st.dataframe(st.session_state.df.tail(10), use_container_width=True)
    
    st.session_state.df["Pulse_Pressure"] = st.session_state.df["BP_Sys"] - st.session_state.df["BP_Dia"]
    fig = px.line(st.session_state.df, x="Date", y="Pulse_Pressure", title="Pulse Pressure Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    csv = st.session_state.df.to_csv(index=False).encode()
    st.download_button("📤 Download Full Data", csv, "fazaila_tracker_data.csv", "text/csv")
else:
    st.info("No entries yet — add the first one above!")

st.caption("Private • Data saved locally • Built for Fazaila")
