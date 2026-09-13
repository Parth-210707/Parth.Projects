import streamlit as st
import joblib

# Load the new 66.36% accuracy model and clean encoders
model = joblib.load('ipl_winner_model.pkl')
encoders = joblib.load('ipl_encoders.pkl')

st.set_page_config(page_title="IPL Predictor", page_icon="🏏")
st.title("🏏 IPL Win Predictor Dashboard")
st.write("Predict the chasing team's chances at the innings break!")

# Venues are now automatically clean straight from the backend!
clean_venues = sorted(list(encoders['venue'].classes_))
all_teams = sorted(list(encoders['team1'].classes_))

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Team 1 (Batting First)", all_teams)
    
    # UI FIX 1: Team 2 cannot be the same as Team 1
    available_team2 = [t for t in all_teams if t != team1]
    team2 = st.selectbox("Team 2 (Chasing)", available_team2)
    
    venue = st.selectbox("Venue", clean_venues)

with col2:
    # UI FIX 2: Toss winner must be exactly Team 1 or Team 2
    toss_winner = st.selectbox("Toss Winner", [team1, team2])
    toss_decision = st.selectbox("Toss Decision", encoders['toss_decision'].classes_)
    target_runs = st.number_input("Target Runs (1st Innings)", min_value=0, max_value=350, value=180, step=1)

if st.button("Predict Winner"):
    try:
        t1 = encoders['team1'].transform([team1])[0]
        t2 = encoders['team2'].transform([team2])[0]
        v = encoders['venue'].transform([venue])[0]
        tw = encoders['toss_winner'].transform([toss_winner])[0]
        td = encoders['toss_decision'].transform([toss_decision])[0]
        
        prediction = model.predict([[t1, t2, v, tw, td, target_runs]])[0]
        winner = team1 if prediction == 1 else team2
        
        st.success(f"🏆 Predicted Winner (Chasing {target_runs}): **{winner}**")
    except Exception as e:
        st.error(f"Error: {e}")