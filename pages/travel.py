import streamlit as st
import qrcode
from io import BytesIO
import time

st.set_page_config(page_title="Smart Travel Manager", layout="centered")

st.title("🧳 Smart Travel Manager")

# 1. Initialize the checklist in Session State so it stays during refreshes
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = {
        "Passport": False,
        "Laptop": False,
        "Charger": False
    }

# 2. THE SCANNER LOGIC (Reads the URL: .../travel?check=ItemName)
query_params = st.query_params
check_item = query_params.get("check")

if check_item:
    item_to_tick = check_item.strip().capitalize()
    if item_to_tick in st.session_state.scanned_items:
        if not st.session_state.scanned_items[item_to_tick]:
            st.session_state.scanned_items[item_to_tick] = True
            st.success(f"✅ {item_to_tick} verified via QR!")
            time.sleep(1)
            # Clear the URL parameter so it doesn't keep "scanning" on refresh
            st.query_params.clear()
            st.rerun()

# 3. Visual Checklist & Progress
st.subheader("Packing Progress")
packed_count = sum(st.session_state.scanned_items.values())
total_count = len(st.session_state.scanned_items)
st.progress(packed_count / total_count if total_count > 0 else 0)

col1, col2 = st.columns([2, 1])
with col1:
    for item, is_packed in st.session_state.scanned_items.items():
        status = "✅" if is_packed else "❌"
        st.write(f"{status} **{item}**")

with col2:
    if st.button("Reset All Ticks"):
        for key in st.session_state.scanned_items:
            st.session_state.scanned_items[key] = False
        st.rerun()

# 4. QR CODE GENERATOR SECTION
st.divider()
st.subheader("➕ Create New Item Tag")
st.write("Type an item name to add it to your list and generate its unique QR tag.")

new_item = st.text_input("Item Name (e.g., Camera, Umbrella):")

if st.button("Generate Packing QR"):
    if new_item:
        clean_name = new_item.strip().capitalize()
        
        # Add to checklist if it's a new item
        if clean_name not in st.session_state.scanned_items:
            st.session_state.scanned_items[clean_name] = False
        
        # USE YOUR ACTUAL APP URL HERE
        base_url = "https://blank-app-x4koreu3hsq.streamlit.app/travel" 
        final_qr_link = f"{base_url}?check={clean_name}"
        
        # Generate QR Image
        qr = qrcode.make(final_qr_link)
        buf = BytesIO()
        qr.save(buf, format="PNG")