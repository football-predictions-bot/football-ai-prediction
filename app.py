import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="Football Predictions Bot", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #39FF14 0%, #20C20E 100%);
        color: black; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none;
    }
    div[data-baseweb="select"] > div { border: 2px solid #39FF14 !important; border-radius: 10px; }
    h1, h2, h3 { text-align: center; color: #39FF14; }
    .report-card { background-color: #1a1c24; padding: 20px; border-radius: 15px; border-left: 5px solid #39FF14; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Football Predictions Bot")

# --- 2. 100% VERIFIED TEAM LISTS (2025-26 Season) ---
league_data = {
    "Premier League": {
        "url": "https://www.espn.in/football/teams/_/league/ENG.1/english-premier-league",
        "teams": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds United", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur", "West Ham United", "Wolves"]
    },
    "La Liga": {
        "url": "https://www.espn.in/football/teams/_/league/ESP.1/spanish-laliga",
        "teams": ["Alaves", "Athletic Club", "Atletico Madrid", "Barcelona", "Celta Vigo", "Elche CF", "Espanyol", "Getafe", "Girona", "Las Palmas", "Leganes", "Levante", "Mallorca", "Osasuna", "Rayo Vallecano", "Real Betis", "Real Madrid", "Real Oviedo", "Real Sociedad", "Sevilla", "Valencia", "Villarreal"]
    },
    "Serie A": {
        "url": "https://www.espn.in/football/teams/_/league/ITA.1/italian-serie-a",
        "teams": ["AC Milan", "AS Roma", "Atalanta", "Bologna", "Cagliari", "Como", "Cremonese", "Fiorentina", "Genoa", "Inter Milan", "Juventus", "Lazio", "Lecce", "Napoli", "Parma", "Pisa", "Sassuolo", "Torino", "Udinese", "Verona"]
    },
    "Bundesliga": {
        "url": "https://www.espn.com/football/teams/_/league/ger.1/german-bundesliga",
        "teams": ["Augsburg", "Bayer Leverkusen", "Bayern Munich", "Bochum", "Borussia Dortmund", "Borussia Monchengladbach", "Eintracht Frankfurt", "FC Heidenheim", "FC Koln", "FC St. Pauli", "Hamburger SV", "Holstein Kiel", "Mainz 05", "RB Leipzig", "SC Freiburg", "TSG Hoffenheim", "Union Berlin", "VfB Stuttgart", "VfL Wolfsburg", "Werder Bremen"]
    },
    "France Ligue 1": {
        "url": "https://www.espn.in/football/teams/_/league/FRA.1/french-ligue-1",
        "teams": ["Angers", "Auxerre", "Brest", "Le Havre", "Lens", "Lille", "Lorient", "Lyon", "Marseille", "Metz", "Monaco", "Nantes", "Nice", "Paris FC", "Paris Saint-Germain", "Rennes", "Strasbourg", "Toulouse"]
    },
    "Champions League": {
        "url": "https://www.uefa.com/uefachampionsleague/standings/",
        "teams": ["AC Milan", "Arsenal", "Aston Villa", "Atalanta", "Atletico Madrid", "Bayer Leverkusen", "Bayern Munich", "Benfica", "Bologna", "Borussia Dortmund", "Brest", "Celtic", "Club Brugge", "Dinamo Zagreb", "Feyenoord", "Girona", "Inter Milan", "Juventus", "Liverpool", "Manchester City", "Monaco", "PSG", "PSV Eindhoven", "RB Leipzig", "Real Madrid", "Red Bull Salzburg", "Red Star Belgrade", "Shakhtar Donetsk", "Slovan Bratislava", "Sparta Prague", "Sporting CP", "Sturm Graz", "VfB Stuttgart", "Young Boys"]
    }
}

# --- 3. PART 1: MATCH CHECKER ---
st.subheader("🔍 Part 1: Check Matches (Strict 2026)")
c1, c2 = st.columns(2)
with c1:
    sel_league = st.selectbox("Select League", list(league_data.keys()), key="main_league")
with c2:
    sel_date = st.date_input("Select Date", datetime.date.today())

if st.button("Check Match List"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key မတွေ့ပါ။ Secrets တွင် ထည့်သွင်းပါ။")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-3-flash-preview')
            with st.spinner('Checking 2026 Live Data...'):
                search_prompt = f"""
                AUDIT: Today is {datetime.date.today()} (2026).
                STRICT RULE: Ignore all data before August 2025.
                Task: List ALL {sel_league} matches on {sel_date}.
                If no match in 2025-26 season, say "ယနေ့တွင် ပွဲစဉ်များ လုံးဝမရှိပါ။"
                """
                response = model.generate_content(search_prompt)
                st.markdown(f"<div class='report-card'><h3>📅 {sel_date} Fixtures</h3>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.write("---")

# --- 4. PART 2: PREDICTIONS ---
st.subheader("🎯 Part 2: Predict & Analyze")
col1, col2 = st.columns(2)
with col1:
    home_in = st.selectbox("🏠 Home Team", league_data[sel_league]["teams"], key="h_box")
with col2:
    away_in = st.selectbox("🚀 Away Team", league_data[sel_league]["teams"], index=1, key="a_box")

if st.button("Generate Predictions"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key မရှိသေးပါ။")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-3-flash-preview')
            with st.spinner('Analyzing Current 2026 Season...'):
                audit_prompt = f"""
                ULTRA-STRICT 2026 AUDIT: Today is {datetime.date.today()}.
                Match: {home_in} vs {away_in} ({sel_league}).
                
                RULES:
                1. NO 2024 DATA ALLOWED.
                2. IGNORE ALL BACK-DATES before August 2025.
                3. Only show results from 2025-26 season.
                
                Provide in Burmese:
                - Last 5 Results Table.
                - Prediction (Score, O/U, Corners, Cards, BTTS).
                """
                prediction = model.generate_content(audit_prompt)
                st.markdown(f"<div class='report-card'><h3>📊 Prediction: {home_in} vs {away_in}</h3>{prediction.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 5.7 - Fixed Indent | 2026 Strict Mode</p>", unsafe_allow_html=True)
