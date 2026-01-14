import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. AI SETUP (GEMINI 3 FLASH) ---
def setup_ai():
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return None
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Google Search Tool ပါဝင်သော Gemini 3 Flash Preview
        return genai.GenerativeModel(
            model_name='gemini-3-flash-preview',
            tools=[{'google_search': {}}]
        )
    except:
        return None

model = setup_ai()

# --- 2. LEAGUE DATA WITH OFFICIAL LINKS ---
league_data = {
    "Premier League": {
        "link": "https://www.espn.in/football/teams/_/league/ENG.1/english-premier-league",
        "teams": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton And Hove Albion", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds United", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers"]
    },
    "Champions League": {
        "link": "https://www.espn.in/football/teams/_/league/uefa.champions",
        "teams": ["Real Madrid", "Manchester City", "Bayern Munich", "Arsenal", "Barcelona", "Inter Milan", "Liverpool", "PSG", "Bayer Leverkusen", "Atletico Madrid", "Dortmund", "AC Milan", "Aston Villa", "Sporting CP", "Benfica", "Monaco"]
    },
    "La Liga": {
        "link": "https://www.espn.in/football/teams/_/league/ESP.1/spanish-laliga",
        "teams": ["Alaves", "Athletic Club", "Atletico Madrid", "Barcelona", "Celta Vigo", "Espanyol", "Getafe", "Girona", "Las Palmas", "Leganes", "Mallorca", "Osasuna", "Rayo Vallecano", "Real Betis", "Real Madrid", "Real Sociedad", "Sevilla", "Valencia", "Valladolid", "Villarreal"]
    },
    "Serie A": {
        "link": "https://www.espn.in/football/teams/_/league/ITA.1/italian-serie-a",
        "teams": ["AC Milan", "Atalanta", "Bologna", "Cagliari", "Como", "Empoli", "Fiorentina", "Genoa", "Inter Milan", "Juventus", "Lazio", "Lecce", "Napoli", "Parma", "AS Roma", "Torino", "Udinese", "Verona"]
    },
    "France Ligue 1": {
        "link": "https://www.espn.in/football/teams/_/league/FRA.1/french-ligue-1",
        "teams": ["Angers", "Auxerre", "Brest", "Le Havre", "Lens", "Lille", "Lyon", "Marseille", "Monaco", "Montpellier", "Nantes", "Nice", "Paris Saint-Germain", "Reims", "Rennes", "Strasbourg", "St Etienne", "Toulouse"]
    }
}

# --- 3. UI DESIGN ---
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

# --- LEAGUE & DATE PICKER ---
st.subheader("📋 Step 1: Select Match Info")
c_l, c_d = st.columns(2)
with c_l:
    sel_league = st.selectbox("Select League", list(league_data.keys()))
with c_d:
    sel_date = st.date_input("Select Match Date", datetime.date.today())

st.write("---")

# --- TEAM PICKER ---
st.subheader("🎯 Step 2: Pick Teams")
col1, col2 = st.columns(2)
with col1:
    home_team = st.selectbox("🏠 Home Team", league_data[sel_league]["teams"], index=0)
with col2:
    away_team = st.selectbox("🚀 Away Team", league_data[sel_league]["teams"], index=1)

# --- 4. PREDICTION LOGIC ---
if st.button("Generate Verified Live Analysis"):
    if home_team == away_team:
        st.error("Error: အိမ်ကွင်းနှင့် အဝေးကွင်း အသင်းမတူရပါ။")
    elif not model:
        st.error("Error: AI ချိတ်ဆက်မှုမရှိပါ။")
    else:
        with st.spinner('AI က မူရင်း Website များမှ နောက်ဆုံး ၅ ပွဲရလဒ်များကို စစ်ဆေးနေပါသည်...'):
            try:
                # AI အတွက် ညွှန်ကြားချက်များ
                prompt = f"""
                Professional Audit Request:
                You must verify data before responding.
                1. Go to {league_data[sel_league]["link"]} and also check LiveScore.com, Goal.com.
                2. Find the ACTUAL results of the LAST 5 MATCHES for {home_team} and {away_team} (2025-26 Season).
                3. Check current injury updates and H2H stats for {sel_date}.
                
                Format (Burmese Language):
                - ✅ နောက်ဆုံး ၅ ပွဲရလဒ် အစစ်အမှန်များ (Table Format)
                - 📊 Tactical Analysis (Current Form အပေါ်အခြေခံသည်)
                - 🎯 Prediction: Score, O/U 2.5, Corners, BTTS, Yellow Cards
                
                Use football emojis and be 100% accurate based on the web data.
                """
                
                response = model.generate_content(prompt)
                st.success("Verification Complete!")
                st.markdown("---")
                st.markdown(f"### 📋 {sel_league} Report: {home_team} vs {away_team}")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI API Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 3.0 - Full Feature Pick & Live Verification | Gemini 3</p>", unsafe_allow_html=True)
