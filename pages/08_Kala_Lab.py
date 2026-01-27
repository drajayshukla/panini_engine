import streamlit as st
from core.phonology import sanskrit_varna_vichhed
from logic.kala_rules import apply_ukalo_aj_1_2_27

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Kala-Sanjna Lab", layout="wide", page_icon="⏳")

# --- २. शास्त्रीय उदाहरणों का संग्रह ---
examples = {
    "ह्रस्व (१ मात्रा)": "दधि",
    "दीर्घ (२ मात्रा)": "कुमारी",
    "प्लुत (३ मात्रा)": "देवदत्त३"
}

st.title("⏳ स्वर-काल विश्लेषण प्रयोगशाला (SK6 Lab)")

# --- ३. उदाहरण सेलेक्टर ---
st.markdown("### 📚 शास्त्रीय उदाहरण (Classical Examples)")
cols_ex = st.columns(3)
selected_example = ""

if cols_ex[0].button("ह्रस्व: दधि / मधु"):
    selected_example = "दधि"
if cols_ex[1].button("दीर्घ: कुमारी / गौरी"):
    selected_example = "कुमारी"
if cols_ex[2].button("प्लुत: देवदत्त३"):
    selected_example = "देवदत्त३"

# --- ४. यूजर इनपुट ---
input_text = st.text_input("यहाँ शब्द लिखें या ऊपर से चुनें:", value=selected_example if selected_example else "दधि")

if input_text:
    varna_objects = sanskrit_varna_vichhed(input_text)
    processed_varnas = [apply_ukalo_aj_1_2_27(v) for v in varna_objects]

    # --- ५. विज़ुअल आउटपुट (Cards) ---
    st.subheader(f"🔍 विश्लेषण: {input_text}")
    cols = st.columns(len(processed_varnas))

    for i, v in enumerate(processed_varnas):
        with cols[i]:
            # कलर कोडिंग: ह्रस्व-हरा, दीर्घ-नीला, प्लुत-नारंगी
            bg_color = "#E8F5E9" if v.matra == 1 else "#E3F2FD" if v.matra == 2 else "#FFF3E0" if v.matra == 3 else "#F5F5F5"
            text_color = "#2E7D32" if v.matra == 1 else "#1565C0" if v.matra == 2 else "#E65100" if v.matra == 3 else "#616161"

            st.markdown(f"""
                <div style="background-color:{bg_color}; border:2px solid {text_color}; border-radius:10px; padding:15px; text-align:center;">
                    <h1 style="margin:0; color:black;">{v.char}</h1>
                    <b style="color:{text_color}; font-size:1.1rem;">{v.kala_sanjna}</b>
                    <p style="margin:0; font-size:0.9rem;">{v.matra} मात्रा</p>
                </div>
            """, unsafe_allow_html=True)

    # --- ६. डायग्नोस्टिक रिपोर्ट (The Audit Log) ---
    st.divider()
    col_rep1, col_rep2 = st.columns(2)

    with col_rep1:
        st.subheader("📋 पाणिनीय ऑडिट रिपोर्ट")
        for v in processed_varnas:
            if v.is_vowel:
                if v.char in ['ए', 'ओ', 'ऐ', 'औ']:
                    st.info(f"🔹 **{v.char}**: नियम ३ (ह्रस्वाभाव) - यह सदैव दीर्घ/प्लुत होता है।")
                elif 'ऌ' in v.char:
                    st.info(f"🔸 **{v.char}**: नियम २ (दीर्घाभाव) - इसका दीर्घ रूप नहीं होता।")
                else:
                    st.success(f"✅ **{v.char}**: नियम १ - ह्रस्व, दीर्घ, प्लुत तीनों संभव हैं।")

    with col_rep2:
        st.subheader("📖 सूत्र संदर्भ (Context)")
        if "३" in input_text:
            st.warning(
                "👉 **देवदत्त३ अत्र न्वसि**: यहाँ 'त' का 'अ' प्लुत है क्योंकि संबोधन में दूर से बुलाने पर 'दूराद्धूते च' (8.2.84) से प्लुत होता है।")
        elif input_text in ["दधि", "मधु"]:
            st.success("👉 **दधि/मधु**: यहाँ 'इ' और 'उ' ह्रस्व हैं (१ मात्रा)।")
        elif input_text in ["कुमारी", "गौरी"]:
            st.success("👉 **कुमारी/गौरी**: यहाँ 'ई' दीर्घ है (२ मात्रा)।")

# --- ७. विज़ुअल चार्ट ---
st.divider()