import streamlit as st
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Contact Owner", layout="centered")

st.title("📬 Message the Owner")
st.write("Fill out this form to notify the owner that you have found their item.")

# The Form
with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Your Name *")
    phone = st.text_input("Your Phone Number *")
    details = st.text_area("Where did you find the item?")
    
    submit = st.form_submit_button("Send Alert to Owner")

    if submit:
        if not name or not phone:
            st.error("Please fill in your name and phone number.")
        else:
            try:
                msg = EmailMessage()
                msg.set_content(f"Item Found!\n\nName: {name}\nPhone: {phone}\nLocation: {details}")
                msg['Subject'] = "🚨 QR Connect: Someone found your item!"
                msg['To'] = "hanshhilar705@gmail.com"
                msg['From'] = "hanshhilar705@gmail.com"

                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                # Use your 16-character App Password here
                server.login("hanshhilar705@gmail.com", "ituf bmzk xjba etlz") 
                server.send_message(msg)
                server.quit()

                st.success("✅ Message sent! The owner has been notified.")
                st.balloons()
            except Exception as e:
                st.error("Service error. Please check the App Password.")