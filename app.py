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

# --- 2. LEAGUE DATA (OFFICIAL ESPN LINKS) ---
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

# --- 4. PREDICTION LOGIC (WITH MATCH VERIFICATION) ---
if st.button("Generate Verified Live Analysis"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Error: Secrets ထဲမှာ API KEY မတွေ့ပါ။")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-3-flash-preview')

            with st.spinner('ပထမဦးစွာ သတ်မှတ်ရက်စွဲတွင် ပွဲစဉ်ရှိမရှိ စစ်ဆေးနေပါသည်...'):
                # AI ကို အရင်ဆုံး ပွဲရှိမရှိ စစ်ခိုင်းသည့် Prompt
                prompt = f"""
                Professional Audit Task (Today is {datetime.date.today()}, checking for {sel_date}):
                
                Step 1: Use Google Search to check the official 2025-26 fixture list for {sel_league}.
                Step 2: Does {home_team} play against {away_team} on the date {sel_date}?
                
                IF NO MATCH EXISTS: 
                Simply reply in Burmese that "ဒီနေ့မှာ {home_team} နဲ့ {away_team} တို့ရဲ့ ပွဲစဉ်မရှိပါဘူး။" and list the next upcoming match date for them.
                
                IF MATCH EXISTS:
                1. Provide the REAL last 5 results (W/D/L) for both.
                2. Analyze injuries and Head-to-Head.
                3. Prediction: Score, O/U 2.5, Corners, BTTS, Yellow Cards.
                
                Language: Burmese with emojis. Accuracy is the top priority.
                """
                
                response = model.generate_content(prompt)
                st.success("စစ်ဆေးမှု ပြီးဆုံးပါပြီ!")
                st.markdown("---")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"AI Connection Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 3.5 - Match Verification Mode | Powered by Gemini 3</p>", unsafe_allow_html=True)
