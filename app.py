import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import os

st.set_page_config(page_title="Fazaila Tracker", page_icon="🩺", layout="wide")

# Data file
data_file = "fazaila_data.csv"

if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
    df = pd.read_csv(data_file)
else:
    df = pd.DataFrame(columns=["Date", "Time", "Stomach_Empty", "Borborygmi", "BP_Sys", "BP_Dia",
                               "Tongue_Burning", "Jaw_Scapula_Pain", "Meal_Readiness",
                               "Fatigue", "Physical", "Sleep", "Nutrition", "Emotional", "GI", "Neurology", "Notes"])

if "df" not in st.session_state:
    st.session_state.df = df

st.title("🩺 Fazaila Symptom & Vitals Tracker")
st.caption("Metastatic Gastric Cancer • Cycle 6 (13 Mar 2026) • Nadir Week 20–27 Mar")

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["📝 Daily Entry", "📊 Vitals", "🌟 QoL", "👨‍⚕️ Caregiver Dashboard"])

with tab1:
    st.subheader(f"Daily Entry — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    with st.form("daily_entry"):
        col1, col2 = st.columns(2)
        with col1:
            stomach_empty = st.slider("Morning empty-stomach readiness (0-5)", 0, 5, 3)
            borborygmi = st.slider("Borborygmi (0-5)", 0, 5, 2)
            bp_sys = st.number_input("BP Systolic", 70, 160, 100)
            bp_dia = st.number_input("BP Diastolic", 40, 100, 60)
        with col2:
            tongue_burning = st.slider("Tongue burning (0-5)", 0, 5, 1)
            jaw_pain = st.slider("Jaw / scapula / ear pain (0-5)", 0, 5, 2)
            meal_readiness = st.slider("Meal timing readiness (0-5)", 0, 5, 3)
            fatigue = st.slider("Fatigue (0-5)", 0, 5, 2)
        
        notes = st.text_area("Notes", "")
        
        if st.form_submit_button("✅ Save Entry"):
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
                "Fatigue": fatigue,
                "Physical": 0, "Sleep": 0, "Nutrition": 0, "Emotional": 0, "GI": 0, "Neurology": 0,
                "Notes": notes
            }])
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.session_state.df.to_csv(data_file, index=False)
            st.success("✅ Saved!")

with tab2:
    st.subheader("Vitals Dashboard")
    if not st.session_state.df.empty:
        st.session_state.df["Pulse_Pressure"] = st.session_state.df["BP_Sys"] - st.session_state.df["BP_Dia"]
        st.dataframe(st.session_state.df[["Date", "Time", "BP_Sys", "BP_Dia", "Pulse_Pressure"]].tail(10))
        fig = px.line(st.session_state.df, x="Date", y="Pulse_Pressure", title="Pulse Pressure Trend")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("QoL Dashboard")
    st.info("Full QoL sections coming in next update — for now you can add scores in Daily Entry and they will appear here soon.")

with tab4:
    st.subheader("Caregiver Management Dashboard")
    if not st.session_state.df.empty:
        st.write("**Recent Trends**")
        st.dataframe(st.session_state.df.tail(10))
        st.download_button("📤 Download Full Data", st.session_state.df.to_csv(index=False).encode(), "fazaila_full_data.csv")
        st.success("Red-flag alerts and detailed management tools will be added in the next version.")

st.caption("Private app • Built for Fazaila • Data saved locally")
