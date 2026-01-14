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
        return genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"AI Setup Error: {str(e)}")
        return None

model = setup_ai()

# --- 2. FOOTBALL DATA API ---
def get_matches(league_code, date_str):
    if "FOOTBALL_DATA_API_KEY" not in st.secrets:
        return []
    
    # API ကနေ သတ်မှတ်ထားတဲ့ ရက်စွဲအတိုင်း ပွဲစဉ်တွေ ဆွဲယူမယ်
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

# League & Date Selection
league_map = {"Premier League": "PL", "Champions League": "CL", "La Liga": "PD", "Serie A": "SA", "Bundesliga": "BL1"}
sel_league = st.selectbox("Select League", list(league_map.keys()))

# အရေးကြီးသည်- ပွဲစဉ်ရှိနိုင်မယ့် ရက်စွဲကို ရွေးပေးရပါမယ် (ဥပမာ- ရှေ့လာမယ့် စနေ၊ တနင်္ဂနွေ)
sel_date = st.date_input("Select Date", datetime.date.today())

# ပွဲစဉ်တွေကို API ကနေ ရှာမယ်
matches = get_matches(league_map[sel_league], sel_date.strftime("%Y-%m-%d"))

st.write("---")
home_team, away_team = "", ""

# --- ဒီအပိုင်းက အသင်းတွေကို Pick လုပ်တဲ့အပိုင်းပါ ---
if matches:
    st.markdown("<h3>🎯 Select a Match to Analyze</h3>", unsafe_allow_html=True)
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" for m in matches]
    selected_match_str = st.selectbox("ပွဲစဉ်ကို ရွေးချယ်ပါ", match_options)
    
    # ရွေးလိုက်တဲ့ ပွဲစဉ်ကနေ အသင်းနာမည်တွေကို ထုတ်ယူမယ်
    for m in matches:
        if f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" == selected_match_str:
            home_team, away_team = m['homeTeam']['name'], m['awayTeam']['name']
            break
    
    st.success(f"Selected: {home_team} vs {away_team}")
else:
    # ပွဲစဉ်ရှာမတွေ့မှသာ ရိုက်ထည့်ခိုင်းမယ့် Box ပေါ်လာမယ်
    st.warning(f"⚠️ {sel_date} နေ့မှာ {sel_league} ပွဲစဉ်များ မရှိသေးပါ။")
    st.info("ပွဲစဉ်ရှိမယ့် ရက်စွဲ (ဥပမာ- လာမည့်စနေနေ့) ကို ပြောင်းရွေးကြည့်ပါ သို့မဟုတ် အောက်တွင် ကိုယ်တိုင်ရိုက်ထည့်ပါ။")
    c1, c2 = st.columns(2)
    home_team = c1.text_input("Home Team", placeholder="Eg. Liverpool")
    away_team = c2.text_input("Away Team", placeholder="Eg. Arsenal")

# --- 4. PREDICTION BUTTON ---
if st.button("Get AI Analysis"):
    if home_team and away_team:
        with st.spinner(f'Gemini 3 Flash က {home_team} vs {away_team} ကို သုံးသပ်နေပါသည်...'):
            try:
                prompt = f"Analyze {home_team} vs {away_team} in {sel_league}. Provide: Correct Score, O/U 2.5, Corners, BTTS, and Yellow Cards. Explain in Burmese with emojis."
                response = model.generate_content(prompt)
                st.markdown("### 🎯 AI Result")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI Error: {str(e)}")
    else:
        st.error("ကျေးဇူးပြု၍ အသင်းတစ်ပွဲကို အရင်ရွေးချယ်ပေးပါ။")
