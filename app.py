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
        "teams": ["Real Madrid", "Manchester City", "Bayern Munich", "Arsenal", "Barcelona", "Inter Milan", "Liverpool", "PSG", "Bayer Leverkusen", "Atletico Madrid", "Dortmund", "AC Milan"]
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

# --- 4. PREDICTION LOGIC (GEMINI 3 FLASH) ---
if st.button("Generate Verified Live Analysis"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Error: Secrets ထဲမှာ API KEY မတွေ့ပါ။")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            # လက်ရှိ ၂၀၂၆ ခုနှစ်အတွက် Gemini 3 Flash (Preview) ကို အသုံးပြုထားသည်
            model = genai.GenerativeModel('gemini-3-flash-preview')

            with st.spinner('AI က Web Data များကို ရှာဖွေစစ်ဆေးနေပါသည်...'):
                prompt = f"""
                Professional Audit Request (Current Date: {sel_date}):
                Please analyze the match: {home_team} vs {away_team} in {sel_league}.
                
                Mandatory Tasks:
                1. Find the REAL last 5 match results for both teams from sources like ESPN, LiveScore, or Goal.com.
                2. Check latest player injuries and tactical updates for the 2025-26 season.
                3. Provide prediction: Correct Score, O/U 2.5, Corners, BTTS, and Yellow Cards.
                
                Answer in Burmese language with professional football emojis. 
                Focus on accuracy based on live web information.
                """
                
                response = model.generate_content(prompt)
                st.success("ခွဲခြမ်းစိတ်ဖြာမှု ပြီးဆုံးပါပြီ!")
                st.markdown("---")
                st.markdown(f"### 📊 Professional Report: {home_team} vs {away_team}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"AI Connection Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 3.4 - Gemini 3 Flash Preview | Live Web Analysis</p>", unsafe_allow_html=True)
