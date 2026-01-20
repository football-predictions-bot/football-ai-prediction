import streamlit as st
import datetime
import requests
from google import genai  # Warning ပျောက်ရန် Version အသစ်သို့ ပြောင်းလဲခြင်း
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
CACHE_DIR = "/tmp/data_cache"
try:
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR, exist_ok=True)
except Exception:
    CACHE_DIR = "/tmp"

def get_disk_cache(key):
    safe_key = key.replace("/", "_")
    file_path = os.path.join(CACHE_DIR, f"{safe_key}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                cache_data = json.load(f)
                expiry = datetime.datetime.fromisoformat(cache_data['expiry'])
                # Timezone-aware object သုံး၍ နှိုင်းယှဉ်ခြင်း
                if datetime.datetime.now(datetime.timezone.utc) < expiry.replace(tzinfo=datetime.timezone.utc):
                    return cache_data['data']
        except:
            return None
    return None

def set_disk_cache(key, data, expiry_dt=None, days=19):
    if expiry_dt is None:
        expiry_dt = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=days)
    
    safe_key = key.replace("/", "_")
    file_path = os.path.join(CACHE_DIR, f"{safe_key}.json")
    try:
        with open(file_path, "w") as f:
            json.dump({'data': data, 'expiry': expiry_dt.isoformat()}, f)
    except Exception as e:
        st.sidebar.error(f"Cache Error: {str(e)}")

# Time Handling (Warning ပျောက်ရန် utcnow အစား timezone-aware object သုံးခြင်း)
now_mm = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=6, minutes=30)
today_mm = now_mm.date()
yesterday_mm = today_mm - datetime.timedelta(days=1)
tomorrow_mm = today_mm + datetime.timedelta(days=1)

# ၁။ Dictionary & Session State
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
if 'h_teams' not in st.session_state:
    st.session_state.h_teams = ["Select Team"]
if 'a_teams' not in st.session_state:
    st.session_state.a_teams = ["Select Team"]
if 'display_matches' not in st.session_state:
    st.session_state.display_matches = []
if 'check_performed' not in st.session_state:
    st.session_state.check_performed = False

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
        'no_match': 'No match found between these teams! Please check the Match Table.',
        'no_fixture': 'No matches available for this date.'
    },
    'MM': {
        'title1': 'ပွဲကြိုခန့်မှန်းချက်များ', 'sel_league': 'လိဂ်ကို ရွေးချယ်ပါ', 'sel_date': 'ရက်စွဲကို ရွေးချယ်ပါ',
        'btn_check': 'ပွဲစဉ်များကို စစ်ဆေးမည်', 'title2': 'အသင်းကို ရွေးချယ်ပါ',
        'home': 'အိမ်ရှင်အသင်း', 'away': 'ဧည့်သည်အသင်း', 'btn_gen': 'ခန့်မှန်းချက် ထုတ်ယူမည်',
        'trans_btn': 'Switch to English',
        'date_opts': ["ရက်စွဲတပ်၍ရှာမည်", "၂၄ နာရီအတွင်း", "၄၈ နာရီအတွင်း"],
        'ai_lang': 'Burmese',
        'no_match': 'ရွေးထားသော ပွဲစဉ်မရှိပါ။ Match Table ကို ပြန်စစ်ပါ။',
        'no_fixture': 'ရွေးထားသော ရက်စွဲတွင် ပွဲစဉ်မရှိပါ။'
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
    st.session_state.check_performed = True
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    
    with st.spinner('Checking Matches...'):
        try:
            l_code = league_codes[league]
            table_cache_key = f"table_v2_{l_code}_{sel_date}_{date_option}"
            cached_table = get_disk_cache(table_cache_key)

            if cached_table:
                st.session_state.display_matches = cached_table['matches']
                st.session_state.h_teams = cached_table['h_teams']
                st.session_state.a_teams = cached_table['a_teams']
            else:
                token = st.secrets["api_keys"]["FOOTBALL_DATA_KEY"]
                if date_option == d[lang]['date_opts'][1]:
                    d_from, d_to = today_mm, today_mm + datetime.timedelta(days=1)
                elif date_option == d[lang]['date_opts'][2]:
                    d_from, d_to = today_mm, today_mm + datetime.timedelta(days=2)
                else:
                    d_from = d_to = sel_date

                d_from_api = d_from - datetime.timedelta(days=1)
                d_to_api = d_to + datetime.timedelta(days=1)

                if l_code == "ALL":
                    target_codes = ",".join([v for k, v in league_codes.items() if v != "ALL"])
                    url = f"https://api.football-data.org/v4/matches?competitions={target_codes}&dateFrom={d_from_api}&dateTo={d_to_api}"
                else:
                    url = f"https://api.football-data.org/v4/competitions/{l_code}/matches?dateFrom={d_from_api}&dateTo={d_to_api}"
                
                headers = {'X-Auth-Token': token}
                response = requests.get(url, headers=headers)
                data = response.json()
                matches = data.get('matches', [])
                
                st.session_state.display_matches = [] 
                if matches:
                    h_set, a_set = set(), set()
                    for m in matches:
                        if m['status'] in ['SCHEDULED', 'TIMED']:
                            utc_dt = datetime.datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                            mm_dt = utc_dt + datetime.timedelta(hours=6, minutes=30)
                            
                            if d_from <= mm_dt.date() <= d_to:
                                h, a = m['homeTeam']['name'], m['awayTeam']['name']
                                h_logo = m['homeTeam'].get('crest', '')
                                a_logo = m['awayTeam'].get('crest', '')
                                l_display = league_name_map.get(m['competition']['name'], m['competition']['name'])
                                dt_str = mm_dt.strftime("%d/%m %H:%M")
                                h_set.add(h)
                                a_set.add(a)
                                st.session_state.display_matches.append({
                                    'datetime': dt_str, 'home': h, 'away': a, 'league': l_display,
                                    'h_logo': h_logo, 'a_logo': a_logo, 'utc_str': m['utcDate']
                                })
                    
                    st.session_state.h_teams = sorted(list(h_set)) if h_set else ["No matches found"]
                    st.session_state.a_teams = sorted(list(a_set)) if a_set else ["No matches found"]
                    
                    cache_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=59)
                    set_disk_cache(table_cache_key, {
                        'matches': st.session_state.display_matches,
                        'h_teams': st.session_state.h_teams,
                        'a_teams': st.session_state.a_teams
                    }, expiry_dt=cache_expiry)
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
                <div class="match-row" style="height: auto; padding: 15px 10px;">
                    <div class="col-no">#{idx}</div>
                    <div class="col-time" style="font-size: 11px;">📅 {m['datetime']}</div>
                    <div class="col-team" style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                        <img src="{m['h_logo']}" width="30" style="margin-bottom:5px;">
                        <div>{m['home']}</div>
                    </div>
                    <div class="col-vs">VS</div>
                    <div class="col-team" style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                        <img src="{m['a_logo']}" width="30" style="margin-bottom:5px;">
                        <div>{m['away']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
elif st.session_state.check_performed:
    st.markdown(f"""
        <div style="background-color:rgba(255,0,0,0.1); padding:20px; border-radius:10px; border:1px solid #ff4b4b; text-align:center; margin:20px;">
            <h3 style="color:#ff4b4b; margin:0;">⚠️ Warning</h3>
            <p style="color:white; font-size:18px; margin-top:10px;">{d[lang]['no_fixture']}</p>
        </div>
    """, unsafe_allow_html=True)

# ၄။ Select Team Title
st.markdown(f'<div class="title-style" style="font-size:45px; margin-top:20px;">{d[lang]["title2"]}</div>', unsafe_allow_html=True)

# --- Helper: API-Sports Data Fetching with Route (Key Rotation) ---
def get_api_sports_stats(h_team, a_team, match_date, h_id=None, a_id=None):
    api_keys = [st.secrets["api_keys"][f"APISPORTS_KEY_{i}"] for i in range(1, 5)]
    headers_list = [{'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': key} for key in api_keys]
    
    for headers in headers_list:
        try:
            # ၁။ Fixture ID ရှာဖွေခြင်း
            search_url = f"https://v3.football.api-sports.io/fixtures?date={match_date}"
            res = requests.get(search_url, headers=headers, timeout=10).json()
            
            fixture_obj = None
            if 'response' in res and res['response']:
                for f in res['response']:
                    if (h_team.lower() in f['teams']['home']['name'].lower() or f['teams']['home']['name'].lower() in h_team.lower()):
                        fixture_obj = f
                        break
            
            if not fixture_obj: continue 
            f_id = fixture_obj['fixture']['id']
            h_team_id = fixture_obj['teams']['home']['id']
            a_team_id = fixture_obj['teams']['away']['id']

            # ၂။ Predictions & Stats
            pred_res = requests.get(f"https://v3.football.api-sports.io/predictions?fixture={f_id}", headers=headers, timeout=10).json()
            
            # ၃။ Injuries
            inj_res = requests.get(f"https://v3.football.api-sports.io/injuries?fixture={f_id}", headers=headers, timeout=10).json()

            # ၄။ Player Ratings & Stats (Last 5 Matches)
            h_last_stats = requests.get(f"https://v3.football.api-sports.io/fixtures?team={h_team_id}&last=5&status=FT", headers=headers, timeout=10).json()
            a_last_stats = requests.get(f"https://v3.football.api-sports.io/fixtures?team={a_team_id}&last=5&status=FT", headers=headers, timeout=10).json()

            # ၅။ Fixture Schedule (Next matches to check congestion)
            h_next = requests.get(f"https://v3.football.api-sports.io/fixtures?team={h_team_id}&next=2", headers=headers, timeout=10).json()
            a_next = requests.get(f"https://v3.football.api-sports.io/fixtures?team={a_team_id}&next=2", headers=headers, timeout=10).json()

            return {
                'analysis': pred_res.get('response', [None])[0],
                'injuries': inj_res.get('response', []),
                'h_last_5': h_last_stats.get('response', []),
                'a_last_5': a_last_stats.get('response', []),
                'h_schedule': h_next.get('response', []),
                'a_schedule': a_next.get('response', [])
            }
        except:
            continue 
    return None

# --- Helper: AI Key Rotation ---
def get_gemini_response_rotated(prompt):
    ai_keys = [st.secrets["gemini_keys"][f"GEMINI_KEY_{i}"] for i in range(1, 4)]
    for key in ai_keys:
        try:
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt,
                config={'temperature': 0}
            )
            return response.text
        except:
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
                
            with st.spinner('AI is analyzing stats, player ratings & match congestion...'):
                match_utc = datetime.datetime.strptime(match_obj['utc_str'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
                expiry_dt_naive = datetime.datetime.now() + (match_utc + datetime.timedelta(hours=1) - datetime.datetime.now(datetime.timezone.utc))
                
                cache_key = f"pred_hybrid_v5_last5_{h_team}_{a_team}_{today_mm}"
                cached_result = get_disk_cache(cache_key)

                if cached_result:
                    st.markdown(cached_result, unsafe_allow_html=True)
                else:
                    real_data = get_api_sports_stats(h_team, a_team, today_mm.isoformat())
                    
                    stats_context = "No detailed real-time data available."
                    if real_data:
                        analysis = real_data.get('analysis', {})
                        comp = analysis.get('comparison', {})
                        advice = analysis.get('advice', 'No direct advice')
                        
                        # Formatting Last 5 Matches
                        h_last_5_results = []
                        for m in real_data.get('h_last_5', []):
                            res = f"{m.get('teams',{}).get('home',{}).get('name')} {m.get('goals',{}).get('home')}-{m.get('goals',{}).get('away')} {m.get('teams',{}).get('away',{}).get('name')}"
                            h_last_5_results.append(res)
                        
                        a_last_5_results = []
                        for m in real_data.get('a_last_5', []):
                            res = f"{m.get('teams',{}).get('home',{}).get('name')} {m.get('goals',{}).get('home')}-{m.get('goals',{}).get('away')} {m.get('teams',{}).get('away',{}).get('name')}"
                            a_last_5_results.append(res)

                        h_next_game = real_data['h_schedule'][0].get('fixture', {}).get('date', 'N/A') if real_data.get('h_schedule') else "N/A"
                        a_next_game = real_data['a_schedule'][0].get('fixture', {}).get('date', 'N/A') if real_data.get('a_schedule') else "N/A"
                        
                        inj_list = [i.get('player', {}).get('name', 'Unknown') for i in real_data.get('injuries', [])]

                        stats_context = f"""
                        CURRENT DATA (DATE: {datetime.date.today()}):
                        - {h_team} Last 5 Matches: {', '.join(h_last_5_results)}
                        - {a_team} Last 5 Matches: {', '.join(a_last_5_results)}
                        - Next Match: {h_team}: {h_next_game} | {a_team}: {a_next_game}
                        - Comparison: Home Att {comp.get('att', {}).get('home')}, Def {comp.get('def', {}).get('home')} | Away Att {comp.get('att', {}).get('away')}, Def {comp.get('def', {}).get('away')}
                        - Injuries: {', '.join(inj_list) if inj_list else 'None'}
                        - API Advice: {advice}
                        """

                    prompt = f"""
                    SYSTEM INSTRUCTION: You are a professional football analyst in 2026. 
                    IGNORE all your pre-training memory about team coaches, squads, or player locations. 
                    STRICTLY use the provided CURRENT DATA. 
                    
                    {stats_context}
                    
                    Analyze {h_team} vs {a_team}. 
                    Consider "Match Congestion" (Rest days) and "Squad Rotation" if the next match is a major tournament or very close.
                    Identify if a team is in a "Goal Drought" (last 5 matches) or "Poor Form".
                    Respond strictly in BURMESE language (Unicode).

                    OUTPUT FORMAT:
                    # သုံးသပ်ချက်
                    **{h_team} Form & Squad Analysis** (နောက်ဆုံး ၅ ပွဲရလဒ်နှင့် ခြေစွမ်းကိုအခြေခံ၍ ၅ ကြောင်း)
                    **{a_team} Form & Squad Analysis** (နောက်ဆုံး ၅ ပွဲရလဒ်နှင့် ခြေစွမ်းကိုအခြေခံ၍ ၅ ကြောင်း)
                    **ပွဲပန်းမှုနှင့် လူချန်နိုင်မှု** (နောက်ပွဲရက်စွဲနှင့် အရေးကြီးပုံကိုကြည့်၍ ၅ ကြောင်း)
                    **အိမ်ကွင်း/အဝေးကွင်း အခြေအနေ** (၅ ကြောင်း)

                    ### **Summarize Table**
                    | Category | Prediction |
                    | :--- | :--- |
                    | Winner Team | [မြန်မာလိုဖြေပါ] |
                    | Correct Score | [Result] |
                    | Goal under/over | [Result] |
                    | Corners under/over | [Result] |
                    | Yellow Card under/over | [Result] |
                    | Both Teams To Score yes/no | [Result] |

                    # **🏆 အဖြစ်နိုင်ဆုံးနှင့် အန္တရာယ်အကင်းဆုံးရွေးချယ်မှု: [ရလဒ်ကို Bold ဖြင့်ပြပါ]**
                    Reasoning: (နောက်ဆုံး ၅ ပွဲ၏ Statistics နှင့် ပွဲပန်းမှုကို အခြေခံ၍ ၆ ကြောင်း အတိအကျဖြေပါ)
                    """
                    
                    response_text = get_gemini_response_rotated(prompt)
                    final_output = f'<div style="background:#0c0c0c; padding:20px; border-radius:15px; border:1px solid #39FF14; color:white;">{response_text}</div>'
                    set_disk_cache(cache_key, final_output, expiry_dt=expiry_dt_naive)
                    st.markdown(final_output, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ {d[lang]['no_match']}")
    else:
        st.warning("Please select teams first!")

