import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. AI SETUP (GEMINI 3 FLASH) ---
def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        return None
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # model နာမည်ကို gemini-3-flash-preview ဟု အမှန်ပြင်ထားသည်
        model = genai.GenerativeModel(
            model_name='gemini-3-flash-preview',
            tools=[{'google_search': {}}]
        )
        return model
    except Exception as e:
        return None

model = setup_ai()

# --- 2. OFFICIAL TEAM LISTS (ALL LEAGUES) ---
# ESPN မှ အသင်းစာရင်းများကို ပြန်လည်ထည့်သွင်းပေးထားသည်
league_data = {
    "Premier League": {
        "link": "https://www.espn.in/football/teams/_/league/ENG.1/english-premier-league",
        "teams": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton And Hove Albion", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds United", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers"]
    },
    "Champions League": {
        "link": "https://www.espn.in/football/teams/_/league/uefa.champions",
        "teams": ["Real Madrid", "Manchester City", "Bayern Munich", "Arsenal", "Barcelona", "Inter Milan", "Liverpool", "Paris Saint-Germain", "Atletico Madrid", "Atalanta", "Juventus", "Borussia Dortmund", "Sporting CP", "AC Milan", "Aston Villa", "Benfica", "Feyenoord", "Monaco", "PSV Eindhoven", "Lille", "Celtic"]
    },
    "La Liga": {
        "link": "https://www.espn.in/football/teams/_/league/ESP.1/spanish-laliga",
        "teams": ["Alaves", "Athletic Club", "Atletico Madrid", "Barcelona", "Celta Vigo", "Elche", "Espanyol", "Getafe", "Girona", "Las Palmas", "Leganes", "Levante", "Mallorca", "Osasuna", "Rayo Vallecano", "Real Betis", "Real Madrid", "Real Sociedad", "Sevilla", "Valencia", "Valladolid", "Villarreal"]
    },
    "Serie A": {
        "link": "https://www.espn.in/football/teams/_/league/ITA.1/italian-serie-a",
        "teams": ["AC Milan", "Atalanta", "Bologna", "Cagliari", "Como", "Cremonese", "Empoli", "Fiorentina", "Genoa", "Inter Milan", "Juventus", "Lazio", "Lecce", "Napoli", "Parma", "Pisa", "AS Roma", "Sassuolo", "Torino", "Udinese", "Verona"]
    },
    "France Ligue 1": {
        "link": "https://www.espn.in/football/teams/_/league/FRA.1/french-ligue-1",
        "teams": ["Angers", "Auxerre", "Brest", "Le Havre", "Lens", "Lille", "Lyon", "Marseille", "Metz", "Monaco", "Montpellier", "Nantes", "Nice", "Paris Saint-Germain", "Paris FC", "Reims", "Rennes", "Strasbourg", "St Etienne", "Toulouse"]
    }
}

# --- 3. UI DESIGN ---
st.set_page_config(page_title="Football AI Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #39FF14 0%, #20C20E 100%);
        color: black; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none;
    }
    div[data-baseweb="select"] > div { 
        border: 2px solid #39FF14 !important; 
        border-radius: 10px;
        background-color: #1a1c24 !important;
    }
    h1, h2, h3 { text-align: center; color: #39FF14; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Football AI Match Analyst")
st.markdown("<p style='text-align: center;'>Gemini 3 Flash: Live Data Mode (2025-26)</p>", unsafe_allow_html=True)

# Step 1: Selection
st.subheader("📋 Step 1: Info Selection")
c_l, c_d = st.columns(2)
with c_l:
    sel_league = st.selectbox("Select League", list(league_data.keys()))
with c_d:
    sel_date = st.date_input("Match Date", datetime.date.today())

st.write("---")

# Step 2: Pick Teams
st.subheader("🎯 Step 2: Pick Teams")
col1, col2 = st.columns(2)
with col1:
    home_team = st.selectbox("🏠 Home Team", league_data[sel_league]["teams"], index=0)
with col2:
    away_team = st.selectbox("🚀 Away Team", league_data[sel_league]["teams"], index=1)

# Step 3: Analysis Button
if st.button("Generate Verified Live Analysis"):
    if home_team == away_team:
        st.error("အိမ်ကွင်းနှင့် အဝေးကွင်း အသင်းမတူရပါ။")
    elif not model:
        st.error("AI နှင့် ချိတ်ဆက်၍မရပါ။ Secrets ထဲတွင် API KEY ကို စစ်ဆေးပါ။")
    else:
        with st.spinner('AI က မူရင်း Website များမှ နောက်ဆုံး ၅ ပွဲရလဒ်များကို စစ်ဆေးနေပါသည်...'):
            try:
                # Prompt ကို အချက်အလက် တိုက်စစ်ခိုင်းသည့် ပုံစံဖြင့် ခိုင်းထားသည်
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
                st.error(f"Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 3.0 - Full Feature Pick & Live Verification | Gemini 3</p>", unsafe_allow_html=True)
