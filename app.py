import streamlit as st
import requests
import google.generativeai as genai
import datetime
import random

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="2026 Football Auditor", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #39FF14 0%, #20C20E 100%);
        color: black; border-radius: 12px; font-weight: bold; border: none; width: 100%;
    }
    h1, h2, h3 { color: #39FF14; text-align: center; }
    .report-card { background-color: #1a1c24; padding: 20px; border-radius: 15px; border-left: 5px solid #39FF14; margin-bottom: 20px; }
    .match-box { border: 1px solid #333; padding: 10px; border-radius: 10px; margin-bottom: 5px; background: #252833; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Football Predictions Bot (2026)")

# --- 2. CORE LOGIC: API & AI ROTATION ---

# API Data ယူပြီး Cache လုပ်ထားမည့် Function (၆ နာရီ သက်တမ်း)
@st.cache_data(ttl=21600)
def get_football_data(team_id):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-apisports-key': st.secrets["APISPORTS_KEY"]}
    params = {'team': team_id, 'last': 5}
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json().get('response', [])
    except:
        return []

# Gemini Model ကို အလှည့်ကျ ခေါ်ပေးမည့် Function
def get_rotated_model():
    keys = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"], st.secrets["GEMINI_KEY_3"]]
    selected_key = random.choice(keys)
    genai.configure(api_key=selected_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# --- 3. TEAM DATA (API IDs added) ---
# Premier League အတွက် API IDs များ
pl_teams = {
    "Arsenal": 42, "Aston Villa": 66, "Bournemouth": 35, "Brentford": 55, 
    "Brighton": 51, "Chelsea": 49, "Crystal Palace": 52, "Everton": 45, 
    "Fulham": 36, "Liverpool": 40, "Manchester City": 50, "Manchester United": 33, 
    "Newcastle United": 34, "Nottingham Forest": 65, "Tottenham Hotspur": 47, 
    "West Ham United": 48, "Wolves": 39
}

# --- 4. MATCH CHECKER ---
st.subheader("🔍 Part 1: Verified Team Form")
sel_team_name = st.selectbox("အသင်းရွေးချယ်ပါ", list(pl_teams.keys()))

if st.button("Check Latest Form Now"):
    with st.spinner('API မှ တကယ့်ရလဒ်များကို ရယူနေပါသည်...'):
        results = get_football_data(pl_teams[sel_team_name])
        
        if results:
            st.write(f"### {sel_team_name} Last 5 Results")
            summary = ""
            for m in results:
                match_str = f"{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}"
                st.markdown(f"<div class='match-box'>⚽ {match_str}</div>", unsafe_allow_html=True)
                summary += match_str + "\n"
            
            # AI Analysis
            try:
                model = get_rotated_model()
                prompt = f"Analyze these {sel_team_name} results: {summary}. Give a professional prediction for their next match in Burmese. Be realistic."
                ai_resp = model.generate_content(prompt)
                st.markdown(f"<div class='report-card'><b>🤖 AI Analysis:</b><br>{ai_resp.text}</div>", unsafe_allow_html=True)
            except:
                st.error("Key Limit ပြည့်နေပါသည်။ ခဏစောင့်ပါ။")
        else:
            st.error("Data ရှာမတွေ့ပါ။ API Key ကို စစ်ဆေးပါ။")

st.write("---")

# --- 5. HEAD TO HEAD (Simplified for Performance) ---
st.subheader("🎯 Part 2: Quick Match Analysis")
c1, c2 = st.columns(2)
with c1:
    h_team = st.selectbox("🏠 Home", list(pl_teams.keys()), key="h")
with c2:
    a_team = st.selectbox("🚀 Away", list(pl_teams.keys()), index=1, key="a")

if st.button("Generate Match Prediction"):
    # ဤနေရာတွင် AI ကို Data အချက်အလက်ပေးပြီး ခွဲခြမ်းစိတ်ဖြာခိုင်းပါမည်
    try:
        model = get_rotated_model()
        with st.spinner('ခွဲခြမ်းစိတ်ဖြာနေပါသည်...'):
            prompt = f"Predict the match between {h_team} and {a_team} based on typical 2026 season form in Burmese."
            response = model.generate_content(prompt)
            st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
    except:
        st.error("Error in AI Prediction.")

st.markdown("<br><p style='text-align: center; font-size: 10px; color: gray;'>V 7.0 - Hybrid API-Sports & Gemini Engine</p>", unsafe_allow_html=True)
