import streamlit as st
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Contact Owner", layout="centered")

# --- DYNAMIC OWNER LOGIC ---
# This tries to get the email from the QR code link first (?owner=...)
query_params = st.query_params
url_email = query_params.get("owner", "hanshhilar705@gmail.com")

st.title("📬 Message the Owner")

with st.form("contact_form", clear_on_submit=True):
    # NEW: Manual Owner Email Input
    st.info("Verify or enter the owner's email address below.")
    owner_to_contact = st.text_input("Owner's Email Address *", value=url_email)
    
    st.divider()
    
    # Finder's Details
    finder_name = st.text_input("Your Name *")
    finder_phone = st.text_input("Your Phone Number *")
    message_body = st.text_area("Message (e.g., 'I found your bag near the canteen')")
    
    submit = st.form_submit_button("Send Alert")

    if submit:
        if not finder_name or not finder_phone or not owner_to_contact:
            st.error("Please fill in all required fields (*).")
        elif "@" not in owner_to_contact:
            st.error("Please enter a valid email address.")
        else:
            try:
                # Backend Email Logic
                msg = EmailMessage()
                msg.set_content(f"Item Found Alert!\n\n"
                                f"Finder Name: {finder_name}\n"
                                f"Finder Phone: {finder_phone}\n"
                                f"Message: {message_body}")
                
                msg['Subject'] = "🚨 QR Connect: Someone found your item!"
                msg['To'] = owner_to_contact  # Sends to whatever is in the box
                msg['From'] = "hanshhilar705@gmail.com" # Your system email

                # SMTP Login
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                # Ensure you have your 16-character App Password in Secrets or here
                server.login("hanshhilar705@gmail.com", st.secrets["ituf bmzk xjba etlz"]) 
                
                server.send_message(msg)
                server.quit()

                st.success(f"✅ Success! An alert has been sent to {owner_to_contact}.")
                st.balloons()
            except Exception as e:
                st.error("Service error. Please verify the App Password settings.")