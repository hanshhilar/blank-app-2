import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from io import BytesIO

st.set_page_config(page_title="Smart Travel Manager", layout="centered")

st.title("🧳 Smart Travel Manager")

# 1. State Management (Keeps the ticks saved)
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = {"Passport": False, "Laptop": False, "Charger": False}

# 2. THE PYTHON SCANNER
st.subheader("📷 Scan Item Tag")
img_file = st.camera_input("Take a photo of the QR code to tick the item")

if img_file:
    # Convert the uploaded file to an OpenCV image
    pil_image = Image.open(img_file)
    opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    # Decode the QR code
    detected_barcodes = decode(opencv_image)
    
    if not detected_barcodes:
        st.warning("No QR code detected. Try holding it closer or getting better light!")
    else:
        for barcode in detected_barcodes:
            data = barcode.data.decode('utf-8')
            # Look for our special '?check=' trigger in the URL
            if "?check=" in data:
                item_name = data.split("?check=")[-1].strip().capitalize()
                
                if item_name in st.session_state.scanned_items:
                    st.session_state.scanned_items[item_name] = True
                    st.success(f"✅ {item_name} Scanned Successfully!")
                    st.balloons()
                else:
                    st.error(f"Item '{item_name}' is not in your checklist.")

# 3. CHECKLIST UI
st.divider()
packed = sum(st.session_state.scanned_items.values())
total = len(st.session_state.scanned_items)
st.progress(packed / total if total > 0 else 0)

cols = st.columns(3)
for i, (item, status) in enumerate(st.session_state.scanned_items.items()):
    with cols[i % 3]:
        st.write(f"{'✅' if status else '❌'} {item}")

if st.button("Reset All"):
    for k in st.session_state.scanned_items: st.session_state.scanned_items[k] = False
    st.rerun()

# 4. QR GENERATOR
st.divider()
st.subheader("➕ Tag Generator")
new_item = st.text_input("New Item Name:")
if st.button("Generate QR"):
    # Ensure this URL matches your actual app URL!
    link = f"https://blank-app-x4koreu3hsq.streamlit.app/travel?check={new_item}"
    qr_img = qrcode.make(link)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), width=150)
    st.caption(f"Scan this to tick: {new_item}")