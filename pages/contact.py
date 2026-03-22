import streamlit as st
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Contact Owner", layout="centered")

# --- DYNAMIC OWNER LOGIC ---
# This reads the "?owner=..." part of the URL
query_params = st.query_params
target_email = query_params.get("owner", "hanshhilar705@gmail.com") # Default to yours if empty

st.title("📬 Message the Owner")
st.info(f"Sending message to: **{target_email}**")

with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Your Name *")
    phone = st.text_input("Your Phone Number *")
    details = st.text_area("Message for the owner")
    
    submit = st.form_submit_button("Send Alert")

    if submit:
        if not name or not phone:
            st.error("Please fill in required fields.")
        else:
            try:
                msg = EmailMessage()
                msg.set_content(f"Item Found!\n\nFinder: {name}\nPhone: {phone}\nNote: {details}")
                msg['Subject'] = "🚨 QR Connect: Your item was found!"
                msg['To'] = target_email  # Dynamic recipient!
                msg['From'] = "hanshhilar705@gmail.com" # Your system email

                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                # Use your 16-character App Password here
                server.login("hanshhilar705@gmail.com", "your_app_password") 
                server.send_message(msg)
                server.quit()

                st.success(f"✅ Success! An alert has been sent to {target_email}.")
                st.balloons()
            except Exception as e:
                st.error("Email service error. Check App Password.")