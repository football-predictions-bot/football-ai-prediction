import streamlit as st
import requests
import google.generativeai as genai
import datetime
import random

# --- 1. UI CONFIGURATION (Neon Style) ---
st.set_page_config(page_title="Football Predictions Bot 2026", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    
    /* Input Boxes */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #111 !important;
        border: 2px solid #39FF14 !important;
        border-radius: 12px !important;
    }
    
    /* Green Button (Check Matches) */
    div.stButton > button:first-child {
        background-color: #39FF14 !important;
        color: black !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 10px !important;
    }

    /* Orange Button (Generate Predictions) */
    div.stButton > button:last-child {
        background: linear-gradient(180deg, #FF8C00 0%, #FF4500 100%) !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 20px !important;
        height: 60px !important;
    }

    .match-box {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #39FF14;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API FUNCTIONS ---

def get_rotated_model():
    keys = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"], st.secrets["GEMINI_KEY_3"]]
    genai.configure(api_key=random.choice(keys))
    return genai.GenerativeModel('gemini-1.5-flash')

def get_live_matches(league_id, date_str):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-apisports-key': st.secrets["APISPORTS_KEY"]}
    # ၂၀၂၅-၂၆ ရာသီအတွက် season ကို ၂၀၂၅ လို့ထားရပါမယ်
    params = {'league': league_id, 'season': 2025, 'date': date_str}
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json().get('response', [])
    except:
        return []

# --- 3. UI LAYOUT ---

st.title("Football Predictions")

# Match Finder Section
leagues = {"Premier League": 39, "La Liga": 140, "Serie A": 135, "Bundesliga": 78, "Champions League": 2}
c1, c2 = st.columns(2)
with c1:
    sel_league = st.selectbox("Select League", list(leagues.keys()))
with c2:
    sel_date = st.date_input("Select Date", datetime.date.today())

# Check Matches Button
if st.button("Check Matches Now"):
    with st.spinner('ပွဲစဉ်များ ရှာဖွေနေပါသည်...'):
        matches = get_live_matches(leagues[sel_league], sel_date.strftime('%Y-%m-%d'))
        if matches:
            for m in matches:
                st.markdown(f"""
                <div class='match-box'>
                    <b>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</b><br>
                    <small>Time: {m['fixture']['date'][11:16]} UTC</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("ယနေ့အတွက် ပွဲစဉ်များ ရှာမတွေ့ပါ။")

st.write("---")

# Prediction Section
st.markdown("<h3 style='color:#39FF14; text-align:center;'>Select Team for Analysis</h3>", unsafe_allow_html=True)
team_list = ["Arsenal", "Man City", "Liverpool", "Real Madrid", "Barcelona", "Man Utd", "Chelsea", "Spurs", "Inter Milan", "Bayern Munich"]
col1, col2 = st.columns(2)
with col1:
    home = st.selectbox("HOME TEAM", team_list, key="h")
with col2:
    away = st.selectbox("AWAY TEAM", team_list, index=1, key="a")

if st.button("Generate Predictions"):
    model = get_rotated_model()
    with st.spinner('AI ဖြင့် ခွဲခြမ်းစိတ်ဖြာနေပါသည်...'):
        try:
            prompt = f"Predict the score and winner for {home} vs {away} in {sel_league}. Write in Burmese."
            response = model.generate_content(prompt)
            st.success("Analysis Complete!")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
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
