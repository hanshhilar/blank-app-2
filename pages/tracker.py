import streamlit as st
import time
from datetime import datetime

# Matching your Wix Navy and Orange
NAVY_BLUE = "#002060"
ORANGE = "#FF8C00"

st.set_page_config(page_title="Item Safety Check", page_icon="🛡️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: white; }}
    h1, h3 {{ color: {NAVY_BLUE}; }}
    .stButton>button {{
        background-color: {ORANGE};
        color: white;
        border-radius: 25px;
        width: 100%;
        height: 3em;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_value=True)

st.title("🛡️ Item Safety Verified")
st.write("Scan successful. Your item is marked as **Present**.")

# Record the scan
current_time = datetime.now().strftime("%I:%M %p")
st.success(f"Verified at {current_time}")

# Timer Logic
st.divider()
st.subheader("⏰ Next Check-in")
st.write("To ensure your belongings stay with you, please re-scan in:")

# A 30-minute countdown for your commute
countdown_placeholder = st.empty()
for i in range(1800, 0, -1):
    mins, secs = divmod(i, 60)
    countdown_placeholder.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
    time.sleep(1)
    if i == 1:
        st.error("⚠️ ALERT: Item not scanned in time! Check your surroundings.")