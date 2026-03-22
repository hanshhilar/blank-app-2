import streamlit as st
import time

# This hides the sidebar and the "Made with Streamlit" footer
st.set_page_config(page_title="Safety Tracker", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stApp { background-color: #002060; color: white; text-align: center; }
    h1 { color: #FF8C00; }
    </style>
    """, unsafe_allow_value=True)

st.title("🛡️ Item Safety Check")
st.write("Scan confirmed. Your items are currently with you.")

# Timer Logic
st.divider()
st.subheader("⏰ Next check-in in:")
placeholder = st.empty()

# 30 Minute Timer
for i in range(1800, 0, -1):
    mins, secs = divmod(i, 60)
    placeholder.metric("Safe Window", f"{mins:02d}:{secs:02d}")
    time.sleep(1)