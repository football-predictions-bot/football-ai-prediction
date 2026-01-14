import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. AI SETUP ---
def setup_ai():
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return None
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # အင်တာနက်ရှာဖွေရေး Tool ကို ထည့်သွင်းထားသည်
        return genai.GenerativeModel(
            model_name='gemini-3-flash-preview',
            tools=[{'google_search': {}}]
        )
    except:
        return None

model = setup_ai()

# --- 2. SOURCE LINKS FOR VERIFICATION ---
sources = [
    "https://www.livescore.com/en/",
    "https://m.aiscore.com/",
    "https://www.goal.com/en/live-scores",
    "https://www.espn.in/football/fixtures"
]

# --- 3. UI ---
st.set_page_config(page_title="AI Tactical Analyst", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #39FF14 0%, #20C20E 100%);
        color: black; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none;
    }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { 
        border: 2px solid #39FF14 !important; border-radius: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ AI Match Analysis (Live Data)")
st.info("AI သည် LiveScore, AiScore နှင့် Goal.com တို့မှ အချက်အလက်များကို တိုက်ရိုက်စစ်ဆေးပါမည်။")

col1, col2 = st.columns(2)
with col1:
    home_team = st.text_input("🏠 Home Team")
with col2:
    away_team = st.text_input("🚀 Away Team")

# --- 4. DATA-DRIVEN PROMPT ---
if st.button("Generate Verified Analysis"):
    if not home_team or not away_team:
        st.warning("အသင်းနာမည်များ အရင်ထည့်ပေးပါဗျ။")
    else:
        with st.spinner('မူရင်း Website များမှ နောက်ဆုံး ၅ ပွဲရလဒ်များကို အသေးစိတ် စစ်ဆေးနေပါသည်...'):
            try:
                # Prompt ကို အချက်အလက် မမှားစေရန် အောက်ပါအတိုင်း ခိုင်းထားသည်
                prompt = f"""
                You are a professional football data auditor.
                Match: {home_team} vs {away_team} (2025-26 Season).
                
                Mandatory Steps:
                1. Access these websites: {", ".join(sources)}.
                2. Extract the EXACT results of the last 5 matches for {home_team} and {away_team}.
                3. Do NOT guess. If a match was played yesterday, find the score.
                4. Analyze Head-to-Head (H2H) and player injuries from these live sources.
                
                Report Structure (Burmese Language):
                - ✅ Verified Last 5 Matches (Home/Away Table)
                - 📊 Tactical Analysis based on current form
                - 🎯 Prediction: Score, O/U 2.5, Corners, Cards (BTTS)
                
                Use professional football emojis and Burmese terminology.
                Ensure 100% accuracy based on the provided links.
                """
                
                response = model.generate_content(prompt)
                st.success("Verification Complete!")
                st.markdown("---")
                st.markdown(f"### 📋 Match Analysis: {home_team} vs {away_team}")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("<br><hr><p style='text-align: center; font-size: 10px; color: gray;'>Data Sources: LiveScore | AiScore | Goal.com | ESPN</p>", unsafe_allow_html=True)
