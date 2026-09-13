import streamlit as st
import joblib

# Page config MUST be the first command
st.set_page_config(page_title="IPL Win Predictor", page_icon="🏏", layout="wide")

# Injecting Custom CSS for the Premium Stadium UI
page_bg_img = '''
<style>
/* Background Stadium Image */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Glassmorphism effect for inputs to make them readable over the image */
div[data-testid="stForm"], div[data-testid="stVerticalBlock"] > div > div {
    background: rgba(10, 20, 35, 0.85) !important;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
}

/* Making text white/gold for contrast */
h1, h2, h3, p, label {
    color: #f8f9fa !important;
}

/* Premium Prediction Button */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    border: 2px solid #ffcc00;
    border-radius: 10px;
    padding: 10px 25px;
    font-weight: bold;
    font-size: 18px;
    box-shadow: 0px 4px 15px rgba(255, 204, 0, 0.5);
    transition: 0.3s;
}
div.stButton > button:first-child:hover {
    transform: scale(1.05);
    border: 2px solid white;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load the model and encoders
model = joblib.load('ipl_winner_model.pkl')
encoders = joblib.load('ipl_encoders.pkl')

# Custom Styled Headers
st.markdown("<h1 style='text-align: center; color: #ffcc00; text-shadow: 2px 2px 4px #000000;'>🏏 IPL WIN PREDICTOR - THE SMART ENGINE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; font-weight: bold; text-shadow: 1px 1px 3px #000000;'>PREDICT THE CHASING TEAM'S CHANCES AT THE INNINGS BREAK!</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

clean_venues = sorted(list(encoders['venue'].classes_))
all_teams = sorted(list(encoders['team1'].classes_))

col1, col2 = st.columns(2)

with col1:
    team_a = st.selectbox("Team 1", all_teams)
    available_team2 = [t for t in all_teams if t != team_a]
    team_b = st.selectbox("Team 2", available_team2)
    venue = st.selectbox("Venue", clean_venues)

with col2:
    toss_winner = st.selectbox("Toss Winner", [team_a, team_b])
    toss_decision = st.selectbox("Toss Decision", encoders['toss_decision'].classes_)
    target_runs = st.number_input("Target Runs (1st Innings)", min_value=0, max_value=350, value=180, step=1)

st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1]) # Centers the button

with col_btn2:
    predict_clicked = st.button("LAUNCH PREDICTION", use_container_width=True)

if predict_clicked:
    try:
        # CRICKET LOGIC ENGINE
        if (toss_winner == team_a and toss_decision == 'bat') or (toss_winner == team_b and toss_decision == 'field'):
            batting_team = team_a
            chasing_team = team_b
        else:
            batting_team = team_b
            chasing_team = team_a
            
        t1 = encoders['team1'].transform([batting_team])[0]
        t2 = encoders['team2'].transform([chasing_team])[0]
        v = encoders['venue'].transform([venue])[0]
        tw = encoders['toss_winner'].transform([toss_winner])[0]
        td = encoders['toss_decision'].transform([toss_decision])[0]
        
        prediction = model.predict([[t1, t2, v, tw, td, target_runs]])[0]
        winner = batting_team if prediction == 1 else chasing_team
        
        # Premium Result Banner
        result_html = f"""
        <div style='background: rgba(0, 0, 0, 0.9); padding: 20px; border-radius: 15px; border: 2px solid #ffcc00; text-align: center; margin-top: 20px; box-shadow: 0px 0px 20px rgba(255, 204, 0, 0.4);'>
            <h4 style='color: #ffffff; margin-bottom: 5px;'>🏏 Match Info: {batting_team} batted first. {chasing_team} is chasing {target_runs}.</h4>
            <h2 style='color: #ffcc00; margin-top: 10px; font-size: 32px;'>🏆 PREDICTED WINNER: {winner.upper()}</h2>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {e}")