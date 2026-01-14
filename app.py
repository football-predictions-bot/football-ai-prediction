import streamlit as st
import google.generativeai as genai
import requests
import datetime

# --- 1. API SETUP ---
def setup_ai():
    try:
        # Secrets စစ်ဆေးခြင်း
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Error: GEMINI_API_KEY ကို Secrets ထဲမှာ ရှာမတွေ့ပါ။")
            return None
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"AI Setup Error: {str(e)}")
        return None

model = setup_ai()

# --- 2. FOOTBALL DATA API FUNCTION ---
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
        background: linear-gradient(90deg, #FF5F1F 0%, #FF8C00 100%);
        color: white; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none;
    }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        border: 2px solid #39FF14 !important; background-color: #1e1e1e !important;
    }
    h1, h2, h3 { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Football AI Predictions")

# League & Date Selection
league_map = {"Premier League": "PL", "Champions League": "CL", "La Liga": "PD", "Serie A": "SA", "Bundesliga": "BL1"}
sel_league = st.selectbox("Select League", list(league_map.keys()))
sel_date = st.date_input("Select Date", datetime.date.today())

# Fetch Matches
matches = get_matches(league_map[sel_league], sel_date.strftime("%Y-%m-%d"))

st.markdown("---")

home_team, away_team = "", ""

# Match Selection Logic
if matches:
    st.subheader("Match Found")
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" for m in matches]
    selected_match_str = st.selectbox("Select Match", match_options)
    for m in matches:
        if f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" == selected_match_str:
            home_team, away_team = m['homeTeam']['name'], m['awayTeam']['name']
            break
else:
    st.warning("အဲဒီနေ့အတွက် ပွဲစဉ်များ ရှာမတွေ့ပါ။ အောက်တွင် အသင်းနာမည် တိုက်ရိုက်ရိုက်ထည့်ပါ။")
    c1, c2 = st.columns(2)
    home_team = c1.text_input("Home Team", placeholder="Eg. Liverpool")
    away_team = c2.text_input("Away Team", placeholder="Eg. Arsenal")

# --- 4. PREDICTION BUTTON & LOGIC ---
# Button ကို အမြဲတမ်း ပေါ်နေအောင် နေရာချထားခြင်း
predict_clicked = st.button("Get Predictions")

if predict_clicked:
    if not home_team or not away_team:
        st.error("ကျေးဇူးပြု၍ အသင်းနာမည်များ ထည့်သွင်းပေးပါ။")
    elif not model:
        st.error("AI Model မရှိပါ။ API Key ကို ပြန်စစ်ပေးပါ။")
    else:
        with st.spinner('AI က ပွဲစဉ်များကို သုံးသပ်နေပါသည်...'):
            prompt = f"Analyze {home_team} vs {away_team} in {sel_league}. Provide: Correct Score, O/U 2.5, Corners, BTTS, and Yellow Cards. Language: Burmese with emojis."
            try:
                response = model.generate_content(prompt)
                st.success("Analysis Complete!")
                st.markdown("### 🎯 AI Result")
                st.write(response.text)
            except Exception as e:
                # Error ဖြစ်ရင် ဒီမှာ အသေးစိတ်ပြမယ်၊ Button တော့ ပျောက်မသွားဘူး
                st.error(f"AI API Error: {str(e)}")

st.markdown("<br><p style='text-align: center; font-size: 10px; color: gray;'>V 1.0 - Football AI</p>", unsafe_allow_html=True)
