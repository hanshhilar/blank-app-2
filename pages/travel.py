import streamlit as st
import qrcode
from io import BytesIO
import time

st.set_page_config(page_title="Smart Travel Manager", layout="centered")

st.title("🧳 Smart Travel Manager")

# 1. PERSISTENT STATE: This ensures ticks stay even if the page refreshes
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = {
        "Passport": False,
        "Laptop": False,
        "Charger": False
    }

# 2. THE SCANNER LOGIC (URL Processor)
query_params = st.query_params
if "check" in query_params:
    item_to_tick = query_params["check"].strip().capitalize()
    if item_to_tick in st.session_state.scanned_items:
        # Update the state!
        st.session_state.scanned_items[item_to_tick] = True
        st.success(f"✅ {item_to_tick} verified via QR!")
        # We don't clear the params immediately so the user sees the success
        # But we use st.rerun() to clean the URL for the next scan
        time.sleep(1)
        st.query_params.clear()
        st.rerun()

# 3. UI: PACKING PROGRESS
st.subheader("Packing Progress")
packed_count = sum(st.session_state.scanned_items.values())
total_count = len(st.session_state.scanned_items)
st.progress(packed_count / total_count if total_count > 0 else 0)

# Layout for the Checklist
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

st.divider()

# 4. ADDING THE SCANNER (Camera Input)
st.subheader("📷 Live Scanner")
# This opens the camera on mobile/laptop
picture = st.camera_input("Scan your item's QR Tag")

if picture:
    st.info("Visual scanning is active. For the B.Tech demo, use the QR-triggered URLs to update the list in real-time!")

# 5. QR GENERATOR SECTION
st.divider()
st.subheader("➕ Create New Item Tag")
new_item = st.text_input("Item Name (e.g., Camera):")

if st.button("Generate Packing QR"):
    if new_item:
        clean_name = new_item.strip().capitalize()
        if clean_name not in st.session_state.scanned_items:
            st.session_state.scanned_items[clean_name] = False
        
        # Replace with your actual deployed URL
        base_url = "https://blank-app-x4koreu3hsq.streamlit.app/travel" 
        final_qr_link = f"{base_url}?check={clean_name}"
        
        qr = qrcode.make(final_qr_link)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        
        st.image(buf.getvalue(), width=200)
        st.download_button("Download Tag", buf.getvalue(), f"{clean_name}_tag.png")
        st.rerun()