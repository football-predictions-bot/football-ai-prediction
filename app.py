import streamlit as st
import requests
import google.generativeai as genai
import datetime
import random

# --- 1. UI DESIGN & CONFIGURATION (ပုံထဲကအတိုင်း ပြင်ဆင်ခြင်း) ---
st.set_page_config(page_title="Football Predictions 2026", layout="centered")

# Custom CSS for Neon/Dark Theme
st.markdown("""
    <style>
    /* Main Background - Dark Green/Black */
    .stApp {
        background-color: #050a05; 
        color: white;
    }
    
    /* Input Fields (Selectbox & DateInput) - Neon Green Borders */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #1a1a1a;
        border: 2px solid #39FF14 !important; /* Neon Green */
        border-radius: 15px !important;
        color: white;
    }
    
    /* Text Colors inside inputs */
    div[data-baseweb="select"] span, input {
        color: white !important;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: white;
        text-align: center;
        font-family: sans-serif;
    }
    
    /* The ORANGE BUTTON (Predictions) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(180deg, #ff8c00 0%, #ff4500 100%); /* Orange Gradient */
        color: white;
        font-weight: bold;
        font-size: 20px;
        border: none;
        border-radius: 30px; /* Rounded Pill Shape */
        padding: 15px 0px;
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(255, 69, 0, 0.4);
    }
    .stButton > button:hover {
        color: white;
        background: linear-gradient(180deg, #ff4500 0%, #ff8c00 100%);
    }

    /* Output Cards */
    .match-card {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #39FF14;
    }
    
    /* VS Circle Design */
    .vs-circle {
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(90deg, #39FF14 50%, #ff4500 50%);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        margin: 0 auto;
        font-weight: bold;
        color: black;
        border: 2px solid white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BACKEND LOGIC (API & AI) ---

def get_rotated_model():
    keys = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"], st.secrets["GEMINI_KEY_3"]]
    genai.configure(api_key=random.choice(keys))
    return genai.GenerativeModel('gemini-1.5-flash')

@st.cache_data(ttl=3600)
def get_matches_by_date(league_id, date_str):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-apisports-key': st.secrets["APISPORTS_KEY"]}
    params = {'league': league_id, 'season': 2025, 'date': date_str}
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json().get('response', [])
    except:
        return []

@st.cache_data(ttl=21600)
def get_team_form(team_id):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-apisports-key': st.secrets["APISPORTS_KEY"]}
    params = {'team': team_id, 'last': 5}
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json().get('response', [])
    except:
        return []

# Data Dictionary
leagues = {"Premier League": 39, "La Liga": 140, "Serie A": 135, "Bundesliga": 78}
team_ids = {
    "Arsenal": 42, "Man City": 50, "Liverpool": 40, "Chelsea": 49, 
    "Man United": 33, "Tottenham": 47, "Aston Villa": 66, "Newcastle": 34,
    "Real Madrid": 541, "Barcelona": 529, "Bayern Munich": 157
}

# --- 3. UI LAYOUT (ပုံထဲက Layout အတိုင်း) ---

st.title("Football Predictions")

# --- SECTION 1: MATCH FINDER ---
st.markdown("### Match Finder")
col1, col2 = st.columns(2)
with col1:
    sel_league = st.selectbox("Select League", list(leagues.keys()))
with col2:
    sel_date = st.date_input("Select Date", datetime.date.today())

# --- SECTION 2: TEAM SELECTOR (Split Design) ---
st.write("") # Spacer
st.markdown("<h3 style='text-align:center; color:#39FF14;'>Select Team</h3>", unsafe_allow_html=True)

# Creating the "VS" visual layout
c1, c2, c3 = st.columns([5, 2, 5])

with c1:
    st.markdown("<div style='text-align:center; font-weight:bold; color:#39FF14;'>HOME TEAM</div>", unsafe_allow_html=True)
    home_team = st.selectbox("Home", list(team_ids.keys()), label_visibility="collapsed")

with c2:
    st.markdown("<br><div class='vs-circle'>VS</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div style='text-align:center; font-weight:bold; color:#ff4500;'>AWAY TEAM</div>", unsafe_allow_html=True)
    away_team = st.selectbox("Away", list(team_ids.keys()), index=1, label_visibility="collapsed")

# --- SECTION 3: THE BIG ORANGE BUTTON ---
if st.button("Predictions"):
    
    # 1. Date Search Result
    date_str = sel_date.strftime('%Y-%m-%d')
    with st.spinner('Checking Schedule...'):
        matches = get_matches_by_date(leagues[sel_league], date_str)
        if matches:
            st.success(f"Matches found for {sel_league} on {date_str}")
        else:
            st.warning(f"No matches scheduled for {sel_league} on {date_str}")

    # 2. Team Analysis (API + AI)
    with st.spinner(f'Analyzing {home_team} vs {away_team}...'):
        h_form = get_team_form(team_ids[home_team])
        a_form = get_team_form(team_ids[away_team])
        
        if h_form and a_form:
            # Preparing Data for AI
            summary = f"Analysis for {home_team} vs {away_team}:\n"
            summary += f"\n{home_team} Last 5 Matches:\n"
            for m in h_form:
                summary += f"{m['teams']['home']['name']} {m['goals']['home']}-{m['goals']['away']} {m['teams']['away']['name']}\n"
            
            summary += f"\n{away_team} Last 5 Matches:\n"
            for m in a_form:
                summary += f"{m['teams']['home']['name']} {m['goals']['home']}-{m['goals']['away']} {m['teams']['away']['name']}\n"
            
            # AI Prediction
            try:
                model = get_rotated_model()
                prompt = f"You are a football expert. Based ONLY on these results:\n{summary}\nPredict the winner and score for the upcoming match between {home_team} and {away_team}. Write in Burmese."
                response = model.generate_content(prompt)
                
                # Display Result Card
                st.markdown(f"""
                <div class='match-card'>
                    <h3 style='color:#39FF14;'>🤖 AI Prediction</h3>
                    <p>{response.text}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show Raw Data (Last 5 Games)
                st.write("---")
                c_a, c_b = st.columns(2)
                with c_a:
                    st.caption(f"{home_team} Recent Form")
                    for m in h_form:
                        st.text(f"{m['goals']['home']}-{m['goals']['away']} vs {m['teams']['away']['name'] if m['teams']['home']['name'] == home_team else m['teams']['home']['name']}")
                with c_b:
                    st.caption(f"{away_team} Recent Form")
                    for m in a_form:
                        st.text(f"{m['goals']['home']}-{m['goals']['away']} vs {m['teams']['away']['name'] if m['teams']['home']['name'] == away_team else m['teams']['home']['name']}")

            except Exception as e:
                st.error("AI Limit Reached. Please wait a moment.")
        else:
            st.error("Could not fetch team data. Please check API Key.")

# Footer
st.markdown("<br><center><small style='color:gray'>Powered by Gemini & API-Sports</small></center>", unsafe_allow_html=True)
