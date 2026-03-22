import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="QR Connect Manager", page_icon="🔗")

st.title("🔗 QR Connect: System Validator")
st.write("Generate a QR code to demonstrate the system to your faculty.")

# 1. Base URL of your Wix "Found Item" Page
# Replace this with your actual Wix page link
wix_found_page = "https://hanshhilar705.wixsite.com/qrconect/found-item"

# 2. Input Section
st.subheader("Recipient Details")
test_mode = st.toggle("Enable Teacher Test Mode")

if test_mode:
    # Put your teacher's email here
    recipient_email = st.text_input("Teacher's Email:", "teacher_email@vimaljyothi.ac.in")
    st.info("💡 This QR will send the 'Found' alert directly to your teacher.")
else:
    recipient_email = st.text_input("Owner Email:", "hanshhilar705@gmail.com")

if st.button("Generate Validation QR"):
    # The Magic: Attaching the email to the URL
    validation_link = f"{wix_found_page}?mail={recipient_email}"
    
    # Create the QR
    qr_img = qrcode.make(validation_link)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    
    st.image(buf.getvalue(), caption=f"Validation Link: {validation_link}")
    
    st.download_button(
        label="Download QR for Faculty",
        data=buf.getvalue(),
        file_name="teacher_test_qr.png",
        mime="image/png"
    )
    st.success(f"Done! When scanned, this QR will tell Wix to email {recipient_email}")