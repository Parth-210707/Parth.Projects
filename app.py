import streamlit as st
import joblib
import pandas as pd

# Load the exported model and encoders
model = joblib.load('ipl_winner_model.pkl')
encoders = joblib.load('ipl_encoders.pkl')

st.set_page_config(page_title="IPL Predictor", page_icon="🏏")
st.title("🏏 IPL Win Predictor Dashboard")
st.write("Predict the chasing team's chances at the innings break!")

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Team 1 (Batting First)", encoders['team1'].classes_)
    venue = st.selectbox("Venue", encoders['venue'].classes_)
    toss_decision = st.selectbox("Toss Decision", encoders['toss_decision'].classes_)

with col2:
    team2 = st.selectbox("Team 2 (Chasing)", encoders['team2'].classes_)
    toss_winner = st.selectbox("Toss Winner", encoders['toss_winner'].classes_)
    target_runs = st.number_input("Target Runs (1st Innings Score)", min_value=0, max_value=300, value=180, step=1)

if st.button("Predict Winner"):
    try:
        # Encode inputs back to numbers
        t1 = encoders['team1'].transform([team1])[0]
        t2 = encoders['team2'].transform([team2])[0]
        v = encoders['venue'].transform([venue])[0]
        tw = encoders['toss_winner'].transform([toss_winner])[0]
        td = encoders['toss_decision'].transform([toss_decision])[0]
        
        # Make Prediction
        prediction = model.predict([[t1, t2, v, tw, td, target_runs]])[0]
        winner = team1 if prediction == 1 else team2
        
        st.success(f"🏆 Predicted Winner (Chasing {target_runs}): **{winner}**")
    except Exception as e:
        st.error(f"Error: {e}")