import streamlit as st
import joblib

# 1. Page Configuration (Must be first)
st.set_page_config(page_title="IPL Predictor", page_icon="🏏", layout="centered")

# 2. THE CSS MAGIC INJECTION (STADIUM BG + GLASSMORPHISM + BIG GREEN BALL CURSOR)
premium_styling = """
<style>
/* Import custom font from Google */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

/* Apply custom font and BIG GREEN BALL CURSOR */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    /* Custom SVG Cursor: Badi Green Ball (48x48 size) */
    cursor: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 48 48'%3E%3Ccircle cx='24' cy='24' r='22' fill='%2384cc16' stroke='%23000' stroke-width='2'/%3E%3Cpath d='M 12 5 A 18 18 0 0 0 12 43' fill='none' stroke='%23fff' stroke-width='2'/%3E%3Cpath d='M 36 5 A 18 18 0 0 1 36 43' fill='none' stroke='%23fff' stroke-width='2'/%3E%3C/svg%3E") 24 24, auto !important;
}

/* EPIC STADIUM BACKGROUND WITH DARK OVERLAY FOR READABILITY */
.stApp {
    background: linear-gradient(rgba(10, 20, 30, 0.6), rgba(0, 0, 0, 0.9)), 
                url('https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&q=80&w=2000');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    color: white;
}

/* Title Styling with Gold text and shadow */
h1 {
    text-align: center;
    font-weight: 800 !important;
    color: #FFD700 !important;
    text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.4);
    margin-bottom: -10px;
}

/* Subtitle Styling */
.subtitle {
    text-align: center;
    color: #A0EBCB;
    font-weight: 400;
    margin-bottom: 30px;
    font-size: 18px;
    text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
}

/* Make Dropdowns and Inputs look like Glass over the Stadium */
div[data-baseweb="select"] > div, input[type="number"] {
    background: rgba(15, 25, 40, 0.75) !important;
    border: 1px solid rgba(255, 215, 0, 0.3) !important;
    backdrop-filter: blur(8px) !important;
    border-radius: 8px !important;
    color: white !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.5), 0 4px 10px rgba(0,0,0,0.3);
}

/* Change Dropdown text color to gold */
.stSelectbox label, .stNumberInput label {
    color: #FFD700 !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
}

/* Glowing Neon Button */
div.stButton > button {
    background: linear-gradient(90deg, #f12711, #f5af19) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 15px 30px !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    letter-spacing: 2px !important;
    box-shadow: 0 10px 20px rgba(245, 175, 25, 0.4) !important;
    transition: all 0.3s ease !important;
    width: 100%;
    margin-top: 20px;
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 25px rgba(245, 175, 25, 0.7) !important;
}

/* Hide Streamlit footer */
footer {visibility: hidden;}
</style>
"""
st.markdown(premium_styling, unsafe_allow_html=True)

# 3. Load Models
model = joblib.load('ipl_winner_model.pkl')
encoders = joblib.load('ipl_encoders.pkl')

# 4. Custom UI Headers
st.title("🏏 IPL Win Predictor")
st.markdown("<p class='subtitle'>Predict the chasing team's chances at the innings break!</p>", unsafe_allow_html=True)

# 5. UI Elements
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

# 6. Prediction Logic
if st.button("LAUNCH PREDICTION"):
    try:
        # Cricket logic engine
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
        
        # Premium Custom Result Banner
        result_html = f"""
        <div style="background: rgba(10, 20, 30, 0.85); border-left: 8px solid #FFD700; border-radius: 10px; padding: 25px; margin-top: 30px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8); backdrop-filter: blur(10px);">
            <p style="color: #A0EBCB; font-size: 16px; margin: 0; font-weight: 600; letter-spacing: 1px;">CRICKET ENGINE ANALYSIS</p>
            <h2 style="color: #ffffff; font-size: 32px; font-weight: 800; margin: 10px 0; text-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);">🏆 PREDICTED WINNER: <span style="color: #FFD700;">{winner.upper()}</span></h2>
            <p style="color: #ccc; font-size: 14px; margin: 0;"><strong>Match Info:</strong> {batting_team} batted first. {chasing_team} is chasing {target_runs}.</p>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {e}")