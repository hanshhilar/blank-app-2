import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="QR Connect Manager", page_icon="🔗")

st.title("🔗 QR Connect: Tag Generator")
st.write("Create a QR tag that lets finders email the owner instantly.")

# User Input Section
col1, col2 = st.columns(2)

with col1:
    owner_name = st.text_input("Owner Name:", "Hansh Hilar")
    owner_email = st.text_input("Owner Email:", "hanshhilar705@gmail.com")

with col2:
    item_name = st.text_input("Item Name (Optional):", "Laptop Bag")
    subject = f"Found Item: {item_name}"

# QR Type Selection
st.divider()
st.subheader("Choose QR Type")
qr_type = st.radio(
    "How should the finder contact you?",
    ["Direct Email (Opens Mail App)", "Save Contact (vCard)"]
)

if st.button("Generate QR Code"):
    # Create the data for the QR
    if qr_type == "Direct Email (Opens Mail App)":
        # mailto format: mailto:email@example.com?subject=SubjectText
        data = f"mailto:{owner_email}?subject={subject.replace(' ', '%20')}"
    else:
        # vCard format for saving to contacts
        data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{owner_name}\nEMAIL:{owner_email}\nNOTE:Owner of {item_name}\nEND:VCARD"

    # Generate the Image
    qr_img = qrcode.make(data)
    
    # Process for Streamlit display
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Display Result
    st.image(byte_im, width=250, caption=f"Scan to contact {owner_name}")
    st.download_button(
        label="Download QR for Printing",
        data=byte_im,
        file_name=f"{owner_name}_tag.png",
        mime="image/png"
    )
    st.success("✅ QR Generated! Print this and attach it to your belongings.")