import streamlit as st
import time

st.set_page_config(page_title="Travel Checklist", layout="centered")

# Navy and Orange styling
st.markdown("""
    <style>
    .stApp { background-color: white; color: #002060; }
    h1 { color: #FF8C00; }
    .stCheckbox { font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_value=True)

st.title("🧳 Smart Travel Checklist")
st.write("Scan your items as you pack to ensure nothing is left behind.")

# 1. Initialize the checklist in "Session State" so it remembers what you scanned
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = {
        "Passport": False,
        "Laptop": False,
        "Charger": False,
        "Wallet": False
    }

# 2. The "Scanner" Input
# In a real app, this would be a camera scan. For your demo, 
# you can type the name of the item you "scanned".
scan_input = st.text_input("📷 Simulate Scan (Type item name):", placeholder="e.g. Passport")

if scan_input:
    # Check if the scanned item is in our list
    matched = False
    for item in st.session_state.scanned_items:
        if scan_input.lower() == item.lower():
            st.session_state.scanned_items[item] = True
            st.success(f"✅ {item} verified and packed!")
            matched = True
            time.sleep(1)
            st.rerun()
    
    if not matched and scan_input != "":
        st.error(f"⚠️ Warning: '{scan_input}' is not on your travel list!")

# 3. Display the Checklist
st.divider()
st.subheader("Your Packing Progress")

all_packed = True
for item, status in st.session_state.scanned_items.items():
    if status:
        st.write(f"🟢 **{item}** — Packed")
    else:
        st.write(f"⚪ {item} — *Missing*")
        all_packed = False

# 4. Final Reminder
if all_packed:
    st.balloons()
    st.success("🎉 Everything is packed! You are ready for your journey.")
else:
    st.warning("🚨 Reminder: You still have items left to scan!")

if st.button("Reset Checklist"):
    for item in st.session_state.scanned_items:
        st.session_state.scanned_items[item] = False
    st.rerun()