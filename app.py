import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. UI DESIGN (Professional Look) ---
st.set_page_config(page_title="AI Pro Football Auditor", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #39FF14 0%, #20C20E 100%);
        color: black; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none;
    }
    div[data-baseweb="select"] > div { border: 2px solid #39FF14 !important; border-radius: 10px; }
    h1, h2, h3 { text-align: center; color: #39FF14; }
    .report-box { border: 1px solid #39FF14; padding: 15px; border-radius: 15px; background-color: #1a1c24; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Ultimate Football Auditor")

# --- 2. LEAGUE & DATA SOURCES ---
league_data = {
    "Premier League": {
        "teams": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Ipswich Town", "Leicester City", "Liverpool", "Manchester City", "Manchester United", "Newcastle", "Nottingham Forest", "Southampton", "Tottenham", "West Ham", "Wolves"]
    },
    "Champions League": {
        "teams": ["Real Madrid", "Man City", "Bayern Munich", "Arsenal", "Barcelona", "Inter Milan", "Liverpool", "PSG", "Bayer Leverkusen", "Atletico Madrid", "Dortmund", "AC Milan"]
    }
}

# --- 3. INPUT SELECTION ---
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

# --- 4. PREDICTION LOGIC (DEEP AUDIT MODE) ---
if st.button("Deep Audit & Analysis"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Error: Secrets ထဲမှာ API KEY မတွေ့ပါ။")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-3-flash-preview')

            with st.spinner('AI က နောက်ဆုံး ၅ ပွဲရလဒ်များကို Website မျိုးစုံတွင် အပြင်းအထန် တိုက်စစ်နေပါသည်...'):
                prompt = f"""
                You are a professional Football Auditor. 
                Task: Verify the match {home_team} vs {away_team} on {sel_date} in {sel_league}.
                Current Season: 2025-26.
                
                Mandatory Search Steps:
                1. Use Google Search to find the EXACT results of the LAST 5 MATCHES for both teams.
                2. Cross-check results from LiveScore.com, ESPN, and Soccerway.
                3. Do not assume or guess scores. If a match was yesterday, find the real score.
                
                Report Structure (Burmese Language):
                - ✅ Match Verification: {sel_date} မှာ ဒီပွဲ တကယ်ရှိမရှိ အတည်ပြုချက်။
                - 📊 Audited Results (Last 5):
                    * အသင်းတစ်သင်းချင်းစီအတွက် ပြိုင်ပွဲအမည်၊ ပြိုင်ဘက်၊ ရလဒ် နှင့် ဂိုးရလဒ်ကို ဇယားဖြင့်ဖော်ပြပါ။
                    * (ဥပမာ- vs Liverpool (EPL) - ရှုံး (0-5) ❌)
                - 🎯 Prediction: Verified data ပေါ်အခြေခံပြီး Score, O/U 2.5, Corners, Cards တို့ကို ခန့်မှန်းပါ။
                
                Use professional football emojis. Accuracy is 100% required.
                """
                
                response = model.generate_content(prompt)
                st.success("Deep Audit ပြီးဆုံးပါပြီ!")
                st.markdown("---")
                st.markdown(f"### 📋 Audit Report: {home_team} vs {away_team}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Search Error: {str(e)}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>V 3.7 - Ultra Deep Audit Mode | Verified by AI</p>", unsafe_allow_html=True)
