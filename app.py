import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. UI DESIGN ---
st.set_page_config(page_title="AI Tactical Match Finder", layout="centered")

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

st.title("⚽ AI Match Analysis (Ultra Search)")

# --- 2. LEAGUE DATA ---
league_data = {
    "Premier League": {
        "links": ["https://www.livescore.com/en/football/england/premier-league/", "https://www.espn.in/football/fixtures/_/league/eng.1"],
        "teams": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton And Hove Albion", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds United", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur", "West Ham United", "Wolves"]
    },
    "Champions League": {
        "links": ["https://www.livescore.com/en/football/uefa-champions-league/", "https://www.espn.in/football/fixtures/_/league/uefa.champions"],
        "teams": ["Real Madrid", "Manchester City", "Bayern Munich", "Arsenal", "Barcelona", "Inter Milan", "Liverpool", "PSG", "Atletico Madrid", "Dortmund", "AC Milan"]
    }
}

# --- 3. INPUT ---
c_l, c_d = st.columns(2)
with c_l:
    sel_league = st.selectbox("Select League", list(league_data.keys()))
with c_d:
    sel_date = st.date_input("Match Date", datetime.date.today())

st.write("---")

col1, col2 = st.columns(2)
with col1:
    home_team = st.selectbox("🏠 Home Team", league_data[sel_league]["teams"], index=0)
with col2:
    away_team = st.selectbox("🚀 Away Team", league_data[sel_league]["teams"], index=1)

# --- 4. DEEP SEARCH LOGIC ---
if st.button("Deep Search & Analyze"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Error: Secrets ထဲမှာ API KEY မတွေ့ပါ။")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-3-flash-preview')

            with st.spinner(f'AI က {sel_date} အတွက် ပွဲစဉ်များကို Website အသီးသီးတွင် အပြင်းအထန် ရှာဖွေနေပါသည်...'):
                # AI ကို ပိုမိုတိကျစွာ ရှာခိုင်းသည့် prompt
                prompt = f"""
                CRITICAL TASK: Verify if {home_team} vs {away_team} exists on {sel_date} in {sel_league}.
                
                Instructions:
                1. Search Google with keywords: "{home_team} vs {away_team} {sel_date} fixtures".
                2. Check multiple sports sites: ESPN, LiveScore, BBC Sport, and Sky Sports.
                3. Today is {datetime.date.today()}.
                
                Validation:
                - If the match is postponed, cancelled, or doesn't exist on {sel_date}, clearly explain WHY.
                - If the match exists, provide:
                    a) Confirmed Kick-off Time.
                    b) Recent 5 matches results for both (Audited).
                    c) Tactical analysis & Score Prediction.
                
                Language: Burmese with emojis. 
                Don't say "not found" unless you have checked at least 3 sources.
                """
                
                response = model.generate_content(prompt)
                st.success("ရှာဖွေမှု အောင်မြင်ပါသည်!")
                st.markdown("---")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Search Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 3.6 - Deep Search Mode | Gemini 3 Flash</p>", unsafe_allow_html=True)
