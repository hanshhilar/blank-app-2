import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
from io import BytesIO

st.set_page_config(page_title="Smart Travel Manager", layout="centered")

st.title("🧳 Smart Travel Manager")

# 1. State Management
if 'scanned_items' not in st.session_state:
    st.session_state.scanned_items = {
        "Passport": False, 
        "Laptop": False, 
        "Charger": False
    }

# 2. THE SCANNER
st.subheader("📷 Scan Item Tag")
img_file = st.camera_input("Take a photo of the QR code")

if img_file:
    try:
        # Load image with Pillow
        img = Image.open(img_file)
        
        # Decode QR using pyzbar
        decoded_list = decode(img)
        
        if not decoded_list:
            st.warning("No QR code detected. Try holding it steady and make sure there's enough light!")
        else:
            for obj in decoded_list:
                data = obj.data.decode("utf-8")
                if "?check=" in data:
                    item_name = data.split("?check=")[-1].strip().capitalize()
                    
                    if item_name in st.session_state.scanned_items:
                        st.session_state.scanned_items[item_name] = True
                        st.success(f"✅ {item_name} Scanned!")
                        st.balloons()
                    else:
                        st.error(f"'{item_name}' isn't on your list.")
    except ImportError:
        st.error("The scanner library is having trouble on this server. Please use the URL links for the demo!")
    except Exception as e:
        st.error(f"Error: {e}")

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
    # Replace with your actual app URL
    link = f"https://blank-app-x4koreu3hsq.streamlit.app/travel?check={new_item}"
    qr_img = qrcode.make(link)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), width=150)
    st.caption(f"Scan this to tick: {new_item}")