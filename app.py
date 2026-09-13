import streamlit as st
import joblib

st.set_page_config(page_title="IPL Smart Engine", page_icon="🏏", layout="wide")

# ADVANCED CSS INJECTION FOR PREMIUM GAME-LIKE UI
premium_css = """
<style>
    /* Full screen stadium background */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.7)), url("https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Arial', sans-serif;
    }
    
    /* Top Title Banner */
    .title-banner {
        background: linear-gradient(180deg, #1c283d 0%, #0d1624 100%);
        border-top: 3px solid #7892b5;
        border-bottom: 3px solid #7892b5;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.8);
        margin-bottom: 20px;
    }
    .title-text { color: #ffffff; font-size: 32px; font-weight: 900; text-transform: uppercase; font-style: italic; letter-spacing: 2px; text-shadow: 2px 2px 4px #000; margin: 0; }
    .subtitle-text { color: #a9b5c7; font-size: 14px; font-weight: bold; margin-top: 5px; }

    /* Left and Right Panels */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background: linear-gradient(145deg, rgba(20,35,60,0.85) 0%, rgba(10,20,35,0.95) 100%);
        border: 2px solid #3c5478;
        border-radius: 15px;
        padding: 20px;
        box-shadow: inset 0px 0px 15px rgba(0,0,0,0.8), 0px 15px 25px rgba(0,0,0,0.6);
    }

    /* Input Field Styling (Selectbox & Number Input) */
    .stSelectbox label, .stNumberInput label {
        color: #e0e6ed !important;
        font-weight: bold;
        font-size: 15px;
    }
    div[data-baseweb="select"] > div, input[type="number"] {
        background: linear-gradient(90deg, #172a45 0%, #1e3a5f 100%) !important;
        border: 1px solid #ffcc00 !important; /* Golden Border */
        border-radius: 8px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: inset 0px 2px 5px rgba(0,0,0,0.5);
    }
    
    /* Center Button Styling */
    .stButton > button {
        background: linear-gradient(180deg, #2c538e 0%, #0d2149 100%);
        color: #ffcc00;
        border: 2px solid #ffcc00;
        border-radius: 8px;
        padding: 15px 40px;
        font-size: 20px;
        font-weight: 900;
        letter-spacing: 1px;
        box-shadow: 0px 0px 20px rgba(255, 204, 0, 0.4), inset 0px 2px 4px rgba(255,255,255,0.3);
        transition: all 0.3s ease;
        display: block;
        margin: 0 auto;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(180deg, #3a6ab3 0%, #15326b 100%);
        transform: translateY(-2px);
        box-shadow: 0px 0px 30px rgba(255, 204, 0, 0.7);
        color: white;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(premium_css, unsafe_allow_html=True)

# LOAD MODEL
model = joblib.load('ipl_winner_model.pkl')
encoders = joblib.load('ipl_encoders.pkl')

# CUSTOM TITLE BANNER
st.markdown("""
<div class="title-banner">
    <p class="title-text">IPL WIN PREDICTOR - THE SMART ENGINE</p>
    <p class="subtitle-text">PREDICT THE CHASING TEAM'S CHANCES AT THE INNINGS BREAK!</p>
</div>
""", unsafe_allow_html=True)

clean_venues = sorted(list(encoders['venue'].classes_))
all_teams = sorted(list(encoders['team1'].classes_))

# TWO PANELS
col1, col2 = st.columns(2, gap="large")

with col1:
    team_a = st.selectbox("Team 1", all_teams)
    available_team2 = [t for t in all_teams if t != team_a]
    team_b = st.selectbox("Team 2", available_team2)
    venue = st.selectbox("Venue", clean_venues)

with col2:
    toss_winner = st.selectbox("Toss Winner", [team_a, team_b])
    toss_decision = st.selectbox("Toss Decision", encoders['toss_decision'].classes_)
    target_runs = st.number_input("Target Runs (1st Innings)", min_value=0, max_value=350, value=180, step=1)

st.write("") 
st.write("")

# CENTER BUTTON
col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
with col_b2:
    predict_clicked = st.button("LAUNCH PREDICTION")

# PREDICTION LOGIC
if predict_clicked:
    try:
        if (toss_winner == team_a and toss_decision == 'bat') or (toss_winner == team_b and toss_decision == 'field'):
            batting_team, chasing_team = team_a, team_b
        else:
            batting_team, chasing_team = team_b, team_a
            
        t1 = encoders['team1'].transform([batting_team])[0]
        t2 = encoders['team2'].transform([chasing_team])[0]
        v = encoders['venue'].transform([venue])[0]
        tw = encoders['toss_winner'].transform([toss_winner])[0]
        td = encoders['toss_decision'].transform([toss_decision])[0]
        
        prediction = model.predict([[t1, t2, v, tw, td, target_runs]])[0]
        winner = batting_team if prediction == 1 else chasing_team
        
        # PREMIUM WINNER BANNER
        st.markdown(f"""
        <div style="background: linear-gradient(180deg, #0d1624 0%, #1a273b 100%); border: 3px solid #ffcc00; border-radius: 12px; padding: 25px; text-align: center; margin-top: 30px; box-shadow: 0px 10px 30px rgba(0,0,0,0.9), 0px 0px 20px rgba(255,204,0,0.3);">
            <p style="color: #a9b5c7; font-size: 16px; font-weight: bold; letter-spacing: 1px; margin-bottom: 5px;">PREDICTED WINNER</p>
            <h2 style="color: #ffffff; font-size: 38px; font-weight: 900; margin: 0; text-shadow: 0px 4px 10px rgba(0,0,0,0.8);"><span style="color:#ffcc00">🏆</span> {winner.upper()} <span style="color:#ffcc00">🏆</span></h2>
            <p style="color: #ffcc00; font-size: 13px; margin-top: 15px;">**Match Info:** {batting_team} batted first. {chasing_team} is chasing {target_runs}.</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {e}")