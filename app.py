import streamlit as st
import sys
import os
import plotly.graph_objects as go
import pandas as pd
import streamlit.components.v1 as components
import time
import pydeck as pdk

# Simple user database (username: password) and role mapping
USERS = {"admin": "admin123", "analyst": "analyst123"}
ROLES = {"admin": "admin", "analyst": "analyst"}

def location_to_coords(loc):
    mapping = {
        "India": (20.5937, 78.9629),
        "USA": (37.0902, -95.7129),
        "UK": (55.3781, -3.4360)
    }
    return mapping.get(loc, (0,0))

# Fix import path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from detect import detect_fraud


# 🔥 NEW BACKGROUND (Gradient + Floating Circles)
components.html(
    """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
        margin: 0;
        overflow: hidden;
    }

    .gradient-bg {
        position: fixed;
        width: 100%;
        height: 100%;
        background: linear-gradient(-45deg, #00ff99, #00ccff, #0033ff, #00ffcc);
        background-size: 400% 400%;
        animation: gradientMove 10s ease infinite;
        z-index: -3;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .circle {
        position: absolute;
        border-radius: 50%;
        background: rgba(0,255,255,0.2);
        animation: float 12s infinite;
    }

    .circle:nth-child(2) {
        width: 200px;
        height: 200px;
        top: 10%;
        left: 20%;
    }

    .circle:nth-child(3) {
        width: 300px;
        height: 300px;
        top: 60%;
        left: 70%;
    }

    .circle:nth-child(4) {
        width: 150px;
        height: 150px;
        top: 40%;
        left: 40%;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-40px); }
        100% { transform: translateY(0px); }
    }

    </style>
    </head>

    <body>
        <div class="gradient-bg"></div>
        <div class="circle"></div>
        <div class="circle"></div>
        <div class="circle"></div>
    </body>
    </html>
    """,
    height=0,
)


# 🔥 UI STYLING (Glass + Glow)
st.markdown(
    """
    <style>

    body, .stApp {
        color: white;
        font-family: Arial;
    }

    .block-container {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(10px);
        animation: fadeIn 1s ease-in;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }

    h1 {
        text-align: center;
        color: #00ffff;
        text-shadow: 0 0 15px #00ffff;
    }

    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        color: white;
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.1);
        box-shadow: 0px 0px 20px #00ffff;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Title
st.title("🚨 Advanced Fraud Detection Dashboard")

# 🔹 Session State for History
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['User', 'Amount', 'Location', 'Risk Score', 'Status'])

# 🔹 Sidebar for Inputs
with st.sidebar:
    # 🔐 Authentication Section
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None

    if not st.session_state.logged_in:
        st.sidebar.subheader("🔑 Login")
        login_user = st.sidebar.text_input("Username")
        login_pass = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if login_user in USERS and login_pass == USERS[login_user]:
                st.session_state.logged_in = True
                st.session_state.role = ROLES[login_user]
                st.session_state.username = login_user
                st.success(f"Logged in as {login_user} ({st.session_state.role})")
            else:
                st.sidebar.error("Invalid credentials")
        st.stop()

    # Display logged‑in user info
    st.sidebar.write(f"Logged in: **{st.session_state.username}** ({st.session_state.role})")

    st.header("📝 Transaction Details")
    user = st.selectbox("Select User", ["user1", "user2"])
    amount = st.number_input("Transaction Amount ($)", min_value=0.0, step=10.0)
    location = st.selectbox("Location", ["India", "USA", "UK"])

    
    with st.expander("⚙️ Advanced Features (29 inputs)"):
        features = []
        for i in range(29):
            val = st.number_input(f"Feature {i+1}", value=0.0)
            features.append(val)
            
    check_btn = st.button("🚀 Analyze Transaction", use_container_width=True)

# 🔹 Main Dashboard Area
if check_btn:
    with st.spinner("Analyzing transaction patterns... 🔍"):
        time.sleep(1.5)
        result, score, reasons, prob = detect_fraud(user, features, amount, location)
        
    # Add to history
    # Add to history with optional anonymization for non‑admin users
    new_record = pd.DataFrame([{'User': user, 'Amount': f"${amount:.2f}", 'Location': location, 'Risk Score': f"{score:.1f}/100", 'Status': result}])
    st.session_state.history = pd.concat([new_record, st.session_state.history], ignore_index=True)

    # If the current user is not admin, mask usernames in the displayed history
    def mask_user(name):
        return name[:2] + "***" if st.session_state.role != "admin" else name

    display_history = st.session_state.history.copy()
    display_history['User'] = display_history['User'].apply(mask_user)

    # 🔹 Top Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Risk Score", value=f"{score:.1f}", delta=f"{(prob*100):.1f}% Confidence", delta_color="inverse")
    col2.metric(label="Transaction Amount", value=f"${amount:.2f}")
    col3.metric(label="Location", value=location)

    # 🔹 Middle Row: Gauge Chart & Details
    col_chart, col_details = st.columns([1.2, 1])
    
    with col_chart:
        st.subheader("📊 Risk Meter")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Fraud Probability", 'font': {'color': 'white'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "white"},
                'bar': {'color': "rgba(0,0,0,0)"},
                'steps': [
                    {'range': [0, 30], 'color': "#00ffcc"},
                    {'range': [30, 70], 'color': "#ffcc00"},
                    {'range': [70, 100], 'color': "#ff3333"}],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': score}
            }
        ))
        fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)

    with col_details:
        st.subheader("📋 Analysis Report")
        if "Fraud" in result:
            st.error(f"🚨 ALERT: {result}")
        elif "Suspicious" in result:
            st.warning(f"⚠️ WARNING: {result}")
        else:
            st.success(f"✅ CLEAR: {result}")
            
        st.markdown("**Flagged Reasons:**")
        if reasons:
            for r in reasons:
                st.markdown(f"- 🚩 {r}")
        else:
            st.markdown("- No suspicious indicators found.")

    # 🔹 Bottom Row: History
    st.subheader("🕰️ Recent Transactions")
    st.dataframe(display_history.head(5), use_container_width=True)

# 🗺️ Geospatial Map of recent transactions (admin sees all, analyst sees masked usernames)
if st.session_state.history.shape[0] > 0:
    # Prepare coordinates for each location
    def _coords(row):
        lat, lon = location_to_coords(row["Location"])
        return pd.Series({"lat": lat, "lon": lon})
    coords_df = st.session_state.history.apply(_coords, axis=1)
    map_df = st.session_state.history.copy()
    map_df["lat"] = coords_df["lat"]
    map_df["lon"] = coords_df["lon"]
    # Remove entries without valid coordinates (0,0)
    map_df = map_df[(map_df["lat"] != 0) & (map_df["lon"] != 0)]
    if not map_df.empty:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position="[lon, lat]",
            get_fill_color=[255, 0, 0, 140],
            get_radius=50000,
        )
        view_state = pdk.ViewState(latitude=20, longitude=78, zoom=1)
        deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{User}: {Location}"})
        st.pydeck_chart(deck)


else:
    st.info("👈 Enter transaction details in the sidebar and click 'Analyze Transaction' to begin.")
    
    # Show history if exists even when not checking
    if not st.session_state.history.empty:
        st.subheader("🕰️ Recent Transactions")
        st.dataframe(st.session_state.history.head(5), use_container_width=True)