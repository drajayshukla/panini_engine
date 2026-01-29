#pages/06_Vichhed_Lab.py
import streamlit as st
from utils.sanskrit_utils import sanskrit_varna_vichhed, sanskrit_varna_samyoga

st.set_page_config(page_title="Varna Vichhed Lab", layout="wide")

st.title("🔬 वर्ण विच्छेद परीक्षण शाला (Lab)")
st.markdown("---")

st.info("यह लैब आपके १६-नियमों वाले 'Surgical' विच्छेद लॉजिक का स्वतंत्र परीक्षण करने के लिए है।")

# मुख्य इनपुट
input_text = st.text_input("परीक्षण के लिए शब्द लिखें (उदा: एधँ, स्पर्धँ, दधँ):", value="दधँ")

if input_text:
    # विच्छेद प्रक्रिया
    varna_list = sanskrit_varna_vichhed(input_text)

    # परिणाम प्रदर्शन
    st.subheader("📊 विच्छेद परिणाम (Surgical Dissection)")

    # वर्णों को कार्ड्स के रूप में दिखाना
    cols = st.columns(len(varna_list) if varna_list else 1)
    for idx, varna in enumerate(varna_list):
        with cols[idx]:
            st.code(f"{varna}", language="text")
            st.caption(f"Pos: {idx}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**विस्तृत वर्ण सूची (Raw List):**")
        st.success(varna_list)

    with col2:
        st.write("**पुनः संयोग (Reconstruction):**")
        reconstructed = sanskrit_varna_samyoga(varna_list)
        st.info(reconstructed)

    # विशेष टिप्पणियाँ
    if 'ँ' in varna_list:
        st.warning("⚠️ **Observation:** अनुनासिक (ँ) को स्वतंत्र वर्ण के रूप में पहचाना गया है।")