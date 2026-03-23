import streamlit as st
from qreader import QReader
from PIL import Image
import qrcode
from io import BytesIO

st.set_page_config(page_title="Smart Travel Manager", layout="centered")

st.title("🧳 Smart Travel Manager")

# 1. State Management
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = {"Passport": False, "Laptop": False, "Charger": False}

# Initialize the QR Reader (This is now our main tool)
@st.cache_resource
def get_reader():
    return QReader()

qreader = get_reader()

# 2. THE SCANNER
st.subheader("📷 Scan Item Tag")
img_file = st.camera_input("Take a photo of the QR code")

if img_file:
    # Convert image for processing using Pillow
    pil_image = Image.open(img_file)
    
    # Detect and decode QR (QReader can handle PIL images directly)
    decoded_data = qreader.detect_and_decode(image=pil_image)
    
    if not decoded_data or decoded_data[0] is None:
        st.warning("No QR code found. Make sure it's centered and in focus!")
    else:
        for data in decoded_data:
            if data and "?check=" in data:
                # Extract item name from the URL
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

# 4. QR GENERATOR
st.divider()
st.subheader("➕ Tag Generator")
new_item = st.text_input("New Item Name:")
if st.button("Generate QR"):
    # This generates the link that the scanner looks for
    link = f"https://blank-app-x4koreu3hsq.streamlit.app/travel?check={new_item}"
    qr_img = qrcode.make(link)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), width=150)
    st.caption(f"Scan this to tick: {new_item}")