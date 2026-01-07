import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Cardio Health Check",
    page_icon="🫀",
    layout="centered"
)

# ---------- THEME STYLING ----------
st.markdown("""
<style>
/* Hide Streamlit top header */
header[data-testid="stHeader"] {
    display: none;
}

/* App background */
.stApp {
    background-color: #F0FDFA; 
}

/* Form card */
div[data-testid="stForm"] {
    background-color: #FFFFFF;
    padding: 28px;
    border-radius: 18px;
    border: 2px solid #2EC4B6;
    box-shadow: 0 10px 25px rgba(46, 196, 182, 0.1);
}

/* Headings */
h1, h2, h3 {
    color: #006D77;
}

/* Labels & text */
label, p, span {
    color: #134E4A !important;
    font-weight: 500;
}

/* --- SELECT BOXES (Like Gender) --- */
div[data-baseweb="select"] > div {
    background-color: #E6FFFA !important; 
    border: 1.5px solid #2EC4B6 !important;
    border-radius: 12px !important;
    color: #042F2E !important;
}

/* --- SIMPLE NUMBER INPUT STYLING --- */
/* Remove ALL borders from number input containers */
div[data-testid="stNumberInput"],
div[data-testid="stNumberInput"] > div,
div[data-testid="stNumberInputContainer"],
div[data-testid="stNumberInputContainer"] > div {
    border: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
}

/* Create a custom wrapper for number inputs */
div[data-testid="stNumberInput"] {
    position: relative;
}

/* Style the input field directly */
div[data-testid="stNumberInput"] input {
    background-color: #E6FFFA !important;
    border: 1.5px solid #2EC4B6 !important;
    border-radius: 12px !important;
    color: #042F2E !important;
    -webkit-text-fill-color: #042F2E !important;
    padding: 12px 16px !important;
    width: 100% !important;
    min-height: 48px !important;
    box-sizing: border-box !important;
    outline: none !important;
}

/* Remove focus outline */
div[data-testid="stNumberInput"] input:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* Completely remove increment/decrement buttons */
button[data-testid="stNumberInputStepUp"], 
button[data-testid="stNumberInputStepDown"] {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
}

/* Hide the button container completely */
div[data-testid="stNumberInput"] > div > div:nth-child(2) {
    display: none !important;
}

/* Remove number input arrows in all browsers */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none !important;
    margin: 0 !important;
    display: none !important;
}

input[type="number"] {
    -moz-appearance: textfield !important;
    appearance: textfield !important;
}

/* --- RADIO BUTTON STYLING --- */
/* Radio button container */
div[role="radiogroup"] {
    background-color: #E6FFFA !important;
    padding: 8px !important;
    border-radius: 12px !important;
    border: 1.5px solid #2EC4B6 !important;
}

/* Individual radio button circles */
div[role="radiogroup"] > label > div:first-child {
    background-color: #E6FFFA !important;
    border: 1.5px solid #2EC4B6 !important;
    border-radius: 50% !important;
}

/* Selected radio button */
div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
    background-color: #E6FFFA !important;
}

/* Radio button inner dot */
div[role="radiogroup"] > label > div:first-child > div {
    background-color: #2EC4B6 !important;
}

/* Radio button text */
div[role="radiogroup"] > label > div:nth-child(2) {
    color: #134E4A !important;
    font-weight: 500 !important;
}

/* Hover effect */
div[role="radiogroup"] > label:hover > div:first-child {
    background-color: #B2F5EA !important;
    border-color: #2EC4B6 !important;
}

/* --- SUBMIT BUTTON --- */
div[data-testid="stFormSubmitButton"] button {
    background-color: #2EC4B6 !important; 
    color: #FFFFFF !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    width: 100% !important;
    height: 3.8rem !important;
    box-shadow: 0 4px 14px rgba(46, 196, 182, 0.4) !important;
    transition: all 0.4s ease;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background-color: #006D77 !important; 
    transform: translateY(-2px);
}

/* Fix for all input text */
input, select, textarea {
    color: #042F2E !important;
}

/* Ensure consistent spacing */
div[data-testid="column"] > div > div {
    margin-bottom: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(
    """
    <h1 style='text-align:center;'>🫀 Cardiovascular Risk Analyzer</h1>
    <p style='text-align:center; color:#457B9D; font-size:17px; margin-bottom: 20px;'>
        Check your heart health in a few simple steps
    </p>
    """,
    unsafe_allow_html=True
)

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
        cholesterol = st.selectbox(
            "Cholesterol Level",
            ["Normal", "Above Normal", "Well Above Normal"]
        )
    with col4:
        diastolic = st.number_input("Diastolic BP", 50, 150, value=80)
        glucose = st.selectbox(
            "Glucose Level",
            ["Normal", "Above Normal", "Well Above Normal"]
        )

    st.subheader("🏃 Lifestyle Habits")
    col5, col6, col7 = st.columns(3)
    # Reordered to ["No", "Yes"] with index=0 (No) as default
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
        # Risk increases if Physical Activity is "No"
        if activity == "No": risk_score += 1

        st.subheader("📊 Analysis Result")
        if risk_score >= 4:
            st.error("🚨 High Risk of Cardiovascular Disease")
            st.warning("⚠️ Medical consultation is strongly recommended.")
        else:
            st.success("✅ Low Risk of Cardiovascular Disease")
            st.info("💙 Continue maintaining healthy lifestyle habits.")
        
        st.info(f"🔢 Your Risk Score is: {risk_score} / 8")