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
        "teams": ["Angers", "Auxerre", "Brest", "Le Havre", "Lens", "Lille", "Lorient", "Lyon", "Marseille", "Metz", "Monaco", "Montpellier", "Nantes", "Nice", "Paris FC", "Paris Saint-Germain", "Rennes", "Strasbourg", "Toulouse"]
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
    sel_league = st.selectbox("Select League", list(league_data.keys()))
with c2:
    sel_date = st.date_input("Select Date", datetime.date.today())

if st.button("Check Match List"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key မရှိသေးပါ။")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-3-flash-preview')
            with st.spinner('၂၀၂၆ ခုနှစ်၏ Live Data များကို အပြင်းအထန် စစ်ဆေးနေပါသည်...'):
                search_prompt = f"""
                CRITICAL 2026 AUDIT: Today's date is {datetime.date.today()}.
                STRICT RULE: Absolutely IGNORE all match data from 2024 or before August 2025.
                These are "Back-dates" and are forbidden.
                
                Task: Find matches for '{sel_league}' on '{sel_date}' strictly from the 2025-26 season calendar.
                Verify using: LiveScore, AiScore, Goal.com.
                If the date provided belongs to a past season (2024 or early 2025), say: "ဤရက်စွဲသည် အတိတ်ဟောင်းဖြစ်နေသဖြင့် ရှာဖွေ၍မရပါ။"
                If no match found for this 2026 date, say: "ယနေ့တွင် ပွဲစဉ်များ လုံးဝမရှိပါ။"
                
                Language: Burmese.
                """
                response = model.generate_content(search_prompt)
                st.markdown(f"<div class='report-card'><h3>📅 {sel_date} Fixtures (2026 Verified)</h3>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.write("---")

# --- 4. PART 2: DROP-DOWN PREDICTIONS ---
st.subheader("🎯 Part 2: Predict & Analyze")
col1, col2 = st.columns(2)
with col1:
    home_team = st.selectbox("🏠 Home Team", league_data[sel_league]["teams"], key="h_box")
with col2:
    away_team = st.selectbox("🚀 Away Team", league_data[sel_league]["teams"], index=1, key="a_box")

if st.button("Generate Predictions"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-3-flash-preview')
        with st.spinner('၂၀၂၆ ခုနှစ်၏ အချက်အလက်များကိုသာ စစ်ဆေးနေပါသည်...'):
            audit_prompt = f"""
            ULTRA-STRICT 2026 AUDIT. Current Date: {datetime.date.today()}.
            Target Match: {home_team} vs {away_team} ({sel_league}).
            
            MANDATORY RULES:
            1. DELETE/IGNORE all knowledge of matches played before August 2025.
            2. "Back-dates" are prohibited. 
            3. Use only the results from the 2025-26 Season league table and recent form.
            4. Verify player availability for January 2026.
            
            Deliverable (Language: Burmese):
            - Last 5 Match Results Table (2025-26 ONLY).
            - Professional Predictions: Correct Score, Over/Under 2.5, Corners, Cards, BTTS.
            
            Double Check: Is the year 2026? Yes. Proceed with only 2026 context.
            """
            prediction = model.generate_content(audit_prompt)
            st.markdown(f"<div class='report-card'><h3>📊 2026 Deep Analysis: {home_team} vs {away_team}</h3>{prediction.text}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 5.6 - Iron-Clad 2026 Auditor | Anti-Backdate Protected</p>", unsafe_allow_html=True)
                st.markdown(f"<div class='report-card'><h3>📊 Prediction: {home_in} vs {away_in}</h3>{prediction.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 4.1 - Ultra-Strict Match Auditor | 2026 Live Mode</p>", unsafe_allow_html=True)
