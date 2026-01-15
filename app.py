import streamlit as st
import datetime
import requests
import google.generativeai as genai
import random

# ၁။ CSS ချိတ်ဆက်ခြင်း
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Football Predictions")

# ၂။ League ၆ ခု စာရင်း (API ID များဖြင့်)
league_map = {
    "Premier League": 39,
    "Champions League": 2,
    "La Liga": 140,
    "Bundesliga": 78,
    "Serie A": 135,
    "Ligue 1": 61
}

# ၃။ UI Layout (League ရွေးရန်)
st.markdown("<p style='margin-bottom:0;'>Select League</p>", unsafe_allow_html=True)
selected_league_name = st.selectbox(
    "League Selector",
    options=list(league_map.keys()),
    label_visibility="collapsed"
)

# ရွေးထားတဲ့ League ရဲ့ ID ကို သိမ်းထားခြင်း (နောက်ပိုင်း API ခေါ်ဖို့)
selected_league_id = league_map[selected_league_name]

# ၄။ Date ရွေးရန်
st.markdown("<p style='margin-bottom:0; margin-top:10px;'>Select Date</p>", unsafe_allow_html=True)
sel_date = st.date_input(
    "Date Selector", 
    value=datetime.date(2026, 1, 17),
    label_visibility="collapsed"
)

# ၅။ Check Match Button (Purple Neon)
if st.button("Check Match"):
    st.write(f"Selected League ID: {selected_league_id} for {sel_date}")
        try:
            prompt = f"Predict the score and winner for {home} vs {away} in {sel_league}. Write in Burmese."
            response = model.generate_content(prompt)
            st.success("Analysis Complete!")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    st.markdown("<div style='text-align:center; font-weight:bold; color:#ff4500;'>AWAY TEAM</div>", unsafe_allow_html=True)
    away_team = st.selectbox("Away", list(team_ids.keys()), index=1, label_visibility="collapsed")

# --- SECTION 3: THE BIG ORANGE BUTTON ---
if st.button("Predictions"):
    
    # 1. Date Search Result
    date_str = sel_date.strftime('%Y-%m-%d')
    with st.spinner('Checking Schedule...'):
        matches = get_matches_by_date(leagues[sel_league], date_str)
        if matches:
            st.success(f"Matches found for {sel_league} on {date_str}")
        else:
            st.warning(f"No matches scheduled for {sel_league} on {date_str}")

    # 2. Team Analysis (API + AI)
    with st.spinner(f'Analyzing {home_team} vs {away_team}...'):
        h_form = get_team_form(team_ids[home_team])
        a_form = get_team_form(team_ids[away_team])
        
        if h_form and a_form:
            # Preparing Data for AI
            summary = f"Analysis for {home_team} vs {away_team}:\n"
            summary += f"\n{home_team} Last 5 Matches:\n"
            for m in h_form:
                summary += f"{m['teams']['home']['name']} {m['goals']['home']}-{m['goals']['away']} {m['teams']['away']['name']}\n"
            
            summary += f"\n{away_team} Last 5 Matches:\n"
            for m in a_form:
                summary += f"{m['teams']['home']['name']} {m['goals']['home']}-{m['goals']['away']} {m['teams']['away']['name']}\n"
            
            # AI Prediction
            try:
                model = get_rotated_model()
                prompt = f"You are a football expert. Based ONLY on these results:\n{summary}\nPredict the winner and score for the upcoming match between {home_team} and {away_team}. Write in Burmese."
                response = model.generate_content(prompt)
                
                # Display Result Card
                st.markdown(f"""
                <div class='match-card'>
                    <h3 style='color:#39FF14;'>🤖 AI Prediction</h3>
                    <p>{response.text}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show Raw Data (Last 5 Games)
                st.write("---")
                c_a, c_b = st.columns(2)
                with c_a:
                    st.caption(f"{home_team} Recent Form")
                    for m in h_form:
                        st.text(f"{m['goals']['home']}-{m['goals']['away']} vs {m['teams']['away']['name'] if m['teams']['home']['name'] == home_team else m['teams']['home']['name']}")
                with c_b:
                    st.caption(f"{away_team} Recent Form")
                    for m in a_form:
                        st.text(f"{m['goals']['home']}-{m['goals']['away']} vs {m['teams']['away']['name'] if m['teams']['home']['name'] == away_team else m['teams']['home']['name']}")

            except Exception as e:
                st.error("AI Limit Reached. Please wait a moment.")
        else:
            st.error("Could not fetch team data. Please check API Key.")

# Footer
st.markdown("<br><center><small style='color:gray'>Powered by Gemini & API-Sports</small></center>", unsafe_allow_html=True)
