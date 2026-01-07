import streamlit as st

# ---------- PAGE CONFIG (LOCKED) ----------
st.set_page_config(
    page_title="Cardio Health Check",
    page_icon="🫀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- THEME & UI LOCK ----------
st.markdown("""
<style>
/* Hide Streamlit default header */
header[data-testid="stHeader"] {
    display: none;
}

/* App background */
.stApp {
    background-color: #F0FDFA;
}

/* Prevent Streamlit Cloud font override */
* {
    font-family: "Segoe UI", sans-serif !important;
}

/* Form card */
div[data-testid="stForm"] {
    background-color: #FFFFFF;
    padding: 28px;
    border-radius: 18px;
    border: 2px solid #2EC4B6;
    box-shadow: 0 10px 25px rgba(46, 196, 182, 0.1);
}

/* Force heading visibility (DEPLOY FIX) */
h1, h2, h3 {
    color: #006D77 !important;
    opacity: 1 !important;
}

/* Labels & text */
label, p, span {
    color: #134E4A !important;
    font-weight: 500;
}

/* SELECT BOXES */
div[data-baseweb="select"] > div {
    background-color: #E6FFFA !important;
    border: 1.5px solid #2EC4B6 !important;
    border-radius: 12px !important;
    color: #042F2E !important;
}

/* NUMBER INPUT FIX */
div[data-testid="stNumberInput"],
div[data-testid="stNumberInput"] > div {
    border: none !important;
    background-color: transparent !important;
}

div[data-testid="stNumberInput"] input {
    background-color: #E6FFFA !important;
    border: 1.5px solid #2EC4B6 !important;
    border-radius: 12px !important;
    color: #042F2E !important;
    padding: 12px 16px !important;
    width: 100% !important;
    min-height: 48px !important;
}

/* Remove number arrows */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    display: none !important;
}
input[type="number"] {
    -moz-appearance: textfield !important;
}

/* RADIO BUTTON FIX (DEPLOY SAFE) */
div[role="radiogroup"] {
    background-color: #E6FFFA !important;
    padding: 10px !important;
    border-radius: 12px !important;
    border: 1.5px solid #2EC4B6 !important;
}

/* Radio text */
div[role="radiogroup"] label div:nth-child(2) {
    color: #134E4A !important;
    font-weight: 500 !important;
}

/* SUBMIT BUTTON */
div[data-testid="stFormSubmitButton"] button {
    background-color: #2EC4B6 !important;
    color: white !important;
    border-radius: 14px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    width: 100% !important;
    height: 3.8rem !important;
    box-shadow: 0 4px 14px rgba(46, 196, 182, 0.4) !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background-color: #006D77 !important;
    transform: translateY(-2px);
}

/* Spacing consistency */
div[data-testid="column"] > div > div {
    margin-bottom: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<h1 style="text-align:center; color:#006D77;">🫀 Cardiovascular Risk Analyzer</h1>
<p style="text-align:center; color:#457B9D; font-size:17px; margin-bottom: 20px;">
    Check your heart health in a few simple steps
</p>
""", unsafe_allow_html=True)

st.success("💚 Fill the form carefully for accurate results")
st.divider()

# ---------- FORM ----------
with st.form("cardio_form"):

    st.subheader("👤 Personal Details")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (Years)", 1, 120, value=25)
        gender = st.selectbox("Gender", ["Select", "Male", "Female"])
    with col2:
        height = st.number_input("Height (cm)", 100, 250, value=165)
        weight = st.number_input("Weight (kg)", 20, 300, value=60)

    st.subheader("🩺 Medical Information")
    col3, col4 = st.columns(2)
    with col3:
        systolic = st.number_input("Systolic BP", 80, 250, value=120)
        cholesterol = st.selectbox("Cholesterol Level", ["Normal", "Above Normal", "Well Above Normal"])
    with col4:
        diastolic = st.number_input("Diastolic BP", 50, 150, value=80)
        glucose = st.selectbox("Glucose Level", ["Normal", "Above Normal", "Well Above Normal"])

    st.subheader("🏃 Lifestyle Habits")
    col5, col6, col7 = st.columns(3)
    with col5:
        smoking = st.radio("🚬 Smoking", ["No", "Yes"], index=0)
    with col6:
        alcohol = st.radio("🍷 Alcohol", ["No", "Yes"], index=0)
    with col7:
        activity = st.radio("🤸 Physical Activity", ["No", "Yes"], index=0)

    st.divider()
    submit = st.form_submit_button("🔍 ANALYZE HEART RISK")

# ---------- ANALYSIS ----------
if submit:
    if gender == "Select":
        st.error("❌ Please select gender before submitting")
    else:
        risk_score = 0
        if age > 45: risk_score += 1
        if systolic > 140 or diastolic > 90: risk_score += 2
        if cholesterol != "Normal": risk_score += 1
        if glucose != "Normal": risk_score += 1
        if smoking == "Yes": risk_score += 1
        if alcohol == "Yes": risk_score += 1
        if activity == "No": risk_score += 1

        st.subheader("📊 Analysis Result")
        if risk_score >= 4:
            st.error("🚨 High Risk of Cardiovascular Disease")
            st.warning("⚠️ Medical consultation is strongly recommended.")
        else:
            st.success("✅ Low Risk of Cardiovascular Disease")
            st.info("💙 Continue maintaining healthy lifestyle habits.")

        st.info(f"🔢 Your Risk Score is: {risk_score} / 8")
