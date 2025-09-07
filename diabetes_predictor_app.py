import streamlit as st
import pandas as pd
import joblib
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load("best_rf.joblib")
        return model
    except:
        st.error("❌ Model file not found. Please ensure 'best_rf.joblib' is in the same directory.")
        return None

model = load_model()


# BMI classification function
def classify_bmi(bmi):
    if bmi < 18.5:
        return "underweight", "#3498db"  # Blue
    elif 18.5 <= bmi < 25:
        return "normal", "#2ecc71"  # Green
    elif 25 <= bmi < 30:
        return "overweight", "#f39c12"  # Orange
    else:
        return "obesity", "#e74c3c"  # Red

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        background-color: #ff4b4b;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
    }
    .risk-low {
        background-color: #4caf50;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
    }
    .risk-moderate {
        background-color: #ff9800;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
    }
    .probability-badge {
        font-size: 2rem;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
        margin: 10px 0;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .medical-history-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 4px solid #6c757d;
    }
    .bmi-badge {
        padding: 6px 12px;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 5px;
        text-align: center;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #ccc;
        margin-left: 5px;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    /* Custom slider styling with gradient */
    div[data-testid="stSlider"] > div > div > div {
        background: linear-gradient(90deg, #2ecc71 0%, #f39c12 50%, #e74c3c 100%);
        height: 8px;
        border-radius: 4px;
    }
    div[data-testid="stSlider"] > div > div > div > div {
        background-color: #34495e;
        border: 3px solid #fff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    div[data-testid="stSlider"] > div > div > div > div:hover {
        background-color: #2c3e50;
    }
    div[data-testid="stSlider"] > div > div > div > div:focus {
        box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/diabetes.png", width=80)
    selected = option_menu(
        menu_title="Menu",
        options=["Predict", "About", "Help"],
        icons=["heart-pulse", "info-circle", "question-circle"],
        default_index=0,
    )

# Mappings for categorical features
age_mapping = {
    "18-24": 1, "25-29": 2, "30-34": 3, "35-39": 4,
    "40-44": 5, "45-49": 6, "50-54": 7, "55-59": 8,
    "60-64": 9, "65-69": 10, "70-74": 11, "75-79": 12, "80+": 13
}

income_mapping = {
    "<$10,000": 1, "$10,000-$14,999": 2, "$15,000-$19,999": 3,
    "$20,000-$24,999": 4, "$25,000-$34,999": 5, "$35,000-$49,999": 6,
    "$50,000-$74,999": 7, "$75,000+": 8
}

genhlth_mapping = {
    "Excellent": 1, "Very Good": 2, "Good": 3, "Fair": 4, "Poor": 5
}

education_mapping = {
    "Never attended school": 1, "Elementary": 2, "Some High School": 3,
    "High School Graduate": 4, "Some College": 5, "College Graduate": 6
}

# Tooltip descriptions
tooltip_descriptions = {
    "HighBP": "Diagnosed with high blood pressure",
    "HighChol": "Diagnosed with high cholesterol",
    "CholCheck": "Had cholesterol check in the past 5 years",
    "HvyAlcoholConsump": "Heavy alcohol consumption (adult men >14 drinks/week; women >7)",
    "DiffWalk": "Difficulty walking or climbing stairs",
    "PhysActivity": "Engaged in physical activity in the past 30 days (exclude job)",
    "HeartDiseaseorAttack": "Coronary heart disease or myocardial infarction",
    "Stroke": "Ever had a stroke"
}

if selected == "Predict":
    # Main header
    st.markdown('<h1 class="main-header">🩺 Diabetes Risk Prediction</h1>', unsafe_allow_html=True)
    st.markdown("### Enter patient details to assess diabetes risk")

    # UPPER DASHBOARD: Two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Health Metrics")
        
        # Colorful BMI slider with gradient
        BMI = st.slider(
            "BMI (Body Mass Index)", 
            10.0, 60.0, 25.0, 
            help="Healthy range: 18.5-24.9",
            format="%.1f"
        )
        
        # BMI classification badge
        bmi_class, bmi_color = classify_bmi(BMI)
        st.markdown(
            f'<div class="bmi-badge" style="background-color: {bmi_color}; color: white;">BMI Classification: {bmi_class.upper()}</div>',
            unsafe_allow_html=True
        )
        
        Age = st.selectbox("Age Category", list(age_mapping.keys()))
        GenHlth = st.selectbox("General Health", list(genhlth_mapping.keys()))
        
        # Colorful health sliders
        PhysHlth = st.slider(
            "Physical Health (days not good in last 30 days)", 
            0, 30, 5,
            help="0 = All days good, 30 = No days good"
        )
        
        MentHlth = st.slider(
            "Mental Health (days not good in last 30 days)", 
            0, 30, 5,
            help="0 = All days good, 30 = No days good"
        )

    with col2:
        st.markdown("### 👤 Demographic Info")
        Income = st.selectbox("Income Level", list(income_mapping.keys()))
        Education = st.selectbox("Education Level", list(education_mapping.keys()))

    # LOWER DASHBOARD: Medical History in two columns
    st.markdown("### 🏥 Medical History")
    
    # Create two columns for medical history
    med_col1, med_col2 = st.columns(2)
    
    with med_col1:
        # HighBP with tooltip
        st.markdown('<span class="tooltip">High Blood Pressure<span class="tooltiptext">Diagnosed with high blood pressure</span></span>', unsafe_allow_html=True)
        HighBP = st.radio("High Blood Pressure", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="highbp")
        
        # HighChol with tooltip
        st.markdown('<span class="tooltip">High Cholesterol<span class="tooltiptext">Diagnosed with high cholesterol</span></span>', unsafe_allow_html=True)
        HighChol = st.radio("High Cholesterol", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="highchol")
        
        # DiffWalk with tooltip
        st.markdown('<span class="tooltip">Difficulty Walking<span class="tooltiptext">Difficulty walking or climbing stairs</span></span>', unsafe_allow_html=True)
        DiffWalk = st.radio("Difficulty Walking", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="diffwalk")
        
        # HeartDiseaseorAttack with tooltip
        st.markdown('<span class="tooltip">Heart Disease or Attack<span class="tooltiptext">Coronary heart disease or myocardial infarction</span></span>', unsafe_allow_html=True)
        HeartDiseaseorAttack = st.radio("Heart Disease or Attack", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="heartdisease")
    
    with med_col2:
        # Stroke with tooltip
        st.markdown('<span class="tooltip">Stroke History<span class="tooltiptext">Ever had a stroke</span></span>', unsafe_allow_html=True)
        Stroke = st.radio("Stroke History", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="stroke")
        
        # HvyAlcoholConsump with tooltip
        st.markdown('<span class="tooltip">Heavy Alcohol Consumption<span class="tooltiptext">Heavy alcohol consumption (adult men >14 drinks/week; women >7)</span></span>', unsafe_allow_html=True)
        HvyAlcoholConsump = st.radio("Heavy Alcohol Consumption", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="alcohol")
        
        # CholCheck with tooltip
        st.markdown('<span class="tooltip">Cholesterol Check<span class="tooltiptext">Had cholesterol check in the past 5 years</span></span>', unsafe_allow_html=True)
        CholCheck = st.radio("Cholesterol Check in last 5 years", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="cholcheck")
        
        # PhysActivity with tooltip
        st.markdown('<span class="tooltip">Physically Active<span class="tooltiptext">Engaged in physical activity in the past 30 days (exclude job)</span></span>', unsafe_allow_html=True)
        PhysActivity = st.radio("Physically Active", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="physactivity")

    # Prediction button
    if st.button("🎯 Predict Diabetes Risk", type="primary", use_container_width=True):
        if model is None:
            st.error("Model not loaded. Please check the model file.")
        else:
            # Prepare input data
            feature_names = [
                'BMI', 'Age', 'Income', 'PhysHlth', 'Education', 'MentHlth', 'GenHlth',
                'HighBP', 'PhysActivity', 'HighChol', 'DiffWalk', 'HeartDiseaseorAttack',
                'Stroke', 'HvyAlcoholConsump', 'CholCheck'
            ]
            
            input_data = pd.DataFrame([[
                float(BMI),
                float(age_mapping[Age]),
                float(income_mapping[Income]),
                float(PhysHlth),
                float(education_mapping[Education]),
                float(MentHlth),
                float(genhlth_mapping[GenHlth]),
                float(HighBP),
                float(PhysActivity),
                float(HighChol),
                float(DiffWalk),
                float(HeartDiseaseorAttack),
                float(Stroke),
                float(HvyAlcoholConsump),
                float(CholCheck)
            ]], columns=feature_names)

            try:
                # Get prediction
                proba = model.predict_proba(input_data)[0][1]
                
                
                # Display results
                st.markdown("---")
                st.markdown("## 📋 Prediction Results")
                
                # Probability badge with color
                if proba >= 0.8:
                    badge_color = "#ff4b4b"
                    risk_level = "HIGH RISK"
                elif proba >= 0.5:
                    badge_color = "#ff9800" 
                    risk_level = "MODERATE RISK"
                else:
                    badge_color = "#4caf50"
                    risk_level = "LOW RISK"
                
                st.markdown(f"""
                <div style='text-align: center;'>
                    <div class='probability-badge' style='background-color: {badge_color}; color: white;'>
                        {proba:.1%} Probability
                    </div>
                    <h3>Risk Level: {risk_level}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Final prediction
                if proba >= 0.5:
                    st.markdown('<div class="risk-high"><h2>⚠️ AT RISK - Diabetes Predicted</h2><p>Recommend medical consultation and lifestyle changes</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="risk-low"><h2>✅ NO DIABETES - Low Risk</h2><p>Maintain healthy lifestyle for prevention</p></div>', unsafe_allow_html=True)
                
                # Recommendations
                st.markdown("## 💡 Recommendations")
                if proba >= 0.8:
                    st.error("""
                    - 🚨 Immediate medical consultation recommended
                    - 📋 Regular blood sugar monitoring
                    - 🏃‍♂️ Start physical activity program
                    - 🥗 Consult nutritionist for diet plan
                    - ⚕️ Regular health check-ups
                    """)
                elif proba >= 0.5:
                    st.warning("""
                    - 📋 Consider preventive screening
                    - 🏃‍♂️ Increase physical activity
                    - 🥗 Improve dietary habits
                    - ⚖️ Maintain healthy weight
                    - 🚭 Avoid smoking and limit alcohol
                    """)
                else:
                    st.success("""
                    - ✅ Continue healthy lifestyle
                    - 🏃‍♂️ Maintain regular exercise
                    - 🥗 Balanced nutrition
                    - 😊 Stress management
                    - 🩺 Annual health check-ups
                    """)
                    
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

elif selected == "About":
    st.markdown("""
    ## About Diabetes Risk Predictor
    
    This AI-powered tool predicts the risk of diabetes based on health and demographic factors.
    
    **Features:**
    - 🎯 85%+ prediction accuracy
    - 📊 Based on machine learning (Random Forest)
    - ⚕️ Clinical risk assessment
    - 💡 Personalized recommendations
    
    **Model Information:**
    - Algorithm: Random Forest with Probability Calibration
    - Accuracy: 85.34%
    - Training Data: 60,000+ samples
    - Features: 15 health and demographic factors
    """)

elif selected == "Help":
    st.markdown("""
    ## ❓ How to Use
    
    1. **Fill in the patient details** in the Predict section
    2. **Click the Predict button** to get results
    3. **Review the risk level** and recommendations
    
    **📊 Understanding Results:**
    - 🔴 High Risk (≥80%): Immediate action recommended
    - 🟠 Moderate Risk (50-79%): Preventive measures advised  
    - 🟢 Low Risk (<50%): Maintain healthy lifestyle
    
    **⚕️ Note:** This tool is for screening purposes only. Always consult a healthcare professional for medical advice.
    """)

# Footer
st.markdown("---")
st.markdown("*by TARUMT student for assignment purpose only*")