import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIGURATION & AI SETUP ---
try:
    # Streamlit Secrets ကနေ Key ကိုယူမယ်
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Secrets ထဲမှာ GEMINI_API_KEY ထည့်ဖို့ မေ့နေပုံရပါတယ်။")
    st.stop()

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Football AI Prediction", layout="centered")

# --- CUSTOM CSS (NEON THEME) ---
st.markdown("""
    <style>
    /* Background & Main Color */
    .stApp { background-color: #121212; color: white; }
    
    /* Input & Select Box Border */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        border: 2px solid #39FF14 !important;
        border-radius: 10px;
        background-color: #1e1e1e !important;
    }
    
    /* Button Style */
    .stButton>button {
        background: linear-gradient(90deg, #FF5F1F 0%, #FF8C00 100%);
        color: white;
        border: none;
        border-radius: 15px;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
        font-size: 20px;
        box-shadow: 0 4px 15px rgba(255, 95, 31, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 95, 31, 0.5);
    }
    
    /* Subheader color */
    h3 { color: #39FF14 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>⚽ Football Predictions AI</h1>", unsafe_allow_html=True)

# --- INPUT SECTION ---
league = st.selectbox("Select League", 
                     ["Premier League", "Champions League", "Serie A", "Bundesliga", "La Liga"])

date = st.date_input("Select Date", datetime.date.today())

st.markdown("<h3>Select Team</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    home_team = st.text_input("HOME TEAM", placeholder="Eg. Liverpool", key="home")

with col2:
    st.markdown("<h2 style='text-align: center; padding-top: 10px;'>VS</h2>", unsafe_allow_html=True)

with col3:
    away_team = st.text_input("AWAY TEAM", placeholder="Eg. Real Madrid", key="away")

# --- PREDICTION LOGIC ---
def get_football_prediction(home, away, league):
    prompt = f"""
    You are a professional football analyst. Analyze the upcoming match:
    League: {league}
    Match: {home} vs {away}
    
    Please provide the following in Burmese language:
    1. **Correct Score Prediction**
    2. **Over/Under 2.5 Goals Analysis**
    3. **Corner Prediction** (Expected range)
    4. **Both Teams to Score (BTTS)**: Yes or No
    5. **Yellow Cards Prediction**
    6. **Key Reasons** (Short analysis of current form and H2H)
    
    Format the output beautifully with emojis.
    """
    response = model.generate_content(prompt)
    return response.text

# --- EXECUTION ---
if st.button("Get Predictions"):
    if home_team.strip() == "" or away_team.strip() == "":
        st.warning("ကျေးဇူးပြု၍ အိမ်ကွင်းနှင့် အဝေးကွင်းအသင်းအမည်များကို အရင်ထည့်ပေးပါ။")
    else:
        with st.spinner('AI က အချက်အလက်များကို ခွဲခြမ်းစိတ်ဖြာနေပါသည်...'):
            try:
                prediction_result = get_football_prediction(home_team, away_team, league)
                st.markdown("---")
                st.markdown("### 🎯 AI Analysis Result")
                st.write(prediction_result)
            except Exception as e:
                st.error(f"အမှားတစ်ခုရှိနေပါသည်: {str(e)}")

# --- FOOTER ---
st.markdown("<br><p style='text-align: center; font-size: 12px; color: gray;'>Powered by Google Gemini AI & Streamlit</p>", unsafe_allow_html=True)

