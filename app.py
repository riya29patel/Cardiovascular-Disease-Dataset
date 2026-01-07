import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Cardio Health Check",
    page_icon="🫀",
    layout="centered"
)

# ---------- GLOBAL CSS (LOCK UI) ----------
st.markdown("""
<style>

/* Hide Streamlit header */
header[data-testid="stHeader"] { display: none; }

/* Background */
.stApp { background-color: #F0FDFA; }

/* Main form card */
div[data-testid="stForm"] {
    background: #FFFFFF;
    padding: 32px;
    border-radius: 20px;
    border: 2px solid #2EC4B6;
    box-shadow: 0 12px 30px rgba(46,196,182,0.15);
}

/* Headings */
h1, h2, h3 { color: #006D77; }

/* Labels */
label, p, span {
    color: #134E4A !important;
    font-weight: 500;
}

/* ---------- NUMBER INPUT (REMOVE + -) ---------- */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none !important;
    display: none !important;
}

input[type="number"] {
    -moz-appearance: textfield !important;
    appearance: textfield !important;
    background: #E6FFFA !important;
    border: 1.5px solid #2EC4B6 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    color: #042F2E !important;
}

/* ---------- SELECT BOX ---------- */
div[data-baseweb="select"] > div {
    background: #E6FFFA !important;
    border: 1.5px solid #2EC4B6 !important;
    border-radius: 12px !important;
}

/* ---------- RADIO GROUP (LOCK SIZE + REMOVE BLACK DOT) ---------- */
div[role="radiogroup"] {
    background: #E6FFFA !important;
    padding: 14px 18px !important;
    border-radius: 14px !important;
    border: 1.5px solid #2EC4B6 !important;
    min-height: 80px;
}

/* Radio outer circle */
div[role="radiogroup"] label div:first-child {
    border: 2px solid #2EC4B6 !important;
    background: #E6FFFA !important;
}

/* REMOVE BLACK DOT COMPLETELY */
div[role="radiogroup"] label div:first-child div {
    display: none !important;
}

/* Radio text */
div[role="radiogroup"] label div:nth-child(2) {
    font-weight: 500;
    color: #134E4A !important;
}

/* ---------- SUBMIT BUTTON ---------- */
div[data-testid="stFormSubmitButton"] button {
    background: #2EC4B6 !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 14px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    width: 100% !important;
    box-shadow: 0 6px 18px rgba(46,196,182,0.45);
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: #006D77 !important;
}

/* Column spacing */
div[data-testid="column"] > div {
    margin-bottom: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<h1 style="text-align:center;">🫀 Cardiovascular Risk Analyzer</h1>
<p style="text-align:center; font-size:17px; color:#457B9D;">
Check your heart health in a few simple steps
</p>
""", unsafe_allow_html=True)

st.success("💚 Fill the form carefully for accurate results")

# ---------- FORM ----------
with st.form("cardio_form"):

    st.subheader("👤 Personal Details")
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age (Years)", 1, 120, 25)
        gender = st.selectbox("Gender", ["Select", "Male", "Female"])
    with c2:
        height = st.number_input("Height (cm)", 100, 250, 165)
        weight = st.number_input("Weight (kg)", 20, 300, 60)

    st.subheader("🩺 Medical Information")
    c3, c4 = st.columns(2)
    with c3:
        systolic = st.number_input("Systolic BP", 80, 250, 120)
        cholesterol = st.selectbox("Cholesterol Level", ["Normal", "Above Normal", "Well Above Normal"])
    with c4:
        diastolic = st.number_input("Diastolic BP", 50, 150, 80)
        glucose = st.selectbox("Glucose Level", ["Normal", "Above Normal", "Well Above Normal"])

    st.subheader("🏃 Lifestyle Habits")
    c5, c6, c7 = st.columns(3)
    with c5:
        smoking = st.radio("🚬 Smoking", ["No", "Yes"])
    with c6:
        alcohol = st.radio("🍷 Alcohol", ["No", "Yes"])
    with c7:
        activity = st.radio("🤸 Physical Activity", ["No", "Yes"])

    submit = st.form_submit_button("🔍 ANALYZE HEART RISK")

# ---------- RESULT ----------
if submit:
    if gender == "Select":
        st.error("❌ Please select gender")
    else:
        score = 0
        if age > 45: score += 1
        if systolic > 140 or diastolic > 90: score += 2
        if cholesterol != "Normal": score += 1
        if glucose != "Normal": score += 1
        if smoking == "Yes": score += 1
        if alcohol == "Yes": score += 1
        if activity == "No": score += 1

        st.subheader("📊 Analysis Result")
        if score >= 4:
            st.error("🚨 High Risk of Cardiovascular Disease")
        else:
            st.success("✅ Low Risk of Cardiovascular Disease")

        st.info(f"🔢 Risk Score: {score} / 8")
