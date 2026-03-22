import streamlit as st
import time

# Set page config FIRST
st.set_page_config(page_title="Safety Tracker", layout="centered")

# Simpler way to set colors
st.title("🛡️ Item Safety Check")
st.subheader("Your belongings are verified.")

# Use a container for the timer
with st.container():
    st.write("---")
    st.write("Next check-in required in:")
    placeholder = st.empty()

    # 30-minute commute timer
    for i in range(1800, 0, -1):
        mins, secs = divmod(i, 60)
        # Displaying the time clearly
        placeholder.metric(label="Time Remaining", value=f"{mins:02d}:{secs:02d}")
        time.sleep(1)
        if i == 1:
            st.error("⚠️ ALERT: Time up! Please re-scan your QR code.")