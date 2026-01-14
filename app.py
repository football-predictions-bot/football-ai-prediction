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

# --- 2. LEAGUE LINKS (FOR AI REFERENCE) ---
leagues = {
    "Premier League": "https://www.espn.in/football/teams/_/league/ENG.1/english-premier-league",
    "Champions League": "https://www.espn.in/football/teams/_/league/uefa.champions",
    "La Liga": "https://www.espn.in/football/teams/_/league/ESP.1/spanish-laliga",
    "Serie A": "https://www.espn.in/football/teams/_/league/ITA.1/italian-serie-a",
    "France Ligue 1": "https://www.espn.in/football/teams/_/league/FRA.1/french-ligue-1"
}

# --- 3. PART 1: STRICT MATCH CHECKER ---
st.subheader("🔍 Part 1: Check Matches (Live Verification)")
c1, c2 = st.columns(2)
with c1:
    sel_league = st.selectbox("Select League", list(leagues.keys()))
with c2:
    # လက်ရှိ ၂၀၂၆ ခုနှစ်ရက်စွဲကိုသာ အဓိကထားသည်
    sel_date = st.date_input("Select Date", datetime.date.today())

if st.button("Check Match"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key မရှိသေးပါ။")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            with st.spinner(f'Searching {sel_league} fixtures for {sel_date}...'):
                # အပြင်းအထန် စစ်ဆေးရန် ညွှန်ကြားချက်
                search_prompt = f"""
                AUDIT LOG: Current Date is {datetime.date.today()}.
                TASK: Find ALL matches for '{sel_league}' on '{sel_date}'.
                
                MANDATORY SOURCES:
                1. https://www.livescore.com/en/
                2. https://m.aiscore.com/
                3. https://www.goal.com/en/live-score/

                STRICT RULES:
                - Do NOT show results from 2024 or 2025.
                - Only provide matches that are scheduled for the 2025-26 season.
                - If NO matches are found on {sel_date} in the verified sources, strictly reply: "ယနေ့တွင် {sel_league} ပွဲစဉ်များ လုံးဝမရှိပါ။"
                - If matches exist, list them as: [Home Team] vs [Away Team] (Kick-off Time).
                
                Language: Burmese. Be accurate and concise.
                """
                response = model.generate_content(search_prompt)
                st.markdown(f"<div class='report-card'><h3>📅 {sel_date} ပွဲစဉ်ဇယား</h3>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.write("---")

# --- 4. PART 2: DEEP PREDICTION ---
st.subheader("🎯 Part 2: Deep Prediction & Analysis")
col1, col2 = st.columns(2)
with col1:
    home_in = st.text_input("🏠 Home Team Name")
with col2:
    away_in = st.text_input("🚀 Away Team Name")

if st.button("Generate Predictions"):
    if not home_in or not away_in:
        st.warning("အသင်းအမည်များကို အရင်ရိုက်ထည့်ပါဗျ။")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            with st.spinner('နောက်ဆုံး ၅ ပွဲရလဒ်များကို အပြင်းအထန် ရှာဖွေစစ်ဆေးနေပါသည်...'):
                audit_prompt = f"""
                URGENT AUDIT: 2025-26 Season Analysis.
                Match: {home_in} vs {away_in}
                Verify from LiveScore, AiScore, and Goal.com.

                Required Data:
                1. Last 5 Match Results: Find EXACT scores for {home_in} and {away_in} separately (Must be from late 2025 to 2026).
                2. Detailed Prediction:
                   - Correct Score
                   - Total Corners (Range)
                   - Total Yellow Cards
                   - Goal Under/Over 2.5
                   - Both Teams to Score (Yes/No)
                
                Language: Burmese. Use a clear table for results. Use football emojis.
                If data for 2026 is not yet available, do not use 2024 data.
                """
                prediction = model.generate_content(audit_prompt)
                st.markdown(f"<div class='report-card'><h3>📊 Prediction: {home_in} vs {away_in}</h3>{prediction.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 4.1 - Ultra-Strict Match Auditor | 2026 Live Mode</p>", unsafe_allow_html=True)
