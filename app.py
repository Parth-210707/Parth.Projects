import streamlit as st
import joblib

# Load the model and encoders
model = joblib.load('ipl_winner_model.pkl')
encoders = joblib.load('ipl_encoders.pkl')

st.set_page_config(page_title="IPL Predictor", page_icon="🏏")
st.title("🏏 IPL Win Predictor Dashboard")
st.write("Predict the chasing team's chances at the innings break!")

clean_venues = sorted(list(encoders['venue'].classes_))
all_teams = sorted(list(encoders['team1'].classes_))

col1, col2 = st.columns(2)

with col1:
    # Removed the hardcoded "(Batting First)" label
    team_a = st.selectbox("Team 1", all_teams)
    
    available_team2 = [t for t in all_teams if t != team_a]
    team_b = st.selectbox("Team 2", available_team2)
    
    venue = st.selectbox("Venue", clean_venues)

with col2:
    toss_winner = st.selectbox("Toss Winner", [team_a, team_b])
    toss_decision = st.selectbox("Toss Decision", encoders['toss_decision'].classes_)
    target_runs = st.number_input("Target Runs (1st Innings)", min_value=0, max_value=350, value=180, step=1)

if st.button("Predict Winner"):
    try:
        # CRICKET LOGIC ENGINE: Figure out who is actually batting first based on user inputs
        if (toss_winner == team_a and toss_decision == 'bat') or (toss_winner == team_b and toss_decision == 'field'):
            batting_team = team_a
            chasing_team = team_b
        else:
            batting_team = team_b
            chasing_team = team_a
            
        # Pass the correctly assigned batting & chasing teams to the model
        t1 = encoders['team1'].transform([batting_team])[0]
        t2 = encoders['team2'].transform([chasing_team])[0]
        v = encoders['venue'].transform([venue])[0]
        tw = encoders['toss_winner'].transform([toss_winner])[0]
        td = encoders['toss_decision'].transform([toss_decision])[0]
        
        prediction = model.predict([[t1, t2, v, tw, td, target_runs]])[0]
        winner = batting_team if prediction == 1 else chasing_team
        
        st.info(f"🏏 **Match Info:** {batting_team} batted first. {chasing_team} is chasing {target_runs}.")
        st.success(f"🏆 Predicted Winner: **{winner}**")
        
    except Exception as e:
        st.error(f"Error: {e}")