import streamlit as st
import time

st.set_page_config(page_title="Travel Checklist", layout="centered")

# Using standard headers instead of custom CSS to avoid the TypeError
st.title("🧳 Smart Travel Checklist")
st.write("Ensuring you have everything before your journey starts.")

# 1. Initialize the checklist
if 'scanned_items' not in st.session_state:
    # You can add more items here manually
    st.session_state.scanned_items = {
        "Passport": False,
        "Laptop": False,
        "Charger": False,
        "Wallet": False
    }

# 2. Simulation of scanning
st.subheader("📷 Scan Your Items")
scan_input = st.text_input("Simulate QR Scan (Type item name):", placeholder="e.g. Laptop")

if scan_input:
    matched = False
    # Normalize the input to check against our list
    clean_input = scan_input.strip().capitalize()
    
    if clean_input in st.session_state.scanned_items:
        st.session_state.scanned_items[clean_input] = True
        st.success(f"✅ {clean_input} verified!")
        matched = True
        time.sleep(1)
        st.rerun()
    
    if not matched and scan_input != "":
        st.error(f"⚠️ Warning: '{scan_input}' is not on your travel list!")

# 3. Visual Checklist
st.divider()
st.subheader("Packing Progress")

# This calculates how many items are done
packed_count = sum(st.session_state.scanned_items.values())
total_count = len(st.session_state.scanned_items)

# Display a progress bar (Looks great for a project!)
st.progress(packed_count / total_count)

# Display each item with a status
for item, is_packed in st.session_state.scanned_items.items():
    if is_packed:
        st.write(f"🟢 **{item}** — Packed")
    else:
        st.write(f"⚪ {item} — *Missing*")

# 4. Final Validation
if packed_count == total_count:
    st.balloons()
    st.success("🎉 All items verified. Safe travels!")
else:
    remaining = total_count - packed_count
    st.warning(f"🚨 You still have {remaining} item(s) to scan before leaving.")

if st.button("Reset Checklist"):
    for key in st.session_state.scanned_items:
        st.session_state.scanned_items[key] = False
    st.rerun()