import streamlit as st
import pandas as pd
import pickle
from auth.auth_utils import register_user, login_user
from utils import preprocess_input

@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        return pickle.load(file)

model = load_model()

st.set_page_config(page_title="Injury Prediction App", page_icon="🏃‍♂️", layout="centered")
st.title("🏃‍♂️ Injury Prediction & Prevention")

# Authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

auth_mode = st.sidebar.radio("🔐 Auth", ["Login", "Register"])
if auth_mode == "Register":
    st.sidebar.subheader("📝 Register")
    new_user = st.sidebar.text_input("Username")
    new_pass = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Register"):
        if register_user(new_user, new_pass):
            st.sidebar.success("✅ Registered! Now login.")
        else:
            st.sidebar.error("⚠️ User already exists.")
elif auth_mode == "Login":
    st.sidebar.subheader("🔑 Login")
    user = st.sidebar.text_input("Username")
    pwd = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if login_user(user, pwd):
            st.session_state.logged_in = True
            st.session_state.username = user
            st.sidebar.success(f"✅ Welcome {user}!")
        else:
            st.sidebar.error("❌ Invalid credentials.")

if st.session_state.logged_in:
    st.success(f"Welcome, {st.session_state.username}!")

    with st.form("athlete_form"):
        st.subheader("📊 Enter Athlete Data")
        distance = st.number_input("Distance Covered (km)", 0.0, 100.0, 10.0)
        intensity = st.slider("Intensity (1-10)", 1, 10, 5)
        frequency = st.number_input("Sessions per Week", 0, 14, 3)
        duration = st.number_input("Duration per Session (min)", 0, 300, 60)
        prev_injuries = st.selectbox("Previous Injuries", ["No", "Yes"])
        chronic_cond = st.selectbox("Chronic Conditions", ["No", "Yes"])
        submitted = st.form_submit_button("🔍 Predict Injury Risk")

    if submitted:
        input_df = preprocess_input(distance, intensity, frequency, duration, prev_injuries, chronic_cond)
        risk = model.predict_proba(input_df)[0][1]
        st.markdown(f"### 🩺 Predicted Injury Risk Score: `{risk:.2f}`")
        if risk >= 0.7:
            st.error("⚠️ High Injury Risk. Modify training plan.")
        elif risk >= 0.4:
            st.warning("⚠️ Moderate Risk. Monitor regularly.")
        else:
            st.success("✅ Low Risk. Keep training smart!")
else:
    st.info("Login or Register to access the app.")
