import streamlit as st
import time

st.set_page_config(page_title="Travel Checklist", layout="centered")

st.title("🧳 Smart Travel Checklist")

# 1. Initialize the checklist in Session State
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = {
        "Passport": False,
        "Laptop": False,
        "Charger": False,
        "Wallet": False
    }

# 2. THE SCANNER LOGIC (Automatic Check)
# This reads the URL: .../travel?check=Passport
query_params = st.query_params
check_item = query_params.get("check")

if check_item:
    # Capitalize to match our dictionary keys
    item_to_tick = check_item.strip().capitalize()
    
    if item_to_tick in st.session_state.scanned_items:
        if not st.session_state.scanned_items[item_to_tick]:
            st.session_state.scanned_items[item_to_tick] = True
            st.success(f"✅ {item_to_tick} Scanned & Verified!")
            time.sleep(1)
            # Clear the URL parameter so it doesn't keep "scanning" on refresh
            st.query_params.clear()
            st.rerun()

# 3. Visual Checklist Display
st.divider()
packed_count = sum(st.session_state.scanned_items.values())
total_count = len(st.session_state.scanned_items)

st.progress(packed_count / total_count)

for item, is_packed in st.session_state.scanned_items.items():
    if is_packed:
        st.write(f"✅ **{item}** — Packed")
    else:
        st.write(f"❌ {item} — *Waiting for Scan*")

# 4. Final Alert
if packed_count == total_count:
    st.balloons()
    st.success("🎉 All items verified. Safe travels to Kannur!")

if st.button("Reset All Ticks"):
    for key in st.session_state.scanned_items:
        st.session_state.scanned_items[key] = False
    st.rerun()