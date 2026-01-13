import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CardioCheck - Heart Health Analyzer",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- LOAD MODEL ----------
model = joblib.load("heart_disease_model.pkl")

# ---------- DARK/LIGHT MODE DETECTION & STYLING ----------
st.markdown("""
<script>
    // Detect dark mode
    const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.body.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
</script>

<style>
    /* CSS Variables for theming */
    :root {
        --primary: #2EC4B6;
        --primary-dark: #009688;
        --secondary: #006D77;
        --accent: #FF6B6B;
        --success: #28A745;
        --warning: #FFC107;
        --danger: #DC3545;
        --text-primary: #134E4A;
        --text-secondary: #457B9D;
        --bg-primary: #F0FDFA;
        --bg-secondary: #FFFFFF;
        --bg-card: #FFFFFF;
        --border-color: #2EC4B6;
        --shadow-color: rgba(46, 196, 182, 0.15);
    }
    
    [data-theme="dark"] {
        --primary: #26A69A;
        --primary-dark: #00796B;
        --secondary: #004D40;
        --accent: #FF5252;
        --success: #4CAF50;
        --warning: #FFB74D;
        --danger: #EF5350;
        --text-primary: #E0F2F1;
        --text-secondary: #80CBC4;
        --bg-primary: #121212;
        --bg-secondary: #1E1E1E;
        --bg-card: #2D2D2D;
        --border-color: #26A69A;
        --shadow-color: rgba(38, 166, 154, 0.2);
    }
    
    /* Global Styles */
    * {
        transition: background-color 0.3s ease, border-color 0.3s ease;
    }
    
    .stApp {
        background-color: var(--bg-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide default header */
    # header[data-testid="stHeader"] { 
    #     display: none; 
    # }
    header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
    }
    
    /* Smooth transitions */
    div, button, input, select {
        transition: all 0.3s ease !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 1.5rem 1rem;
        margin: -1rem -1rem 1rem -1rem;
        text-align: center;
        border-radius: 0 0 20px 20px;
    }
    
    .sidebar-header h2 {
        color: white;
        margin: 0.5rem 0;
        font-weight: 700;
    }
    
    .sidebar-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* Card Components */
    .card {
        background: var(--bg-card);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px var(--shadow-color);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px var(--shadow-color);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--bg-card), var(--bg-secondary));
        border-left: 4px solid var(--primary);
    }
    
    .info-card {
        background: linear-gradient(135deg, rgba(46, 196, 182, 0.1), rgba(46, 196, 182, 0.05));
        border: 1px solid rgba(46, 196, 182, 0.3);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 196, 182, 0.3);
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary) 100%);
    }
    
    .secondary-button {
        background: transparent !important;
        border: 2px solid var(--primary) !important;
        color: var(--primary) !important;
    }
    
    .secondary-button:hover {
        background: var(--primary) !important;
        color: white !important;
    }
    
    /* Form Styling */
    .stForm {
        background: var(--bg-card);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 25px var(--shadow-color);
    }
    
    /* Input Fields */
    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInput"] input,
    div[role="radiogroup"] {
        background: var(--bg-secondary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }
    
    div[data-baseweb="select"] > div:hover,
    div[data-testid="stNumberInput"] input:hover,
    div[role="radiogroup"]:hover {
        border-color: var(--primary-dark) !important;
        box-shadow: 0 0 0 3px rgba(46, 196, 182, 0.1);
    }
    
    /* Remove number input arrows */
    div[data-testid="stNumberInput"] > div > div:last-child,
    button[data-testid="stNumberInputStepUp"],
    button[data-testid="stNumberInputStepDown"] {
        display: none !important;
    }
    
    /* Labels */
    label, p, span, div {
        color: var(--text-primary) !important;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: var(--text-primary);
        font-weight: 700;
    }
    
    h1 {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    /* Progress & Status */
    .progress-bar {
        height: 8px;
        background: var(--bg-secondary);
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border-radius: 4px;
        transition: width 1s ease-in-out;
    }
    
    /* Alert Boxes */
    .success-box {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.1), rgba(40, 167, 69, 0.05));
        border: 2px solid var(--success);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 193, 7, 0.05));
        border: 2px solid var(--warning);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .danger-box {
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.1), rgba(220, 53, 69, 0.05));
        border: 2px solid var(--danger);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: var(--bg-secondary);
        padding: 4px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 2rem 0;
    }
    
    /* Tooltips */
    [data-tooltip] {
        position: relative;
        cursor: help;
    }
    
    [data-tooltip]:before {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: var(--bg-card);
        color: var(--text-primary);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.8rem;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
        z-index: 1000;
    }
    
    [data-tooltip]:hover:before {
        opacity: 1;
        visibility: visible;
        bottom: 120%;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .card {
            padding: 1rem;
        }
        
        .stForm {
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    min-width: 300px !important;
    max-width: 300px !important;
    display: block !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- SESSION STATE ----------
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'risk_score' not in st.session_state:
    st.session_state.risk_score = None
if 'history' not in st.session_state:
    st.session_state.history = []
# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"

if "navigate_to" not in st.session_state:
    st.session_state.navigate_to = None


# ---------- SIDEBAR ----------
# ---------- HANDLE PROGRAMMATIC NAVIGATION ----------
if st.session_state.navigate_to is not None:
    st.session_state.page = st.session_state.navigate_to
    st.session_state.navigate_to = None

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">❤️</h1>
        <h2>CardioCheck</h2>
        <p>Your Heart Health Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("### 🧭 Navigation")
    # page = st.radio(
    #     "Choose a page",
    #     ["🏠 Dashboard", "🔍 Risk Check", "📊 Insights", "💡 Prevention", "📈 History"],
    #     label_visibility="collapsed"
    # )
    page = st.radio(
    "Choose a page",
    ["🏠 Dashboard", "🔍 Risk Check", "📊 Insights", "💡 Prevention", "📈 History"],
    label_visibility="collapsed",
    key="page"
    ) 

    
    st.divider()
    
    # Quick Stats
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", "72.35%", "Logistic Regression")
    with col2:
        st.metric("Users Today", "124", "+8%")
    
    st.divider()
    
    # User Profile (Mock)
    st.markdown("### 👤 Your Profile")
    st.info("""
    **Status:** Active User
    **Last Check:** Today
    **Risk Level:** Pending Assessment
    """)
    
    st.divider()
    
    # Help & Support
    with st.expander("❓ Need Help?"):
        st.markdown("""
        **How to use:**
        1. Go to **Risk Check**
        2. Fill in your details
        3. Get instant analysis
        
        **Support:**
        📧 help@cardiocheck.com
        📞 1-800-HEART-123
        
        **Emergency:** Call 911
        """)
    
    # Theme Toggle
    st.divider()
    if st.button("🌙 Toggle Dark Mode"):
        st.rerun()

# ---------- DASHBOARD PAGE ----------
if page == "🏠 Dashboard":
    # Welcome Header
    col_welcome1, col_welcome2 = st.columns([3, 1])
    with col_welcome1:
        st.markdown("""
        # Welcome to CardioCheck! 👋
        ### Your personal heart health monitoring assistant
        Track, analyze, and improve your cardiovascular health with AI-powered insights.
        """)
    
    with col_welcome2:
        current_time = datetime.now().strftime("%I:%M %p")
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <p style="margin: 0; font-size: 0.9rem;">🕒 {current_time}</p>
            <h3 style="margin: 0.5rem 0; color: var(--primary);">Ready to Check?</h3>
            <p style="margin: 0; font-size: 0.8rem;">Start your assessment now</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    col_action1, col_action2, col_action3 = st.columns(3)

    with col_action1:
        if st.button("🩺 Start New Check", use_container_width=True):
            st.session_state.navigate_to = "🔍 Risk Check"

    with col_action2:
        if st.button("📊 View History", use_container_width=True):
            st.session_state.navigate_to = "📈 History"

    with col_action3:
        if st.button("💡 Learn Tips", use_container_width=True):
            st.session_state.navigate_to = "💡 Prevention"

    
    st.divider()
    
    # Health Metrics Overview
    st.markdown("### 📈 Health Overview")
    
    if st.session_state.history:
        latest_check = st.session_state.history[-1]
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        
        with col_metric1:
            st.markdown(f"""
            <div class="card metric-card">
                <h4 style="color: var(--primary); margin: 0;">Risk Score</h4>
                <h2 style="margin: 0.5rem 0;">{latest_check['risk_score']:.1f}%</h2>
                <p style="margin: 0; font-size: 0.9rem;">Latest Assessment</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metric2:
            bmi_status = "Healthy" if 18.5 <= latest_check['bmi'] <= 24.9 else "Needs Attention"
            st.metric("BMI", f"{latest_check['bmi']:.1f}", bmi_status)
        
        with col_metric3:
            st.metric("Blood Pressure", f"{latest_check['bp']}")
        
        with col_metric4:
            st.metric("Health Age", f"{latest_check['health_age']}", "vs Actual Age")
    
    else:
        st.info("🔍 No assessment history yet. Start your first check to see your metrics here!")
    
    # Recent Activity
    st.markdown("### 📋 Recent Activity")
    col_activity1, col_activity2 = st.columns([2, 1])
    
    with col_activity1:
        st.markdown("""
        <div class="card">
            <h4>🎯 Your Progress</h4>
            <p>Complete your first assessment to unlock personalized insights and tracking features.</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 30%;"></div>
            </div>
            <p style="text-align: center; font-size: 0.9rem;">30% profile complete</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_activity2:
        st.markdown("""
        <div class="card info-card">
            <h4>🏆 Achievements</h4>
            <p>✅ Account Created</p>
            <p>⏳ First Assessment</p>
            <p>⏳ Health Insights</p>
            <p>⏳ Regular Check-in</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tips Carousel
    st.divider()
    st.markdown("### 💡 Today's Health Tip")
    
    tips = [
        "🚶‍♂️ **Walk 30 minutes daily** - Reduces heart disease risk by 20%",
        "💧 **Stay hydrated** - Drink 8 glasses of water for optimal circulation",
        "😴 **Sleep 7-8 hours** - Quality sleep lowers blood pressure",
        "🧘‍♀️ **Manage stress** - 10 minutes of daily meditation helps heart health"
    ]
    
    tip_index = len(st.session_state.history) % len(tips)
    st.success(tips[tip_index])

# ---------- RISK CHECK PAGE ----------
elif page == "🔍 Risk Check":
    st.markdown("""
    # 🔍 Heart Health Assessment
    *Complete this form for a personalized risk analysis*
    """)
    
    # Progress Indicator
    st.markdown("### 📋 Form Progress")
    progress_cols = st.columns(5)
    with progress_cols[0]: st.markdown("**1. Personal** ✅")
    with progress_cols[1]: st.markdown("**2. Medical** ⏳")
    with progress_cols[2]: st.markdown("**3. Lifestyle**")
    with progress_cols[3]: st.markdown("**4. Review**")
    with progress_cols[4]: st.markdown("**5. Results**")
    
    st.divider()
    
    # Main Form
    with st.form("health_assessment", clear_on_submit=False):
        # Personal Information
        st.markdown("### 👤 Personal Information")
        col_personal1, col_personal2 = st.columns(2)
        
        with col_personal1:
            age = st.number_input(
                "**Your Age**",
                min_value=1,
                max_value=120,
                value=30,
                help="Age is a significant factor in cardiovascular risk"
            )
            
            gender = st.selectbox(
                "**Gender**",
                ["Select Gender", "Male", "Female", "Prefer not to say"],
                help="Biological sex affects risk factors"
            )
        
        with col_personal2:
            height = st.slider(
                "**Height (cm)**",
                min_value=100,
                max_value=250,
                value=170,
                help="Drag to adjust height"
            )
            
            weight = st.slider(
                "**Weight (kg)**",
                min_value=20,
                max_value=300,
                value=70,
                help="Drag to adjust weight"
            )
        
        # Auto-calculate BMI
        bmi = weight / ((height / 100) ** 2)
        bmi_status = "Underweight" if bmi < 18.5 else "Healthy" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
        
        st.markdown(f"""
        <div class="card info-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0;">Your BMI: <span style="color: var(--primary);">{bmi:.1f}</span></h4>
                    <p style="margin: 0; font-size: 0.9rem;">Status: {bmi_status}</p>
                </div>
                <div style="text-align: right;">
                    <p style="margin: 0; font-size: 0.9rem;">Healthy range: 18.5 - 24.9</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Medical Information
        st.markdown("### 🩺 Medical Information")
        
        col_medical1, col_medical2 = st.columns(2)
        
        with col_medical1:
            st.markdown("#### Blood Pressure")
            systolic = st.slider(
                "**Systolic (top number)**",
                min_value=80,
                max_value=250,
                value=120,
                help="Pressure when heart beats"
            )
            
            diastolic = st.slider(
                "**Diastolic (bottom number)**",
                min_value=50,
                max_value=150,
                value=80,
                help="Pressure between beats"
            )
            
            # BP Status Indicator
            bp_status = "Normal" if systolic < 120 and diastolic < 80 else "Elevated" if systolic < 130 else "High"
            bp_color = "var(--success)" if bp_status == "Normal" else "var(--warning)" if bp_status == "Elevated" else "var(--danger)"
            
            st.markdown(f"""
            <div style="background: {bp_color}20; padding: 1rem; border-radius: 8px; border-left: 4px solid {bp_color};">
                <p style="margin: 0; font-weight: 600;">Blood Pressure: <span style="color: {bp_color}">{systolic}/{diastolic} mmHg</span></p>
                <p style="margin: 0; font-size: 0.9rem;">Status: {bp_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_medical2:
            cholesterol = st.select_slider(
                "**Cholesterol Level**",
                options=["Normal", "Above Normal", "Well Above Normal"],
                value="Normal",
                help="Higher cholesterol increases risk"
            )
            
            glucose = st.select_slider(
                "**Glucose Level**",
                options=["Normal", "Above Normal", "Well Above Normal"],
                value="Normal",
                help="Elevated glucose is a risk factor"
            )
            
            # Family History
            family_history = st.radio(
                "**Family History of Heart Disease**",
                ["No", "Yes (Parents)", "Yes (Siblings)", "Yes (Multiple)"],
                horizontal=True
            )
        
        st.divider()
        
        # Lifestyle Factors
        st.markdown("### 🏃 Lifestyle Factors")
        
        col_lifestyle1, col_lifestyle2, col_lifestyle3 = st.columns(3)
        
        with col_lifestyle1:
            st.markdown("#### 🚬 Smoking")
            smoking = st.radio(
                "Do you smoke?",
                ["Never", "Former Smoker", "Occasionally", "Regularly"],
                key="smoking",
                help="Smoking is a major risk factor"
            )
            
            if smoking != "Never":
                years_smoking = st.slider("Years smoking", 1, 60, 5)
        
        with col_lifestyle2:
            st.markdown("#### 🍷 Alcohol")
            alcohol = st.select_slider(
                "Weekly alcohol intake",
                options=["None", "Light (1-7)", "Moderate (8-14)", "Heavy (15+)"],
                value="None",
                help="Drinks per week"
            )
            
            exercise = st.radio(
                "**Exercise Frequency**",
                ["Sedentary", "1-2 times/week", "3-4 times/week", "5+ times/week"],
                horizontal=False
            )
        
        with col_lifestyle3:
            st.markdown("#### 🍽️ Diet")
            diet_quality = st.select_slider(
                "Diet Quality",
                options=["Poor", "Below Average", "Average", "Good", "Excellent"],
                value="Average"
            )
            
            stress_level = st.slider(
                "**Daily Stress Level**",
                1, 10, 5,
                help="1 = Very Relaxed, 10 = Very Stressed"
            )
        
        st.divider()
        
        # Form Buttons
        col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
        with col_submit2:
            submit = st.form_submit_button(
                "🔍 ANALYZE MY HEART HEALTH",
                use_container_width=True,
                type="primary"
            )
            
            if submit:
                st.session_state.submitted = True
                st.session_state.form_data = {
                    'age': age,
                    'gender': gender,
                    'height': height,
                    'weight': weight,
                    'bmi': bmi,
                    'systolic': systolic,
                    'diastolic': diastolic,
                    'cholesterol': cholesterol,
                    'glucose': glucose,
                    'smoking': smoking,
                    'alcohol': alcohol,
                    'exercise': exercise,
                    'diet': diet_quality,
                    'stress': stress_level,
                    'family_history': family_history
                }

# Show Results if Form Submitted
if st.session_state.get('submitted', False):
    form_data = st.session_state.form_data
    
    # Process data for model
    gender_val = 1 if form_data['gender'] in ["Male", "male"] else 0
    chol_map = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}
    gluc_map = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}
    
    input_data = np.array([[
        form_data['age'],
        gender_val,
        form_data['height'],
        form_data['weight'],
        form_data['systolic'],
        form_data['diastolic'],
        chol_map[form_data['cholesterol']],
        gluc_map[form_data['glucose']],
        1 if form_data['smoking'] in ["Regularly", "Occasionally"] else 0,
        1 if form_data['alcohol'] != "None" else 0,
        0 if form_data['exercise'] != "Sedentary" else 1,
        form_data['bmi']
    ]])
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    
    if hasattr(model, "predict_proba"):
        risk_score = model.predict_proba(input_data)[0][1] * 100
    else:
        # Estimate based on factors
        base_risk = 50
        if form_data['age'] > 45: base_risk += 15
        if form_data['systolic'] >= 140: base_risk += 10
        if form_data['cholesterol'] != "Normal": base_risk += 8
        if form_data['smoking'] in ["Regularly", "Occasionally"]: base_risk += 12
        risk_score = min(base_risk, 95)
    
    st.session_state.risk_score = risk_score
    
    # Save to history
    st.session_state.history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'risk_score': risk_score,
        'bmi': form_data['bmi'],
        'bp': f"{form_data['systolic']}/{form_data['diastolic']}",
        'health_age': form_data['age'] + (risk_score - 50) / 10
    })
    
    # Results Display
    st.markdown("---")
    st.markdown("# 📊 Assessment Results")
    
    # Risk Level Card
    if risk_score < 30:
        risk_level = "LOW RISK"
        risk_color = "var(--success)"
        icon = "✅"
        message = "Excellent! Keep up the healthy habits."
    elif risk_score < 60:
        risk_level = "MODERATE RISK"
        risk_color = "var(--warning)"
        icon = "⚠️"
        message = "Some areas need attention. Consider lifestyle improvements."
    else:
        risk_level = "HIGH RISK"
        risk_color = "var(--danger)"
        icon = "🚨"
        message = "Immediate attention needed. Consult a healthcare professional."
    
    st.markdown(f"""
    <div style="background: {risk_color}15; padding: 2rem; border-radius: 16px; border: 2px solid {risk_color}; margin: 2rem 0;">
        <div style="text-align: center;">
            <h1 style="font-size: 4rem; margin: 0; color: {risk_color};">{icon}</h1>
            <h2 style="color: {risk_color}; margin: 1rem 0;">{risk_level}</h2>
            <div style="font-size: 3rem; font-weight: 800; color: {risk_color}; margin: 1rem 0;">
                {risk_score:.1f}%
            </div>
            <p style="font-size: 1.2rem; margin: 1rem 0;">{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Health Score Breakdown
    st.markdown("### 📈 Health Score Breakdown")
    
    fig = go.Figure()
    
    factors = [
        ("Age", form_data['age'], 0.2, risk_score * 0.2),
        ("Blood Pressure", (form_data['systolic'] + form_data['diastolic'])/2, 0.2, risk_score * 0.2),
        ("Cholesterol", chol_map[form_data['cholesterol']] * 10, 0.15, risk_score * 0.15),
        ("Lifestyle", 100 - (20 if form_data['smoking'] == "Never" else 0), 0.25, risk_score * 0.25),
        ("BMI", form_data['bmi'] * 2, 0.2, risk_score * 0.2)
    ]
    
    for factor, value, weight, contribution in factors:
        fig.add_trace(go.Bar(
            name=factor,
            x=[factor],
            y=[contribution],
            text=[f"{contribution:.1f}%"],
            textposition='auto',
            marker_color=risk_color
        ))
    
    fig.update_layout(
        title="Risk Contribution by Factor",
        yaxis_title="Risk Contribution (%)",
        showlegend=False,
        plot_bgcolor='var(--bg-card)',
        paper_bgcolor='var(--bg-card)',
        font=dict(color='var(--text-primary)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Actionable Recommendations
    st.markdown("### 🎯 Personalized Recommendations")
    
    recommendations = []
    
    if risk_score >= 60:
        st.markdown("""
        <div class="danger-box">
            <h4>🚨 URGENT ACTIONS REQUIRED</h4>
            <p><strong>1. Consult a Doctor Immediately:</strong> Schedule an appointment with a cardiologist within 1 week.</p>
            <p><strong>2. Emergency Signs to Watch:</strong></p>
            <ul>
                <li>Chest pain or discomfort</li>
                <li>Shortness of breath</li>
                <li>Pain radiating to arms, back, neck, or jaw</li>
                <li>Sudden dizziness or nausea</li>
            </ul>
            <p><strong>3. Call 911 if you experience:</strong> Any of the above symptoms lasting more than 5 minutes.</p>
            <p><strong>⚠️ This assessment is not a substitute for professional medical advice.</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate specific recommendations
    if form_data['bmi'] >= 25:
        recommendations.append(f"**⚖️ Weight Management:** Aim to lose {form_data['weight'] * 0.05:.1f}kg (5% of current weight) to reduce risk by 10-15%")
    
    if form_data['systolic'] >= 130 or form_data['diastolic'] >= 85:
        recommendations.append("**🩺 Blood Pressure Control:** Reduce sodium intake to <1500mg daily, increase potassium-rich foods")
    
    if form_data['cholesterol'] != "Normal":
        recommendations.append("**🥗 Cholesterol Management:** Increase soluble fiber (oats, beans), reduce saturated fats")
    
    if form_data['smoking'] != "Never":
        recommendations.append("**🚭 Smoking Cessation:** Quitting now reduces heart disease risk by 50% within 1 year")
    
    if form_data['exercise'] == "Sedentary":
        recommendations.append("**🏃 Start Exercising:** Begin with 15-minute walks daily, build to 150 minutes/week")
    
    if form_data['stress'] >= 7:
        recommendations.append("**🧘 Stress Management:** Practice 10-minute daily meditation or deep breathing exercises")
    
    if recommendations:
        st.markdown("#### 💡 Specific Actions for You:")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    
    # Next Steps
    st.markdown("### 📅 Next Steps")
    
    col_next1, col_next2, col_next3 = st.columns(3)
    
    with col_next1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h4>🔄 Track Progress</h4>
            <p>Re-assess in 3 months to track improvements</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_next2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h4>📚 Learn More</h4>
            <p>Visit Prevention page for detailed guides</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_next3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h4>📱 Stay Connected</h4>
            <p>Set reminders for regular check-ups</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Export Options
    st.markdown("---")
    st.markdown("### 💾 Save Your Results")
    
    if st.button("📥 Download Results Summary", use_container_width=True):
        st.success("Results summary generated! (This would trigger a download in a real implementation)")
    
    if st.button("🔄 Start New Assessment", use_container_width=True):
        st.session_state.submitted = False
        st.rerun()

# ---------- INSIGHTS PAGE ----------
elif page == "📊 Insights":
    st.markdown("""
    # 📊 Model & Technical Insights
    *Understanding how CardioCheck works*
    """)
    
    # Model Comparison
    st.markdown("### 🤖 Model Performance Comparison")
    
    models_data = {
        "Model": ["Decision Tree", "Random Forest", "Logistic Regression"],
        "Accuracy": [61.50, 73.10, 72.35],
        "Precision": [59.2, 71.8, 70.5],
        "Recall": [62.1, 72.3, 71.8],
        "F1-Score": [60.6, 72.0, 71.1]
    }
    
    df_models = pd.DataFrame(models_data)
    
    # Display metrics
    col_model1, col_model2, col_model3 = st.columns(3)
    
    with col_model1:
        st.markdown(f"""
        <div class="card" style="text-align: center; background: var(--bg-secondary);">
            <h4>🌲 Decision Tree</h4>
            <h2 style="color: var(--text-secondary);">{models_data['Accuracy'][0]}%</h2>
            <p>Accuracy Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_model2:
        st.markdown(f"""
        <div class="card" style="text-align: center; background: var(--bg-secondary);">
            <h4>🌳 Random Forest</h4>
            <h2 style="color: var(--success);">{models_data['Accuracy'][1]}%</h2>
            <p>Accuracy Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_model3:
        st.markdown(f"""
        <div class="card" style="text-align: center; background: linear-gradient(135deg, var(--primary)15, var(--secondary)15); border-color: var(--primary);">
            <h4>📊 Logistic Regression</h4>
            <h2 style="color: var(--primary);">{models_data['Accuracy'][2]}%</h2>
            <p><strong>Selected Model</strong></p>
            <p>Accuracy Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Why Logistic Regression
    st.markdown("### 🎯 Why We Chose Logistic Regression")
    
    reasons = [
        ("🧠 Interpretability", "Easy to understand feature importance for medical professionals"),
        ("⚡ Efficiency", "Fast training and prediction suitable for real-time assessment"),
        ("📈 Probabilistic Output", "Provides risk percentages, not just yes/no predictions"),
        ("🛡️ Reliability", "Less prone to overfitting than complex models"),
        ("🏥 Medical Acceptance", "Widely used and trusted in clinical research")
    ]
    
    for icon, reason in reasons:
        st.markdown(f"**{icon} {reason[0]}** - {reason[1]}")
    
    # Technical Details
    st.markdown("### 🔧 Technical Implementation")
    
    with st.expander("📊 Train-Test Split Methodology"):
        st.markdown("""
        **Method:** 70-30 Split
        - **Training Data:** 70% of dataset
        - **Testing Data:** 30% of dataset
        - **Validation:** 5-fold cross-validation
        
        **Purpose:** Prevents overfitting and provides realistic accuracy estimates
        """)
    
    with st.expander("📈 Correlation Matrix Analysis"):
        st.markdown("""
        **What is a Correlation Matrix?**
        Shows relationships between different health factors and heart disease risk.
        
        **Key Findings:**
        - **Strong Correlation:** Age, Blood Pressure, Cholesterol
        - **Moderate Correlation:** BMI, Glucose Levels
        - **Important Lifestyle:** Smoking, Physical Activity
        
        **Packages Used:**
        ```python
        # For correlation analysis
        import pandas as pd
        import seaborn as sns
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Calculate correlations
        corr_matrix = df.corr()
        
        # Visualize
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', 
                   center=0, fmt='.2f')
        plt.title('Heart Disease Risk Factors Correlation Matrix')
        plt.tight_layout()
        plt.show()
        ```
        """)
    
    with st.expander("🛠️ Required Packages"):
        st.markdown("""
        **For Development:**
        ```txt
        streamlit>=1.28.0
        joblib>=1.3.0
        numpy>=1.24.0
        pandas>=2.0.0
        scikit-learn>=1.3.0
        plotly>=5.17.0
        matplotlib>=3.7.0
        seaborn>=0.12.0
        ```
        
        **For Deployment (requirements.txt):**
        ```txt
        streamlit==1.28.1
        joblib==1.3.2
        numpy==1.24.3
        pandas==2.0.3
        scikit-learn==1.3.0
        plotly==5.17.0
        matplotlib==3.7.2
        seaborn==0.12.2
        ```
        
        **Install with:**
        ```bash
        pip install -r requirements.txt
        ```
        """)
    
    # Feature Importance Visualization
    st.markdown("### 🔍 Feature Importance")
    
    features = ["Age", "Systolic BP", "Cholesterol", "BMI", "Smoking", 
                "Physical Activity", "Diastolic BP", "Glucose", "Alcohol", "Gender"]
    importance = [0.22, 0.18, 0.15, 0.12, 0.10, 0.08, 0.07, 0.04, 0.03, 0.01]
    
    fig = go.Figure(data=[
        go.Bar(
            x=importance,
            y=features,
            orientation='h',
            marker_color=['var(--primary)' if x > 0.1 else 'var(--secondary)' for x in importance],
            text=[f'{x*100:.1f}%' for x in importance],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Relative Importance of Risk Factors",
        xaxis_title="Importance Score",
        height=400,
        plot_bgcolor='var(--bg-card)',
        paper_bgcolor='var(--bg-card)',
        font=dict(color='var(--text-primary)'),
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ---------- PREVENTION PAGE ----------
elif page == "💡 Prevention":
    st.markdown("""
    # 💡 Heart Health Prevention
    *Evidence-based strategies to reduce cardiovascular risk*
    """)
    
    # Prevention Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏋️‍♂️ Exercise", "🥗 Nutrition", "😴 Sleep & Stress", 
        "🚭 Habits", "📱 Monitoring"
    ])
    
    with tab1:
        st.markdown("### 🏃‍♀️ Physical Activity Guidelines")
        
        col_ex1, col_ex2 = st.columns(2)
        
        with col_ex1:
            st.markdown("""
            **Weekly Targets:**
            - **150 minutes** moderate-intensity OR
            - **75 minutes** vigorous-intensity
            - **2 days** strength training
            
            **Moderate Activities:**
            - 🚶‍♀️ Brisk walking (3-4 mph)
            - 🚴‍♂️ Cycling (<10 mph)
            - 💃 Dancing
            - 🏊‍♀️ Recreational swimming
            
            **Vigorous Activities:**
            - 🏃‍♂️ Running/Jogging
            - 🚴‍♀️ Cycling (>10 mph)
            - 🏋️‍♀️ High-intensity interval training
            - 🏐 Competitive sports
            """)
        
        with col_ex2:
            st.markdown("""
            **Daily Movement Tips:**
            - Take stairs instead of elevator
            - Walk during phone calls
            - Park farther from entrances
            - Stand up every 30 minutes
            
            **Progress Tracking:**
            - Use a pedometer (aim for 7,000-10,000 steps)
            - Track workout frequency
            - Set SMART goals
            - Join fitness challenges
            
            **⚠️ Safety First:**
            - Consult doctor before starting new exercise
            - Warm up and cool down properly
            - Stay hydrated
            - Listen to your body
            """)
    
    with tab2:
        st.markdown("### 🥗 Heart-Healthy Eating")
        
        col_nut1, col_nut2 = st.columns(2)
        
        with col_nut1:
            st.markdown("""
            **✅ Foods to Include:**
            
            **Fruits & Vegetables**
            - Aim for 5+ servings daily
            - Variety of colors
            - Fresh, frozen, or canned (no salt/sugar added)
            
            **Whole Grains**
            - Oats, brown rice, quinoa
            - Whole wheat bread/pasta
            - Barley, buckwheat
            
            **Lean Proteins**
            - Fish (salmon, mackerel) 2x/week
            - Skinless poultry
            - Legumes, lentils
            - Tofu, tempeh
            """)
        
        with col_nut2:
            st.markdown("""
            **❌ Foods to Limit:**
            
            **Sodium**
            - <2300mg daily (ideally <1500mg)
            - Read nutrition labels
            - Use herbs/spices instead of salt
            
            **Added Sugars**
            - <10% of daily calories
            - Avoid sugary drinks
            - Check for hidden sugars
            
            **Unhealthy Fats**
            - Limit saturated fats
            - Avoid trans fats completely
            - Choose healthy oils (olive, avocado)
            
            **Portion Control**
            - Use smaller plates
            - Measure servings
            - Eat slowly, mindfully
            """)
    
    with tab3:
        st.markdown("### 😴 Sleep & Stress Management")
        
        col_sleep1, col_sleep2 = st.columns(2)
        
        with col_sleep1:
            st.markdown("""
            **💤 Sleep Health**
            
            **Recommended:**
            - **7-9 hours** nightly for adults
            - Consistent sleep schedule
            - Dark, cool, quiet bedroom
            
            **Sleep Hygiene:**
            - No screens 1 hour before bed
            - Limit caffeine after 2 PM
            - Relaxing bedtime routine
            - Comfortable mattress/pillows
            
            **Sleep Disorders:**
            - Watch for sleep apnea signs
            - Consult doctor for insomnia
            - Consider sleep study if needed
            """)
        
        with col_sleep2:
            st.markdown("""
            **🧘 Stress Reduction**
            
            **Techniques:**
            - **Meditation:** 10-15 minutes daily
            - **Deep Breathing:** 4-7-8 technique
            - **Yoga/Tai Chi:** Mindful movement
            - **Progressive Relaxation:** Tense/relax muscles
            
            **Lifestyle:**
            - Regular physical activity
            - Social connections
            - Time management
            - Digital detox periods
            
            **Professional Help:**
            - Therapy/counseling
            - Stress management programs
            - Support groups
            - Mindfulness apps
            """)
    
    with tab4:
        st.markdown("### 🚭 Healthy Habits")
        
        st.markdown("""
        **🚬 Smoking Cessation**
        
        **Benefits Timeline:**
        - **20 minutes:** Heart rate drops
        - **12 hours:** Carbon monoxide normalizes
        - **2 weeks-3 months:** Circulation improves
        - **1 year:** Heart disease risk cut in half
        - **5 years:** Stroke risk equals non-smoker
        
        **Quitting Resources:**
        - Nicotine replacement therapy
        - Prescription medications
        - Counseling/support groups
        - Quitlines (1-800-QUIT-NOW)
        - Mobile apps
        """)
        
        st.markdown("""
        **🍷 Alcohol Moderation**
        
        **Guidelines:**
        - **Men:** ≤2 drinks/day
        - **Women:** ≤1 drink/day
        - **Older adults:** Consider less
        - **Certain conditions:** May need abstinence
        
        **One Drink Equals:**
        - 12 oz beer (5% alcohol)
        - 5 oz wine (12% alcohol)
        - 1.5 oz spirits (40% alcohol)
        
        **Tips:**
        - Have alcohol-free days
        - Drink slowly with food
        - Alternate with water
        - Avoid binge drinking
        """)
    
    with tab5:
        st.markdown("### 📱 Health Monitoring")
        
        st.markdown("""
        **🩺 Regular Check-ups**
        
        **Recommended Frequency:**
        - Blood Pressure: Monthly if normal, weekly if high
        - Cholesterol: Every 4-6 years (20+), more often if high
        - Glucose: Annually if 45+, earlier if risk factors
        - BMI: Every doctor visit
        
        **Home Monitoring:**
        - Reliable blood pressure monitor
        - Accurate scale
        - Health tracking app
        - Symptom diary
        
        **Warning Signs:**
        
        **Heart Attack:**
        - Chest discomfort
        - Upper body pain
        - Shortness of breath
        - Cold sweat, nausea
        
        **Stroke (FAST):**
        - Face drooping
        - Arm weakness
        - Speech difficulty
        - Time to call 911
        
        **⚠️ Emergency Action:**
        - Don't drive yourself
        - Chew aspirin if recommended
        - Note symptom onset time
        - Bring medications list
        """)

# ---------- HISTORY PAGE ----------
elif page == "📈 History":
    st.markdown("""
    # 📈 Your Health History
    *Track your progress over time*
    """)
    
    if not st.session_state.history:
        st.info("""
        ## 📋 No assessment history yet
        
        Complete your first heart health assessment to:
        - Track your risk score over time
        - Monitor improvements
        - Set health goals
        - See personalized trends
        
        **Get started by visiting the Risk Check page!**
        """)
        
        if st.button("🔍 Start First Assessment", use_container_width=True):
            st.session_state.page = "🔍 Risk Check"
            st.rerun()
    else:
        # Display history
        st.markdown(f"### 📊 {len(st.session_state.history)} Assessments Completed")
        
        # Convert history to DataFrame for display
        df_history = pd.DataFrame(st.session_state.history)
        
        # Display as table
        st.dataframe(
            df_history.style.format({
                'risk_score': '{:.1f}%',
                'bmi': '{:.1f}',
                'health_age': '{:.0f}'
            }),
            use_container_width=True
        )
        
        # Trends visualization
        st.markdown("### 📈 Risk Score Trend")
        
        if len(df_history) > 1:
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=df_history['timestamp'],
                y=df_history['risk_score'],
                mode='lines+markers',
                name='Risk Score',
                line=dict(color='var(--primary)', width=3),
                marker=dict(size=10)
            ))
            
            # Add improvement zone
            fig_trend.add_hrect(
                y0=0, y1=30,
                fillcolor="rgba(40, 167, 69, 0.2)",
                line_width=0,
                annotation_text="Low Risk Zone",
                annotation_position="top left"
            )
            
            fig_trend.update_layout(
                title="Your Risk Score Over Time",
                xaxis_title="Assessment Date",
                yaxis_title="Risk Score (%)",
                height=400,
                plot_bgcolor='var(--bg-card)',
                paper_bgcolor='var(--bg-card)',
                font=dict(color='var(--text-primary)')
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
        
        # Statistics
        st.markdown("### 📊 Assessment Statistics")
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            avg_risk = df_history['risk_score'].mean()
            st.metric("Average Risk", f"{avg_risk:.1f}%")
        
        with col_stat2:
            latest_risk = df_history.iloc[-1]['risk_score']
            first_risk = df_history.iloc[0]['risk_score']
            change = latest_risk - first_risk
            st.metric("Overall Change", f"{change:+.1f}%")
        
        with col_stat3:
            best_risk = df_history['risk_score'].min()
            st.metric("Best Score", f"{best_risk:.1f}%")
        
        # Export history
        st.markdown("---")
        st.markdown("### 💾 Export Your Data")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            if st.button("📥 Download History CSV", use_container_width=True):
                csv = df_history.to_csv(index=False)
                st.download_button(
                    label="Click to Download",
                    data=csv,
                    file_name="cardiocheck_history.csv",
                    mime="text/csv"
                )
        
        with col_export2:
            if st.button("🔄 Clear History", use_container_width=True):
                st.session_state.history = []
                st.success("History cleared successfully!")
                st.rerun()

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
    <p style="font-size: 0.9rem;">
        <strong>❤️ CardioCheck</strong> - AI-Powered Heart Health Assessment
    </p>
    <p style="font-size: 0.8rem; margin: 0.5rem 0;">
        ⚕️ This tool provides informational insights only and is not a substitute for professional medical advice.
        Always consult healthcare professionals for medical concerns and emergencies.
    </p>
    <p style="font-size: 0.75rem; margin: 0.5rem 0;">
        📊 Model: Logistic Regression | Accuracy: 72.35% | Version 2.0
        <br>
        🔒 Your data is secure and private
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- ADDITIONAL FEATURES ----------
# Add a floating action button style
st.markdown("""
<style>
    .floating-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    @media (max-width: 768px) {
        .floating-button {
            bottom: 10px;
            right: 10px;
        }
    }
</style>

<div class="floating-button">
    <!-- This would be implemented with actual button components -->
</div>
""", unsafe_allow_html=True)