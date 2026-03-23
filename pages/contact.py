import streamlit as st
import smtplib
from email.message import EmailMessage
import imghdr # To identify the image type

st.set_page_config(page_title="Contact Owner", page_icon="📸", layout="centered")

query_params = st.query_params
url_email = query_params.get("owner", "hanshhilar705@gmail.com")

st.title("📸 QR Connect: Photo Alert")

with st.form("pro_contact_form", clear_on_submit=True):
    st.subheader("1. Contact Info")
    target_email = st.text_input("Send Alert To:", value=url_email)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name *")
    with col2:
        phone = st.text_input("Your Phone Number *")
        
    st.divider()
    st.subheader("2. Item Details")
    
    # NEW: Image Upload Field
    uploaded_file = st.file_uploader("Upload a photo of the item", type=["jpg", "png", "jpeg"])
    
    details = st.text_area("Message for the owner", placeholder="Describe the location...")

    submit = st.form_submit_button("🚀 Send Photo & Alert")

    if submit:
        if not name or not phone or not target_email:
            st.error("Please fill in the required name and contact info.")
        else:
            try:
                # Setup the Email
                msg = EmailMessage()
                msg['Subject'] = f"🚨 ITEM FOUND: Photo attached from {name}"
                msg['To'] = target_email
                msg['From'] = "hanshhilar705@gmail.com"
                
                body = f"🌟 Great news! {name} has found your item.\n\n"
                body += f"Finder Phone: {phone}\n"
                body += f"Message: {details}\n\n"
                body += "Check the attachment for the photo!"
                msg.set_content(body)

                # ATTACH THE IMAGE
                if uploaded_file is not None:
                    file_data = uploaded_file.read()
                    file_type = imghdr.what(None, h=file_data)
                    file_name = uploaded_file.name
                    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

                # Send via Gmail SMTP
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("hanshhilar705@gmail.com", st.secrets["EMAIL_PASSWORD"]) 
                server.send_message(msg)
                server.quit()

                st.success(f"✅ Success! Photo and message sent to {target_email}.")
                st.balloons()
                st.snow()
            except Exception as e:
                st.error("Error: Make sure your 'EMAIL_PASSWORD' is set in Streamlit Secrets.")