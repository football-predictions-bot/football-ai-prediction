import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="2026 Football Auditor", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #39FF14 0%, #20C20E 100%);
        color: black; border-radius: 12px; font-weight: bold; border: none;
    }
    h1, h2, h3 { color: #39FF14; text-align: center; }
    .report-card { background-color: #1a1c24; padding: 20px; border-radius: 15px; border-left: 5px solid #39FF14; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Football Predictions Bot (2026)")

# --- 2. SETUP MODEL WITH GOOGLE SEARCH TOOL ---
def get_model(api_key):
    genai.configure(api_key=api_key)
    # ၂၀၂၆ ဇန်နဝါရီအတွက် အသင့်တော်ဆုံး Gemini 3 Flash Model ကို သုံးထားပါတယ်
    # 'google_search_retrieval' tool ကို ထည့်သွင်းပြီး Live Data ရှာခိုင်းပါမည်
    model = genai.GenerativeModel(
        model_name='gemini-3-flash-preview',
        tools=[{'google_search_retrieval': {}}] 
    )
    return model

# --- 3. TEAM DATA ---
league_data = {
    "Premier League": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds United", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur", "West Ham United", "Wolves"],
    "La Liga": ["Alaves", "Athletic Club", "Atletico Madrid", "Barcelona", "Celta Vigo", "Elche CF", "Espanyol", "Getafe", "Girona", "Las Palmas", "Leganes", "Levante", "Mallorca", "Osasuna", "Rayo Vallecano", "Real Betis", "Real Madrid", "Real Oviedo", "Real Sociedad", "Sevilla", "Valencia", "Villarreal"],
    "Serie A": ["AC Milan", "AS Roma", "Atalanta", "Bologna", "Cagliari", "Como", "Cremonese", "Fiorentina", "Genoa", "Inter Milan", "Juventus", "Lazio", "Lecce", "Napoli", "Parma", "Pisa", "Sassuolo", "Torino", "Udinese", "Verona"]
}

# --- 4. MATCH CHECKER (LIVE) ---
st.subheader("🔍 Part 1: Real-Time Match Finder")
c1, c2 = st.columns(2)
with c1:
    sel_league = st.selectbox("League", list(league_data.keys()))
with c2:
    sel_date = st.date_input("Date", datetime.date.today())

if st.button("Check Matches Now"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key မတွေ့ပါ။")
    else:
        try:
            model = get_model(st.secrets["GEMINI_API_KEY"])
            with st.spinner('Google Search မှ တိုက်ရိုက် ရှာဖွေနေပါသည်...'):
                prompt = f"Search Google and list all real matches for {sel_league} on {sel_date}. If no matches, say so clearly in Burmese. Date is January 2026."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.write("---")

# --- 5. DEEP ANALYSIS & PREDICTION ---
st.subheader("🎯 Part 2: Honest Analysis")
col1, col2 = st.columns(2)
with col1:
    home_in = st.selectbox("🏠 Home Team", league_data[sel_league], key="h")
with col2:
    away_in = st.selectbox("🚀 Away Team", league_data[sel_league], index=1, key="a")

if st.button("Generate Verified Prediction"):
    try:
        model = get_model(st.secrets["GEMINI_API_KEY"])
        with st.spinner('နောက်ဆုံး ၅ ပွဲရလဒ်များကို Google မှ အတည်ပြုနေပါသည်...'):
            prompt = f"""
            Search the internet for the last 5 match results of {home_in} and {away_in} in the 2025-26 season.
            Strictly use only actual scores from late 2025 and 2026.
            After finding results, provide a professional prediction in Burmese.
            Show the scores and dates for the last 5 matches.
            """
            response = model.generate_content(prompt)
            st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("<br><p style='text-align: center; font-size: 10px; color: gray;'>V 6.0 - Gemini 3 Hybrid Engine</p>", unsafe_allow_html=True)
