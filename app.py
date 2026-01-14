import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. UI DESIGN ---
st.set_page_config(page_title="AI Match Analyst Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #39FF14 0%, #20C20E 100%);
        color: black; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none;
    }
    div[data-baseweb="select"] > div { border: 2px solid #39FF14 !important; border-radius: 10px; }
    h1, h2, h3 { text-align: center; color: #39FF14; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Live Data Match Analyst")

# --- 2. LEAGUE DATA ---
league_data = {
    "Premier League": {
        "link": "https://www.espn.in/football/teams/_/league/ENG.1/english-premier-league",
        "teams": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton And Hove Albion", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds United", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur", "West Ham United", "Wolves"]
    },
    "Champions League": {
        "link": "https://www.espn.in/football/teams/_/league/uefa.champions",
        "teams": ["Real Madrid", "Manchester City", "Bayern Munich", "Arsenal", "Barcelona", "Inter Milan", "Liverpool", "PSG", "Atletico Madrid", "Dortmund", "AC Milan"]
    },
    "La Liga": {
        "link": "https://www.espn.in/football/teams/_/league/ESP.1/spanish-laliga",
        "teams": ["Alaves", "Athletic Club", "Atletico Madrid", "Barcelona", "Celta Vigo", "Espanyol", "Getafe", "Girona", "Real Madrid", "Real Sociedad", "Sevilla", "Valencia", "Villarreal"]
    }
}

# --- 3. INPUT SELECTION ---
c_l, c_d = st.columns(2)
with c_l:
    sel_league = st.selectbox("Select League", list(league_data.keys()))
with c_d:
    sel_date = st.date_input("Select Match Date", datetime.date.today())

st.write("---")

col1, col2 = st.columns(2)
with col1:
    home_team = st.selectbox("🏠 Home Team", league_data[sel_league]["teams"], index=0)
with col2:
    away_team = st.selectbox("🚀 Away Team", league_data[sel_league]["teams"], index=1)

# --- 4. PREDICTION LOGIC (FIXED) ---
if st.button("Generate Verified Live Analysis"):
    # API Key ရှိမရှိကို ခလုတ်နှိပ်မှ စစ်ဆေးခြင်း (ပိုမိုသေချာစေရန်)
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Error: Secrets ထဲမှာ GEMINI_API_KEY ကို ရှာမတွေ့ပါ။")
    else:
        try:
            # AI ကို ချက်ချင်း Configure လုပ်ပြီး ခေါ်ယူခြင်း
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel(
                model_name='gemini-3-flash-preview',
                tools=[{'google_search': {}}]
            )
            
            with st.spinner('AI က Website များမှ နောက်ဆုံး ၅ ပွဲရလဒ်များကို စစ်ဆေးနေပါသည်...'):
                prompt = f"""
                Verify data from {league_data[sel_league]['link']}, LiveScore.com, and Goal.com.
                Match: {home_team} vs {away_team}
                League: {sel_league}
                Date: {sel_date}

                Task:
                1. Provide the REAL results of the LAST 5 MATCHES for both teams.
                2. Analyze tactical matchup based on current form.
                3. Prediction: Score, O/U 2.5, Corners, BTTS, Yellow Cards.

                Answer in Burmese with emojis. Ensure 100% accuracy from live sources.
                """
                
                response = model.generate_content(prompt)
                st.success("ခွဲခြမ်းစိတ်ဖြာမှု ပြီးဆုံးပါပြီ!")
                st.markdown("---")
                st.markdown(f"### 📊 Professional Report: {home_team} vs {away_team}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"AI ချိတ်ဆက်မှု Error တက်သွားပါသည်: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 3.1 - Enhanced Connection Stability | Gemini 3</p>", unsafe_allow_html=True)
