import streamlit as st
import time

st.set_page_config(page_title="Safety Tracker", page_icon="🛡️")

# Matching your Wix Colors (Navy & Orange)
st.markdown("""
    <style>
    .stApp { background-color: #002060; color: white; text-align: center; }
    h1 { color: #FF8C00; }
    </style>
    """, unsafe_allow_value=True)

st.title("🛡️ Item Safety Check")
st.write("Scan confirmed. Your items are currently with you.")

# 30 Minute Safety Timer
st.divider()
st.subheader("⏰ Time until next check-in:")
placeholder = st.empty()

for i in range(1800, 0, -1):
    mins, secs = divmod(i, 60)
    placeholder.metric("Safe Window", f"{mins:02d}:{secs:02d}")
    time.sleep(1)
    if i == 1:
        st.error("⚠️ ALERT: Check-in required! Ensure all items are present.")