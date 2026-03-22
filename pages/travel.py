import streamlit as st
import qrcode
from io import BytesIO
import time

st.set_page_config(page_title="Travel Checklist & QR Gen", layout="centered")

st.title("🧳 Smart Travel Manager")

# 1. Initialize the checklist
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
            st.success(f"✅ {item_to_tick} Verified!")
            time.sleep(1)
            st.query_params.clear()
            st.rerun()

# 3. Visual Checklist & Progress
packed_count = sum(st.session_state.scanned_items.values())
total_count = len(st.session_state.scanned_items)
st.progress(packed_count / total_count if total_count > 0 else 0)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Checklist")
    for item, is_packed in st.session_state.scanned_items.items():
        status = "✅" if is_packed else "❌"
        st.write(f"{status} **{item}**")

with col2:
    if st.button("Reset All Ticks"):
        for key in st.session_state.scanned_items:
            st.session_state.scanned_items[key] = False
        st.rerun()

# --- 4. NEW: QR CODE GENERATOR SECTION ---
st.divider()
st.subheader("➕ Create New Item Tag")
new_item = st.text_input("Item Name (e.g., Camera):")

if st.button("Generate Packing QR"):
    if new_item:
        # Add to checklist if not already there
        clean_name = new_item.strip().capitalize()
        if clean_name not in st.session_state.scanned_items:
            st.session_state.scanned_items[clean_name] = False
        
        # CREATE THE DYNAMIC URL
        # Replace 'your-app-url' with your actual Streamlit link!
        base_url = "https://blank-app-2.streamlit.app/travel" 
        final_qr_link = f"{base_url}?check={clean_name}"
        
        # Generate QR Image
        qr = qrcode.make(final_qr_link)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        
        st.image(buf.getvalue(), width=200)
        st.write(f"**Link:** `{final_qr_link}`")
        st.download_button("Download Tag", buf.getvalue(), f"{clean_name}_tag.png")
        st.rerun()
    else:
        st.warning("Please enter an item name first.")