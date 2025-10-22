import streamlit as st
import pandas as pd
import joblib

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for compact layout
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    h1 {
        font-size: 2.2rem;
        margin-bottom: 1rem;
    }
    h3 {
        font-size: 1rem;
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .stRadio > label, .stSelectbox > label, .stNumberInput > label, .stSlider > label {
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.3rem;
    }
    hr {
        margin: 0.5rem 0;
    }
    [data-testid="stToolbar"], header, #MainMenu, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

model = joblib.load('D:/PROjects/churn/xgb_churn_model.pkl')

st.markdown("<h1 style='text-align: center;'> Customer Churn Prediction</h1>", unsafe_allow_html=True)

# Initialize defaults once
defaults = {
    "gender": "Male", "senior": "No", "partner": "No", "dependents": "No",
    "phone": "Yes", "multiple": "No phone service", "internet": "DSL",
    "online_security": "No internet service", "online_backup": "No internet service",
    "device_protection": "No internet service", "tech_support": "No internet service",
    "streaming_tv": "No internet service", "streaming_movies": "No internet service",
    "contract": "Month-to-month", "paperless": "Yes", "payment": "Mailed check",
    "tenure": 12, "monthly": 70.0, "total": 840.0, "score": 50
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

st.markdown("---")

# Main layout - 3 equal columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Customer Demographics")
    st.radio("Gender", ["Male", "Female"], key="gender", horizontal=True)
    st.radio("Senior Citizen", ["Yes", "No"], key="senior", horizontal=True)
    st.radio("Partner", ["Yes", "No"], key="partner", horizontal=True)
    st.radio("Dependents", ["Yes", "No"], key="dependents", horizontal=True)
    st.markdown("---")
    st.markdown("### Phone Services")
    st.radio("Phone Service", ["Yes", "No"], key="phone", horizontal=True)

    # Auto-control Multiple Lines if Phone Service = No
    if st.session_state.phone == "No":
        st.session_state.multiple = "No phone service"
        st.selectbox("Multiple Lines", ["No phone service"], key="multiple", disabled=True)
    else:
        st.selectbox("Multiple Lines", ["No phone service", "Yes", "No"], key="multiple")

with col2:
    st.markdown("### Internet Services")
    st.selectbox("Internet Type", ["DSL", "Fiber optic", "No"], key="internet")

    # Auto-control all Internet dependent fields if Internet = No
    if st.session_state.internet == "No":
        for field in ["online_security", "online_backup", "device_protection",
                      "tech_support", "streaming_tv", "streaming_movies"]:
            st.session_state[field] = "No internet service"
        st.selectbox("Online Security", ["No internet service"], key="online_security", disabled=True)
        st.selectbox("Online Backup", ["No internet service"], key="online_backup", disabled=True)
        st.selectbox("Device Protection", ["No internet service"], key="device_protection", disabled=True)
        st.selectbox("Tech Support", ["No internet service"], key="tech_support", disabled=True)
        st.selectbox("Streaming TV", ["No internet service"], key="streaming_tv", disabled=True)
        st.selectbox("Streaming Movies", ["No internet service"], key="streaming_movies", disabled=True)
    else:
        st.selectbox("Online Security", ["Yes", "No"], key="online_security")
        st.selectbox("Online Backup", ["Yes", "No"], key="online_backup")
        st.selectbox("Device Protection", ["Yes", "No"], key="device_protection")
        st.selectbox("Tech Support", ["Yes", "No"], key="tech_support")
        st.selectbox("Streaming TV", ["Yes", "No"], key="streaming_tv")
        st.selectbox("Streaming Movies", ["Yes", "No"], key="streaming_movies")

with col3:
    st.markdown("### Billing, Contract & Charges")
    st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], key="contract")
    st.radio("Paperless Billing", ["Yes", "No"], key="paperless", horizontal=True)
    st.selectbox("Payment Method", [
        "Mailed check", "Credit card (automatic)", "Electronic check", "Bank transfer (automatic)"
    ], key="payment")
    st.markdown("**Charges & Tenure**")
    st.number_input("Tenure (Months)", min_value=0, max_value=100, key="tenure")
    st.number_input("Monthly Charges ($)", min_value=0.0, key="monthly", format="%.2f")
    st.number_input("Total Charges ($)", min_value=0.0, key="total", format="%.2f")

# Churn Score
st.slider("Churn Score", 0, 100, key="score")

# Single Predict button
st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button(" Predict Churn", use_container_width=True, type="primary")

# Prediction logic
if predict_btn:
    df = pd.DataFrame({
        'Gender': [1 if st.session_state.gender == "Male" else 0],
        'Senior Citizen': [1 if st.session_state.senior == "Yes" else 0],
        'Partner': [1 if st.session_state.partner == "Yes" else 0],
        'Dependents': [1 if st.session_state.dependents == "Yes" else 0],
        'Tenure Months': [st.session_state.tenure],
        'Phone Service': [1 if st.session_state.phone == "Yes" else 0],
        'Multiple Lines': [{"No phone service": 2, "Yes": 1, "No": 0}[st.session_state.multiple]],
        'Internet Service': [{"DSL": 0, "Fiber optic": 1, "No": 2}[st.session_state.internet]],
        'Online Security': [{"No": 0, "No internet service": 1, "Yes": 2}[st.session_state.online_security]],
        'Online Backup': [{"No": 0, "No internet service": 1, "Yes": 2}[st.session_state.online_backup]],
        'Device Protection': [{"No": 0, "No internet service": 1, "Yes": 2}[st.session_state.device_protection]],
        'Tech Support': [{"No": 0, "No internet service": 1, "Yes": 2}[st.session_state.tech_support]],
        'Streaming TV': [{"No": 0, "No internet service": 1, "Yes": 2}[st.session_state.streaming_tv]],
        'Streaming Movies': [{"No": 0, "No internet service": 1, "Yes": 2}[st.session_state.streaming_movies]],
        'Contract': [{"Month-to-month": 0, "One year": 1, "Two year": 2}[st.session_state.contract]],
        'Paperless Billing': [1 if st.session_state.paperless == "Yes" else 0],
        'Payment Method': {
            "Mailed check": 3, "Credit card (automatic)": 1,
            "Electronic check": 2, "Bank transfer (automatic)": 0
        }[st.session_state.payment],
        'Monthly Charges': [st.session_state.monthly],
        'Total Charges': [st.session_state.total],
        'Churn Score': [st.session_state.score]
    })

    prediction = model.predict(df)

    st.markdown("---")
    if prediction[0] == 1:
        st.markdown(
            "<div style='background-color:#dc2626;padding:20px;border-radius:10px;color:white;"
            "text-align:center;font-size:1.6rem;'>"
            "<strong>Churn Risk: High</strong><br>"
            "The model predicts a high likelihood of customer attrition.</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='background-color:#16a34a;padding:20px;border-radius:10px;color:white;"
            "text-align:center;font-size:1.6rem;'>"
            "<strong>Churn Risk: Low</strong><br>"
            "The model predicts a low likelihood of customer attrition.</div>",
            unsafe_allow_html=True
    )
