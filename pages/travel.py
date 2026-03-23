import streamlit as st
import streamlit.components.v1 as components
import qrcode
from io import BytesIO
import time

st.set_page_config(page_title="Smart Travel Manager", layout="centered")

# 1. PERSISTENT STATE
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = {
        "Passport": False,
        "Laptop": False,
        "Charger": False
    }

# 2. QR SCANNER LOGIC (URL AND JAVASCRIPT)
# This handles both: Physical phone scans AND the on-screen camera scanner
query_params = st.query_params
check_item = query_params.get("check")

if check_item:
    item_to_tick = check_item.strip().capitalize()
    if item_to_tick in st.session_state.scanned_items:
        if not st.session_state.scanned_items[item_to_tick]:
            st.session_state.scanned_items[item_to_tick] = True
            st.success(f"✅ {item_to_tick} verified!")
            time.sleep(0.5)
            st.query_params.clear()
            st.rerun()

# 3. THE ACTUAL LIVE SCANNER (JavaScript)
st.subheader("📷 Live QR Scanner")
st.write("Point your camera at an item's QR code to tick it off.")

# This HTML/JS block opens the camera and "clicks" the link for you
scanner_code = """
<script src="https://unpkg.com/html5-qrcode"></script>
<div id="reader" style="width:100%; border-radius:10px;"></div>
<script>
    function onScanSuccess(decodedText, decodedResult) {
        // If the QR contains a URL, we redirect the parent window to that URL
        if (decodedText.includes('?check=')) {
            window.parent.location.href = decodedText;
        }
    }
    let html5QrcodeScanner = new Html5QrcodeScanner(
        "reader", { fps: 10, qrbox: 250 });
    html5QrcodeScanner.render(onScanSuccess);
</script>
"""
components.html(scanner_code, height=450)

# 4. UI: PACKING PROGRESS
st.divider()
packed_count = sum(st.session_state.scanned_items.values())
total_count = len(st.session_state.scanned_items)
st.progress(packed_count / total_count if total_count > 0 else 0)

# Checklist Display
cols = st.columns(2)
for i, (item, is_packed) in enumerate(st.session_state.scanned_items.items()):
    with cols[i % 2]:
        status = "✅" if is_packed else "❌"
        st.write(f"{status} **{item}**")

if st.button("Reset All Ticks"):
    for key in st.session_state.scanned_items:
        st.session_state.scanned_items[key] = False
    st.rerun()

# 5. GENERATOR (So you can test it right now)
st.divider()
st.subheader("➕ Create New Item Tag")
new_item = st.text_input("Item Name:")
if st.button("Generate Packing QR"):
    if new_item:
        clean_name = new_item.strip().capitalize()
        if clean_name not in st.session_state.scanned_items:
            st.session_state.scanned_items[clean_name] = False
        
        # USE YOUR ACTUAL APP URL HERE
        base_url = "https://blank-app-x4koreu3hsq.streamlit.app/travel" 
        final_link = f"{base_url}?check={clean_name}"
        
        qr = qrcode.make(final_link)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=200)
        st.download_button("Download Tag", buf.getvalue(), f"{clean_name}.png")
        st.rerun()