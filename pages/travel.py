import streamlit as st
import cv2
import numpy as np
from qreader import QReader
from PIL import Image
import qrcode
from io import BytesIO

st.set_page_config(page_title="Smart Travel Manager", layout="centered")

st.title("🧳 Smart Travel Manager")

# 1. State Management
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = {"Passport": False, "Laptop": False, "Charger": False}

# Initialize the QR Reader
qreader = QReader()

# 2. THE SCANNER
st.subheader("📷 Scan Item Tag")
img_file = st.camera_input("Take a photo of the QR code")

if img_file:
    # Convert image for processing
    pil_image = Image.open(img_file)
    image_array = np.array(pil_image)
    
    # Detect and decode QR
    # QReader returns a list of decoded strings
    decoded_data = qreader.detect_and_decode(image=image_array)
    
    if not decoded_data or decoded_data[0] is None:
        st.warning("No QR code found. Try holding it steady and make sure it's in focus!")
    else:
        for data in decoded_data:
            if data and "?check=" in data:
                item_name = data.split("?check=")[-1].strip().capitalize()
                
                if item_name in st.session_state.scanned_items:
                    st.session_state.scanned_items[item_name] = True
                    st.success(f"✅ {item_name} Scanned!")
                    st.balloons()
                else:
                    st.error(f"'{item_name}' isn't on your list.")

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

# 4. QR GENERATOR (Updated with your URL)
st.divider()
st.subheader("➕ Tag Generator")
new_item = st.text_input("New Item Name:")
if st.button("Generate QR"):
    # Change the URL below to match your actual app link
    link = f"https://blank-app-x4koreu3hsq.streamlit.app/travel?check={new_item}"
    qr_img = qrcode.make(link)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), width=150)
    st.caption(f"Scan this to tick: {new_item}")