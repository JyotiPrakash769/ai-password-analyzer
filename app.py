import streamlit as st
import os
import plotly.graph_objects as go
from src.predictor import PasswordPredictor
from src.utils import estimate_crack_time, generate_ai_password, check_pwned_password, simulate_hash_cracking
from st_keyup import st_keyup
import zxcvbn

# Set up the Streamlit page layout and title
st.set_page_config(page_title="Pro-Level Password Analyzer", page_icon="🛡️", layout="wide")

# Apply Cyber/Hacker Custom CSS Theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .stTextInput>div>div>input {
        background-color: #161b22;
        color: #58a6ff;
        border: 1px solid #30363d;
        border-radius: 6px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.3);
    }
    .metric-container {
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 15px;
        background-color: #161b22;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Pro-Level AI Password Suite")
st.markdown("*Analyze brute-force resistance, visualize weakness metrics, and generate uncrackable AI-powered keys.*")

# Attempt to initialize the predictor which loads the AI model
try:
    predictor = PasswordPredictor()
    model_loaded = True
except FileNotFoundError:
    st.error("⚠️ **Model not found!**\nPlease run the training pipeline first by executing:\n`python -m src.train_model`")
    model_loaded = False

if model_loaded:
    tab1, tab2 = st.tabs(["📊 Live Neural Analyzer", "✨ AI Key Generator"])
    
    with tab1:
        st.subheader("Live Typing Analysis")
        
        # Preserve password state across widget key changes
        if "current_pwd" not in st.session_state:
            st.session_state.current_pwd = ""
            
        # Toggle for password visibility
        show_password = st.toggle("👁️ Show Password", value=False)
        input_type = "default" if show_password else "password"
        
        # Using a dynamic key is necessary because Streamlit prevents changing widget 'type' on the same key
        widget_key = "pwd_input_visible" if show_password else "pwd_input_hidden"
        
        # Use st_keyup for real-time analysis without pressing enter
        password_input = st_keyup(
            "Enter a password to analyze:", 
            value=st.session_state.current_pwd,
            type=input_type, 
            key=widget_key
        )
        
        # Always update our backup state so it's not lost when toggling
        if password_input is not None:
            st.session_state.current_pwd = password_input
        
        if password_input:
            # 1. Advanced Metrics & Zxcvbn
            strength, features = predictor.predict_strength(password_input)
            crack_time = estimate_crack_time(password_input)
            z_results = zxcvbn.zxcvbn(password_input)
            
            # Map predictions to UI colors and gauges
            if strength == 'weak':
                color = "#ff4a4a" # Neon Red
                score = 25
            elif strength == 'medium':
                color = "#ffb000" # Neon Orange
                score = 65
            else:
                color = "#00e676" # Neon Green
                score = 100
                
            # Create Advanced Gauge Meter using Plotly
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "AI Security Rating", 'font': {'size': 20, 'color': '#c9d1d9'}},
                number = {'font': {'color': '#c9d1d9'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': color},
                    'bgcolor': "#161b22",
                    'borderwidth': 2,
                    'bordercolor': "#30363d",
                    'steps': [
                        {'range': [0, 33], 'color': 'rgba(255, 74, 74, 0.1)'},
                        {'range': [33, 67], 'color': 'rgba(255, 176, 0, 0.1)'},
                        {'range': [67, 100], 'color': 'rgba(0, 230, 118, 0.1)'}],
                }
            ))
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            
            # Layout for top section
            col1, col2 = st.columns([1.5, 1])
            with col1:
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                st.markdown(f"### Score: <span style='color:{color}; font-weight:bold; text-shadow: 0 0 5px {color};'>{strength.upper()}</span>", unsafe_allow_html=True)
                st.metric(label="Estimated Brute Force Time", value=crack_time)
                st.metric(label="Shannon Entropy", value=f"{features['entropy']:.2f} bits")
                st.metric(label="Zxcvbn Score", value=f"{z_results['score']}/4")

            # 2. HIBP Data Breach Integration
            st.divider()
            with st.spinner("Checking global data breach databases..."):
                leak_count = check_pwned_password(password_input)
                if leak_count > 0:
                    st.error(f"🚨 **CRITICAL WARNING:** This password has appeared in **{leak_count:,}** public data breaches! DO NOT USE IT.")
                elif leak_count == -1:
                    st.warning("⚠️ Could not reach the Have I Been Pwned API. Skipping breach check.")
                else:
                    st.success("✅ **CLEAN:** This password has not been found in known data breaches (k-Anonymity verified).")

            st.divider()
            
            # 2.5 Real-world Hash Cracking Simulator
            st.subheader("⏱️ Multi-Algorithm Hash Cracking Simulator")
            st.markdown("*Estimated time to brute-force offline using high-end dedicated cracking hardware (e.g. 8x RTX 4090).*")
            
            crack_sim = simulate_hash_cracking(password_input)
            sim_cols = st.columns(len(crack_sim))
            
            for i, (algo, time_str) in enumerate(crack_sim.items()):
                with sim_cols[i]:
                    # Make fast cracking times red, slow ones green
                    if "seconds" in time_str or "Instantly" in time_str or "minutes" in time_str:
                        st.markdown(f"**{algo}**<br><span style='color:#ff4a4a; font-size:1.2em; font-weight:bold;'>{time_str}</span>", unsafe_allow_html=True)
                    elif "hours" in time_str or "days" in time_str:
                        st.markdown(f"**{algo}**<br><span style='color:#ffb000; font-size:1.2em; font-weight:bold;'>{time_str}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**{algo}**<br><span style='color:#00e676; font-size:1.2em; font-weight:bold;'>{time_str}</span>", unsafe_allow_html=True)

            st.divider()
            # 3. Radar Chart + Composition
            rc1, rc2 = st.columns(2)
            
            with rc1:
                # Radar Chart
                st.subheader("🛡️ Defense Vectors")
                radar_fig = go.Figure(data=go.Scatterpolar(
                  r=[min(features['length']/16, 1)*100, 
                     min(features['uppercase_count'], 1)*100, 
                     min(features['digits_count'], 1)*100, 
                     min(features['special_count'], 1)*100,
                     (z_results['score']/4)*100],
                  theta=['Length','Uppercase','Digits','Symbols', 'Unpredictability'],
                  fill='toself',
                  line_color=color,
                  fillcolor='rgba(88, 166, 255, 0.2)' # Adding alpha safely
                ))
                radar_fig.update_layout(
                  polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor='#30363d', linecolor='#30363d'),
                    angularaxis=dict(gridcolor='#30363d', linecolor='#30363d')
                  ),
                  showlegend=False,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  font=dict(color='#c9d1d9'),
                  margin=dict(t=30, b=30, l=30, r=30)
                )
                st.plotly_chart(radar_fig, width='stretch')
                
            with rc2:
                # Cool Bars for Composition
                st.subheader("🧩 Character Matrix")
                comp_fig = go.Figure(data=[
                    go.Bar(name='Uppercase', x=['Matrix'], y=[features['uppercase_count']], marker_color='#58a6ff'),
                    go.Bar(name='Lowercase', x=['Matrix'], y=[features['lowercase_count']], marker_color='#1f6feb'),
                    go.Bar(name='Digits', x=['Matrix'], y=[features['digits_count']], marker_color='#238636'),
                    go.Bar(name='Special', x=['Matrix'], y=[features['special_count']], marker_color='#da3633')
                ])
                comp_fig.update_layout(
                    barmode='group', 
                    height=350, 
                    margin=dict(t=30, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#c9d1d9'),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(gridcolor='#30363d')
                )
                st.plotly_chart(comp_fig, width='stretch')
            
            st.divider()
            
            # Improvement Suggestions Section
            st.subheader("💡 Actionable AI Recommendations")
            
            # Combine our ML suggestions with zxcvbn's warnings
            suggestions = predictor.get_suggestions(password_input, features)
            if z_results['feedback']['warning']:
                 suggestions.insert(0, f"**Zxcvbn Warning:** {z_results['feedback']['warning']}")
                 
            if len(suggestions) == 1 and suggestions[0].startswith("Great job!"):
                st.success(suggestions[0])
            else:
                for suggestion in suggestions:
                    st.warning(f"🔧 {suggestion}")
                        
    with tab2:
        st.subheader("AI Powered Password Generator")
        st.write("Generate an unbreakable, high-entropy cryptographic key instantly.")
        
        plength = st.slider("Select Desired Length", min_value=12, max_value=64, value=18)
        
        if st.button("Generate Secure Password", type="primary"):
            new_pass = generate_ai_password(plength)
            time_to_crack = estimate_crack_time(new_pass)
            
            st.success("Key successfully generated! Copy it below:")
            st.code(new_pass, language='')
            
            # Show a mini metric for the new password
            mcol1, mcol2 = st.columns(2)
            mcol1.metric("Generated Length", f"{plength} characters")
            mcol2.metric("Brute Force Resistance", time_to_crack)
            st.info("💡 Pro Tip: Use a password manager to store this securely.")
