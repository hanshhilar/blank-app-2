import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="QR Tag Factory", page_icon="🎨")

st.title("🎨 QR Tag Factory")
st.write("Create custom QR codes for your project belongings.")

# --- INPUT SECTION ---
with st.container(border=True):
    st.subheader("1. Configure your QR")
    qr_label = st.text_input("Label for this QR (e.g., 'My Backpack'):", "My Item")
    qr_link = st.text_input("Paste the URL here:", "https://")
    
    col1, col2 = st.columns(2)
    with col1:
        fill_color = st.color_picker("Pick QR Color:", "#002060") # Default Navy
    with col2:
        back_color = st.color_picker("Pick Background:", "#FFFFFF") # White

# --- GENERATION LOGIC ---
if st.button("✨ Generate Professional QR", use_container_width=True):
    if qr_link == "https://" or not qr_link:
        st.warning("Please enter a valid URL first!")
    else:
        try:
            # Create the QR Object
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(qr_link)
            qr.make(fit=True)

            # Create the Image
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            # Save to buffer
            buf = BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # Display Result
            st.divider()
            st.success(f"Generated QR for: {qr_label}")
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(byte_im, width=250)
            with c2:
                st.info(f"**Target URL:**\n{qr_link}")
                st.download_button(
                    label="💾 Download PNG Image",
                    data=byte_im,
                    file_name=f"{qr_label.replace(' ', '_')}_qr.png",
                    mime="image/png",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error generating QR: {e}")

st.divider()
st.caption("Tip: Use the Travel page URL with '?check=ItemName' to create auto-ticking tags!")