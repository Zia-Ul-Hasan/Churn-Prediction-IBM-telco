import streamlit as st
import pandas as pd
import joblib
import random

st.set_page_config(layout="wide")

model = joblib.load('D:/PROjects/churn/xgb_churn_model.pkl')

st.markdown("<h1 style='text-align: center;'>Customer Churn Prediction</h1>", unsafe_allow_html=True)

# Initialize defaults once
defaults = {
    "gender": "Male",
    "senior": "No",
    "partner": "No",
    "dependents": "No",
    "phone": "Yes",
    "multiple": "No phone service",
    "internet": "DSL",
    "online_security": "No internet service",
    "online_backup": "No internet service",
    "device_protection": "No internet service",
    "tech_support": "No internet service",
    "streaming_tv": "No internet service",
    "streaming_movies": "No internet service",
    "contract": "Month-to-month",
    "paperless": "Yes",
    "payment": "Mailed check",
    "tenure": 12,
    "monthly": 70.0,
    "total": 840.0,
    "score": 50
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

def random_fill_values():
    internet = random.choice(["DSL", "Fiber optic", "No"])
    vals = {
        "gender": random.choice(["Male", "Female"]),
        "senior": random.choice(["Yes", "No"]),
        "partner": random.choice(["Yes", "No"]),
        "dependents": random.choice(["Yes", "No"]),
        "tenure": random.randint(1, 72),
        "phone": random.choice(["Yes", "No"]),
        "multiple": random.choice(["No phone service", "Yes", "No"]),
        "internet": internet,
        "contract": random.choice(["Month-to-month", "One year", "Two year"]),
        "paperless": random.choice(["Yes", "No"]),
        "payment": random.choice([
            "Mailed check", "Credit card (automatic)", "Electronic check", "Bank transfer (automatic)"
        ]),
        "monthly": round(random.uniform(25, 120), 2),
        "score": random.randint(0, 100)
    }

    # Adjust dependent fields based on internet choice
    if internet == "No":
        vals.update({
            "online_security": "No internet service",
            "online_backup": "No internet service",
            "device_protection": "No internet service",
            "tech_support": "No internet service",
            "streaming_tv": "No internet service",
            "streaming_movies": "No internet service",
        })
    else:
        vals.update({
            "online_security": random.choice(["Yes", "No"]),
            "online_backup": random.choice(["Yes", "No"]),
            "device_protection": random.choice(["Yes", "No"]),
            "tech_support": random.choice(["Yes", "No"]),
            "streaming_tv": random.choice(["Yes", "No"]),
            "streaming_movies": random.choice(["Yes", "No"]),
        })
    vals["total"] = round(vals["monthly"] * vals["tenure"], 2)

    return vals

# Button to fill random values BEFORE widgets
if st.button("Random Fill"):
    vals = random_fill_values()
    st.session_state.update(vals)
    st.experimental_rerun()

# Now render your widgets — use st.radio, st.selectbox, etc.
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Information")
    st.radio("Gender", ["Male", "Female"], key="gender")
    st.radio("Senior Citizen", ["Yes", "No"], key="senior")
    st.radio("Partner", ["Yes", "No"], key="partner")
    st.radio("Dependents", ["Yes", "No"], key="dependents")
    st.radio("Phone Service", ["Yes", "No"], key="phone")
    st.radio("Multiple Lines", ["No phone service", "Yes", "No"], key="multiple")

with col2:
    st.subheader("Services")
    st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], key="internet")

    if st.session_state.internet == "No":
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

st.subheader("Tenure and Billing")
ct1, ct2, ct3 = st.columns(3)
ct1.number_input("Tenure (Months)", min_value=0, max_value=100, key="tenure")
ct2.number_input("Monthly Charges", min_value=0.0, key="monthly")
ct3.number_input("Total Charges", min_value=0.0, key="total")

st.subheader("Billing & Contract")
bc1, bc2, bc3 = st.columns(3)
bc1.selectbox("Contract", ["Month-to-month", "One year", "Two year"], key="contract")
bc2.radio("Paperless Billing", ["Yes", "No"], key="paperless")
bc3.radio("Payment Method", [
    "Mailed check", "Credit card (automatic)", "Electronic check", "Bank transfer (automatic)"
], key="payment")

st.subheader("Customer Score")
st.slider("Churn Score", 0, 100, key="score")

# Buttons side-by-side for Random Fill and Predict Churn
b1, b2 = st.columns([1, 1])
with b1:
    # Button is here above already, so leave empty or replicate?
    pass
with b2:
    if st.button("Predict Churn"):
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
                "Mailed check": 3,
                "Credit card (automatic)": 1,
                "Electronic check": 2,
                "Bank transfer (automatic)": 0
            }[st.session_state.payment],
            'Monthly Charges': [st.session_state.monthly],
            'Total Charges': [st.session_state.total],
            'Churn Score': [st.session_state.score]
        })

        prediction = model.predict(df)

        if prediction[0] == 1:
            st.markdown(
                "<div style='background-color:green;padding:10px;border-radius:5px;color:white;text-align:center;'>"
                "<strong>Customer WILL CHURN</strong></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='background-color:red;padding:10px;border-radius:5px;color:white;text-align:center;'>"
                "<strong>Customer WILL NOT CHURN</strong></div>",
                unsafe_allow_html=True
            )
