import streamlit as st
import google.generativeai as genai
import requests
import datetime

# --- 1. AI SETUP (GEMINI 3 FLASH) ---
def setup_ai():
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Error: GEMINI_API_KEY ကို Secrets ထဲမှာ မတွေ့ပါ။")
            return None
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Google AI Studio ရဲ့ model စာရင်းအရ နာမည်အမှန်ကို အသုံးပြုထားပါတယ်
        return genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"AI Setup Error: {str(e)}")
        return None

model = setup_ai()

# --- 2. FOOTBALL DATA API ---
def get_matches(league_code, date_str):
    if "FOOTBALL_DATA_API_KEY" not in st.secrets:
        return []
    
    url = f"https://api.football-data.org/v4/matches?dateFrom={date_str}&dateTo={date_str}&competitions={league_code}"
    headers = {"X-Auth-Token": st.secrets["FOOTBALL_DATA_API_KEY"]}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("matches", [])
        return []
    except:
        return []

# --- 3. UI DESIGN ---
st.set_page_config(page_title="Football AI Prediction", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #39FF14 0%, #20C20E 100%);
        color: black; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none;
    }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        border: 2px solid #39FF14 !important; background-color: #1e1e1e !important;
    }
    h1, h2, h3 { text-align: center; color: #39FF14; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Football AI Predictions")
st.markdown("<h4 style='text-align: center;'>Powered by Gemini 3 Flash</h4>", unsafe_allow_html=True)

# Selection
league_map = {"Premier League": "PL", "Champions League": "CL", "La Liga": "PD", "Serie A": "SA", "Bundesliga": "BL1"}
sel_league = st.selectbox("Select League", list(league_map.keys()))
sel_date = st.date_input("Select Date", datetime.date.today())

matches = get_matches(league_map[sel_league], sel_date.strftime("%Y-%m-%d"))

st.write("---")
home_team, away_team = "", ""

if matches:
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" for m in matches]
    selected_match_str = st.selectbox("Select Match", match_options)
    for m in matches:
        if f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" == selected_match_str:
            home_team, away_team = m['homeTeam']['name'], m['awayTeam']['name']
            break
else:
    st.warning("ပွဲစဉ်များ ရှာမတွေ့ပါ။ အောက်တွင် အသင်းနာမည် ရိုက်ထည့်ပါ။")
    c1, c2 = st.columns(2)
    home_team = c1.text_input("Home Team", placeholder="Eg. Manchester United")
    away_team = c2.text_input("Away Team", placeholder="Eg. Liverpool")

# --- 4. PREDICTION BUTTON ---
if st.button("Get AI Analysis"):
    if not home_team or not away_team:
        st.error("ကျေးဇူးပြု၍ အသင်းနာမည်များ အရင်ထည့်ပါ။")
    elif not model:
        st.error("AI Model ချိတ်ဆက်မှု မရှိသေးပါ။")
    else:
        with st.spinner('Gemini 3 Flash က ပွဲစဉ်ကို ခွဲခြမ်းစိတ်ဖြာနေပါသည်...'):
            try:
                # Gemini 3 Flash အတွက် ပိုမိုကောင်းမွန်သော Prompt
                prompt = (f"You are an expert football analyst. Analyze {home_team} vs {away_team} "
                         f"in {sel_league}. Provide detailed predictions for: 1. Correct Score, "
                         f"2. Over/Under 2.5 goals, 3. Corners, 4. Both Teams to Score, "
                         f"5. Yellow Cards. Explain the logic in Burmese language with emojis.")
                
                response = model.generate_content(prompt)
                st.success("Analysis Complete!")
                st.markdown("### 🎯 AI Analysis Result")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI API Error: {str(e)}")
                st.info("အကယ်၍ 404 Error ပြနေပါက Gemini API Key က Gemini 3 ကို အသုံးပြုခွင့်ရှိမရှိ ပြန်စစ်ပေးပါ။")

st.markdown("<br><p style='text-align: center; font-size: 10px; color: gray;'>V 1.3 - Gemini 3 Flash Preview</p>", unsafe_allow_html=True)
