import streamlit as st
import datetime
import requests
import google.generativeai as genai
import time
import json
import os
import dateutil.parser

# UI Configuration
st.set_page_config(
    page_title="Football AI",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# --- Disk Caching System ---
CACHE_DIR = "data_cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_disk_cache(key):
    # Cache File ကို ဖတ်ပြီး Expiry မကျော်သေးရင် Data ပြန်ပေးသည်
    file_path = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            cache_data = json.load(f)
            expiry = datetime.datetime.fromisoformat(cache_data['expiry'])
            if datetime.datetime.now() < expiry:
                return cache_data['data']
    return None

def set_disk_cache(key, data, expiry_dt=None, days=19):
    # Expiry အတိအကျမပေးရင် ၁၉ ရက်ထားမယ်
    if expiry_dt is None:
        expiry_dt = datetime.datetime.now() + datetime.timedelta(days=days)
    
    file_path = os.path.join(CACHE_DIR, f"{key}.json")
    with open(file_path, "w") as f:
        json.dump({'data': data, 'expiry': expiry_dt.isoformat()}, f)

# Time Handling
now_mm = datetime.datetime.utcnow() + datetime.timedelta(hours=6, minutes=30)
today_mm = now_mm.date()

# ၁။ Dictionary & Session State
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
if 'h_teams' not in st.session_state:
    st.session_state.h_teams = ["Select Team"]
if 'a_teams' not in st.session_state:
    st.session_state.a_teams = ["Select Team"]
if 'display_matches' not in st.session_state:
    st.session_state.display_matches = []

def toggle_lang():
    st.session_state.lang = 'MM' if st.session_state.lang == 'EN' else 'EN'

d = {
    'EN': {
        'title1': 'Predictions', 'sel_league': 'Select League', 'sel_date': 'Select Date',
        'btn_check': 'Check Matches Now', 'title2': 'Select Team',
        'home': 'HOME TEAM', 'away': 'AWAY TEAM', 'btn_gen': 'Generate Predictions',
        'trans_btn': 'မြန်မာဘာသာသို့ ပြောင်းရန်',
        'date_opts': ["Manual Date", "Within 24 Hours", "Within 48 Hours"],
        'ai_lang': 'English',
        'no_match': 'No match found between these teams! Please check the Match Table.'
    },
    'MM': {
        'title1': 'ပွဲကြိုခန့်မှန်းချက်များ', 'sel_league': 'လိဂ်ကို ရွေးချယ်ပါ', 'sel_date': 'ရက်စွဲကို ရွေးချယ်ပါ',
        'btn_check': 'ပွဲစဉ်များကို စစ်ဆေးမည်', 'title2': 'အသင်းကို ရွေးချယ်ပါ',
        'home': 'အိမ်ရှင်အသင်း', 'away': 'ဧည့်သည်အသင်း', 'btn_gen': 'ခန့်မှန်းချက် ထုတ်ယူမည်',
        'trans_btn': 'Switch to English',
        'date_opts': ["ရက်စွဲတပ်၍ရှာမည်", "၂၄ နာရီအတွင်း", "၄၈ နာရီအတွင်း"],
        'ai_lang': 'Burmese',
        'no_match': 'ရွေးထားသော ပွဲစဉ်မရှိပါ။ Match Table ကို ပြန်စစ်ပါ။'
    }
}
lang = st.session_state.lang

league_codes = {
    "All Leagues": "ALL",
    "Premier League (England)": "PL",
    "Champions League (Europe)": "CL",
    "La Liga (Spain)": "PD",
    "Bundesliga (Germany)": "BL1",
    "Serie A (Italy)": "SA",
    "Ligue 1 (France)": "FL1"
}

league_name_map = {
    "Premier League": "Premier League (England)",
    "UEFA Champions League": "Champions League (Europe)",
    "Primera Division": "La Liga (Spain)",
    "Bundesliga": "Bundesliga (Germany)",
    "Serie A": "Serie A (Italy)",
    "Ligue 1": "Ligue 1 (France)"
}

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Language Toggle
col_space, col_lang = st.columns([7, 3])
with col_lang:
    st.markdown('<div class="lang-wrapper">', unsafe_allow_html=True)
    st.button(d[lang]["trans_btn"], key="lang_btn", on_click=toggle_lang, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="title-style">{d[lang]["title1"]}</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown(f'<p style="color:#aaa; margin-left:15px;">{d[lang]["sel_league"]}</p>', unsafe_allow_html=True)
league_keys = list(league_codes.keys())
league = st.selectbox("L", league_keys, index=1, label_visibility="collapsed")

st.markdown(f'<p style="color:#aaa; margin-left:15px; margin-top:15px;">{d[lang]["sel_date"]}</p>', unsafe_allow_html=True)
date_option = st.radio("Date Option", d[lang]['date_opts'], horizontal=True, label_visibility="collapsed")
sel_date = st.date_input("D", value=today_mm, min_value=today_mm, label_visibility="collapsed")

# ၃။ Check Matches Now
st.markdown('<div class="check-btn-wrapper">', unsafe_allow_html=True)
check_click = st.button(d[lang]["btn_check"], key="check_btn", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if check_click:
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    
    with st.spinner('Checking Matches...'):
        try:
            token = st.secrets["api_keys"]["FOOTBALL_DATA_KEY"]
            if date_option == d[lang]['date_opts'][1]:
                d_from, d_to = today_mm, today_mm + datetime.timedelta(days=1)
            elif date_option == d[lang]['date_opts'][2]:
                d_from, d_to = today_mm, today_mm + datetime.timedelta(days=2)
            else:
                d_from = d_to = sel_date

            l_code = league_codes[league]
            if l_code == "ALL":
                target_codes = ",".join([v for k, v in league_codes.items() if v != "ALL"])
                url = f"https://api.football-data.org/v4/matches?competitions={target_codes}&dateFrom={d_from}&dateTo={d_to}"
            else:
                url = f"https://api.football-data.org/v4/competitions/{l_code}/matches?dateFrom={d_from}&dateTo={d_to}"
            
            headers = {'X-Auth-Token': token}
            response = requests.get(url, headers=headers)
            data = response.json()
            matches = data.get('matches', [])
            
            st.session_state.display_matches = [] 
            if matches:
                h_set, a_set = set(), set()
                for m in matches:
                    h, a = m['homeTeam']['name'], m['awayTeam']['name']
                    l_display = league_name_map.get(m['competition']['name'], m['competition']['name'])
                    utc_dt = datetime.datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                    mm_dt = utc_dt + datetime.timedelta(hours=6, minutes=30)
                    t_str = mm_dt.strftime("%H:%M")
                    h_set.add(h)
                    a_set.add(a)
                    # Saving utc string to re-parse later for cache expiry logic
                    st.session_state.display_matches.append({
                        'time': t_str, 'home': h, 'away': a, 'league': l_display,
                        'utc_str': m['utcDate']
                    })
                st.session_state.h_teams = sorted(list(h_set))
                st.session_state.a_teams = sorted(list(a_set))
            else:
                st.session_state.h_teams = ["No matches found"]
                st.session_state.a_teams = ["No matches found"]
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display Matches
if st.session_state.display_matches:
    grouped_matches = {}
    for match in st.session_state.display_matches:
        grouped_matches.setdefault(match['league'], []).append(match)
    
    sorted_group_titles = [k for k in league_codes.keys() if k in grouped_matches]
    
    for l_title in sorted_group_titles:
        matches_list = grouped_matches[l_title]
        st.markdown(f'<div style="color:#FFD700; font-weight:bold; margin: 15px 0 5px 15px; border-bottom: 1px solid #333;">🏆 {l_title}</div>', unsafe_allow_html=True)
        for idx, m in enumerate(matches_list, 1):
            st.markdown(f"""
                <div class="match-row">
                    <div class="col-no">#{idx}</div>
                    <div class="col-time">🕒 {m['time']}</div>
                    <div class="col-team">{m['home']}</div>
                    <div class="col-vs">VS</div>
                    <div class="col-team">{m['away']}</div>
                </div>
            """, unsafe_allow_html=True)

# ၄။ Select Team Title
st.markdown(f'<div class="title-style" style="font-size:45px; margin-top:20px;">{d[lang]["title2"]}</div>', unsafe_allow_html=True)

# --- Helper: AI Key Rotation (With Temperature 0 for Maximum Consistency) ---
def get_gemini_response_rotated(prompt):
    ai_keys = [st.secrets["gemini_keys"][f"GEMINI_KEY_{i}"] for i in range(1, 4)]
    
    for key in ai_keys:
        try:
            genai.configure(api_key=key)
            # Temperature ကို 0 ထားခြင်းဖြင့် အဖြေများ အမြဲတမ်း တည်ငြိမ်နေစေသည်
            model = genai.GenerativeModel(
                'gemini-flash-latest',
                generation_config={"temperature": 0}
            )
            return model.generate_content(prompt).text
        except Exception:
            continue 
    return "⚠️ AI Service Busy. Please try again later."

# ၅။ Home vs Away Section
c1, cvs, c2 = st.columns([2, 1, 2])

with c1:
    st.markdown(f'<p style="color:white; text-align:center; font-weight:900; font-size:12px;">{d[lang]["home"]}</p>', unsafe_allow_html=True)
    h_team = st.selectbox("H", st.session_state.h_teams, key="h", label_visibility="collapsed")

with cvs:
    st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%;"><div class="vs-ball">vs</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<p style="color:white; text-align:center; font-weight:900; font-size:12px;">{d[lang]["away"]}</p>', unsafe_allow_html=True)
    a_team = st.selectbox("A", st.session_state.a_teams, key="a", label_visibility="collapsed")

# ၆။ Orange Glossy Button & Validation Logic
st.markdown('<div class="gen-btn-wrapper">', unsafe_allow_html=True)
gen_click = st.button(d[lang]["btn_gen"], key="gen_btn", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if gen_click:
    if h_team and a_team and h_team not in ["Select Team", "No matches found"]:
        match_obj = next((m for m in st.session_state.display_matches if m['home'] == h_team and m['away'] == a_team), None)
        
        if match_obj:
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
                
            with st.spinner('AI is analyzing stats & H2H...'):
                match_utc = datetime.datetime.strptime(match_obj['utc_str'], "%Y-%m-%dT%H:%M:%SZ")
                expiry_dt = match_utc + datetime.timedelta(hours=1)
                expiry_dt_naive = datetime.datetime.now() + (expiry_dt - datetime.datetime.utcnow())
                
                # Cache key မှ lang ကို ဖြုတ်လိုက်ပါသည် (Data တစ်ခုတည်းကို နှစ်ဘာသာသုံးရန်)
                cache_key = f"pred_master_{h_team}_{a_team}_{today_mm}"
                cached_result = get_disk_cache(cache_key)

                if cached_result:
                    # Cache ရှိပါက user ရွေးထားသော language အပိုင်းကိုသာ ဖြတ်ထုတ်ပြမည်
                    parts = cached_result.split("---LANG_SPLIT---")
                    display_text = parts[1] if lang == "Burmese" else parts[0]
                    st.markdown(display_text, unsafe_allow_html=True)
                else:
                    # --- AI Prompt (Requesting Dual Language in one call) ---
                    prompt = f"""
                    Analyze {h_team} (Home) vs {a_team} (Away).
                    Respond in two parts separated by '---LANG_SPLIT---'. 
                    First part in English, Second part in Burmese.

                    LOGIC: 
                    1. Goal U/O must match Correct Score.
                    2. Best Pick must be SAFEST (Avoid Correct Score as best pick).
                    3. Both English and Burmese analyses MUST have identical betting predictions.

                    FORMAT FOR BOTH PARTS:
                    # Analysis / သုံးသပ်ချက်
                    **[Team] Form** (5 lines)
                    **[Team] Form** (5 lines)
                    **H2H** (5 lines)
                    **Home/Away Condition** (5 lines)
                    ### **Summarize Table** (Markdown Table)
                    # 🏆 **Best Pick: [Result]**
                    **Reasoning:** (6 lines)
                    """
                    
                    raw_response = get_gemini_response_rotated(prompt)
                    
                    if "---LANG_SPLIT---" in raw_response:
                        parts = raw_response.split("---LANG_SPLIT---")
                        # CSS Styling ထည့်သွင်းခြင်း
                        en_html = f'<div style="background:#0c0c0c; padding:20px; border-radius:15px; border:1px solid #39FF14; color:white;">{parts[0]}</div>'
                        mm_html = f'<div style="background:#0c0c0c; padding:20px; border-radius:15px; border:1px solid #39FF14; color:white;">{parts[1]}</div>'
                        
                        # Cache ထဲတွင် နှစ်မျိုးလုံးပေါင်းသိမ်းသည်
                        master_cache = f"{en_html}---LANG_SPLIT---{mm_html}"
                        set_disk_cache(cache_key, master_cache, expiry_dt=expiry_dt_naive)
                        
                        st.markdown(mm_html if lang == "Burmese" else en_html, unsafe_allow_html=True)
                    else:
                        st.write(raw_response)
        else:
            st.error(f"⚠️ {d[lang]['no_match']}")
    else:
        st.warning("Please select teams first!")

