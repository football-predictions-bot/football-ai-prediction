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

# --- 2. CORE FUNCTIONS ---

def get_rotated_model():
    keys = [st.secrets["GEMINI_KEY_1"], st.secrets["GEMINI_KEY_2"], st.secrets["GEMINI_KEY_3"]]
    genai.configure(api_key=random.choice(keys))
    return genai.GenerativeModel('gemini-1.5-flash')

@st.cache_data(ttl=3600)
def get_matches_by_date(league_id, date_str):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-apisports-key': st.secrets["APISPORTS_KEY"]}
    params = {'league': league_id, 'season': 2025, 'date': date_str}
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json().get('response', [])
    except:
        return []

@st.cache_data(ttl=21600)
def get_team_form(team_id):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-apisports-key': st.secrets["APISPORTS_KEY"]}
    params = {'team': team_id, 'last': 5}
    response = requests.get(url, headers=headers, params=params)
    return response.json().get('response', [])

# --- 3. DATA ---
leagues = {
    "Premier League": 39,
    "La Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78
}

# --- 4. PART 1: MATCH FINDER BY DATE ---
st.subheader("🔍 Part 1: Real-Time Match Finder")
c1, c2 = st.columns(2)
with c1:
    sel_league = st.selectbox("League ရွေးပါ", list(leagues.keys()))
with c2:
    sel_date = st.date_input("Date ရွေးပါ", datetime.date.today())

if st.button("Check Matches Now"):
    date_str = sel_date.strftime('%Y-%m-%d')
    with st.spinner(f'{sel_league} ပွဲစဉ်များကို ရှာဖွေနေပါသည်...'):
        matches = get_matches_by_date(leagues[sel_league], date_str)
        
        if matches:
            st.write(f"### {sel_league} Matches on {date_str}")
            for m in matches:
                status = m['fixture']['status']['short']
                home = m['teams']['home']['name']
                away = m['teams']['away']['name']
                h_goal = m['goals']['home'] if m['goals']['home'] is not None else ""
                a_goal = m['goals']['away'] if m['goals']['away'] is not None else ""
                
                st.markdown(f"<div class='match-box'>⏰ {m['fixture']['date'][11:16]} | {home} {h_goal} - {a_goal} {away} ({status})</div>", unsafe_allow_html=True)
        else:
            st.info("ယနေ့အတွက် ပွဲစဉ်များ ရှာမတွေ့ပါ။")

st.write("---")

# --- 5. PART 2: TEAM ANALYSIS ---
st.subheader("🎯 Part 2: Team Form & AI Analysis")
# (မှတ်ချက် - ဤနေရာတွင် ID များထည့်ရန် လိုအပ်ပါသည်၊ ဥပမာအနေဖြင့် Arsenal သာ ပြထားပါသည်)
pl_teams = {"Arsenal": 42, "Man City": 50, "Liverpool": 40, "Chelsea": 49, "Man United": 33}
sel_team = st.selectbox("အသင်းကို ရွေးချယ်ပြီး Form စစ်ဆေးပါ", list(pl_teams.keys()))

if st.button("Generate Verified Prediction"):
    with st.spinner('Data နှင့် AI Analysis ကို ပြင်ဆင်နေပါသည်...'):
        form_data = get_team_form(pl_teams[sel_team])
        if form_data:
            summary = ""
            for f in form_data:
                res = f"{f['teams']['home']['name']} {f['goals']['home']}-{f['goals']['away']} {f['teams']['away']['name']}"
                summary += res + "\n"
                st.write(f"✅ {res}")
            
            try:
                model = get_rotated_model()
                ai_prompt = f"Analyze these recent results for {sel_team}: {summary}. Provide a prediction in Burmese."
                response = model.generate_content(ai_prompt)
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
            except:
                st.error("AI Limit ပြည့်သွားပါပြီ။ ၁ မိနစ်ခန့် စောင့်ပါ။")

st.markdown("<br><p style='text-align: center; font-size: 10px; color: gray;'>V 8.0 - Full API Integration</p>", unsafe_allow_html=True)
