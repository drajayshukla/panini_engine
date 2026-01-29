#pages/08_Kala_Lab.py
import streamlit as st
import pandas as pd
from core.phonology import sanskrit_varna_vichhed
from logic.kala_rules import apply_ukalo_aj_1_2_27, generate_18_bheda_matrix

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Kala-Sanjna Lab", layout="wide", page_icon="⏳")

# --- २. शास्त्रीय उदाहरण ---
examples = {
    "ह्रस्व": "दधि",
    "दीर्घ": "कुमारी",
    "प्लुत": "देवदत्त३",
    "अनुदात्त": "अ॒ग्निम्",
    "स्वरित": "क्वा॑",
    "अनुनासिक": "आँ"
}

st.title("⏳ स्वर-काल एवं सवर विश्लेषण (SK6-SK10)")
st.caption("नियम: अचश्च (१.२.२८) - काल, स्वर और अनुनासिकता का कार्य केवल अच् पर ही होता है।")

# --- ३. उदाहरण सेलेक्टर ---
st.markdown("### 📚 शास्त्रीय उदाहरण")
cols_ex = st.columns(6)
selected_example = ""

for i, (lab, val) in enumerate(examples.items()):
    if cols_ex[i].button(f"{lab}: {val}"):
        selected_example = val

# --- ४. यूजर इनपुट ---
input_text = st.text_input("यहाँ वैदिक या लौकिक शब्द लिखें:",
                           value=selected_example if selected_example else "अ॒ग्निम्")

if input_text:
    varna_objects = sanskrit_varna_vichhed(input_text)
    # काल संज्ञा नियम लागू करें
    processed_varnas = [apply_ukalo_aj_1_2_27(v) for v in varna_objects]

    st.subheader(f"🔍 विश्लेषण: {input_text}")
    cols = st.columns(len(processed_varnas))

    for i, v in enumerate(processed_varnas):
        with cols[i]:
            # अचश्च (1.2.28) के आधार पर डिजाइन
            is_vowel = v.is_vowel
            bg_color = "#FFFFFF" if not is_vowel else "#E8F5E9" if v.matra == 1 else "#E3F2FD" if v.matra == 2 else "#FFF3E0"
            border_color = "#CFD8DC" if not is_vowel else "#2E7D32" if v.matra == 1 else "#1565C0"

            # स्वर और अनुनासिकता जानकारी
            svara_info = f"<br><span style='color:red; font-size:0.8rem;'>{v.svara} {v.svara_mark if v.svara_mark else ''}</span>" if is_vowel else ""
            nasal_info = f"<br><span style='color:blue; font-size:0.7rem;'>{'अनुनासिक' if v.is_anunasika else 'निरनुनासिक'}</span>" if is_vowel else ""

            st.markdown(f"""
                <div style="background-color:{bg_color}; border:2px solid {border_color}; border-radius:10px; padding:10px; text-align:center; min-height:180px;">
                    <h1 style="margin:0; color:black;">{v.char}</h1>
                    <hr style="margin:5px 0; border:0.5px solid #eee;">
                    <b style="font-size:0.9rem;">{v.kala_sanjna if is_vowel else 'व्यञ्जन'}</b>
                    <p style="margin:0; font-size:0.8rem;">{v.matra} मात्रा</p>
                    {svara_info}
                    {nasal_info}
                </div>
            """, unsafe_allow_html=True)

    # --- ५. ऑडिट रिपोर्ट एवं शास्त्रीय विश्लेषण ---
    st.divider()
    col_rep1, col_rep2 = st.columns(2)

    with col_rep1:
        st.subheader("🛡️ परिभाषा १.२.२८ (अचश्च) रिपोर्ट")
        for v in processed_varnas:
            if not v.is_vowel:
                st.warning(f"🚫 **{v.char}**: व्यञ्जन (हल्) पर काल/स्वर संज्ञाएँ लागू नहीं होतीं।")
            else:
                st.success(f"✅ **{v.char}**: अच् पर संज्ञाएँ सफलतापूर्वक लागू की गईं।")

    with col_rep2:
        st.subheader("📖 शास्त्रीय विश्लेषण")
        if "ँ" in input_text:
            st.info(
                "**मुखनासिकावचनोऽनुनासिकः (१.१.८)**: मुख और नासिका दोनों से उच्चारित होने के कारण यह 'अनुनासिक' है।")
        if any(m in input_text for m in ["॒", "_"]):
            st.info("**नीचैरनुदात्तः (१.२.३०)**: वर्ण के अधोभाग से निष्पन्न होने के कारण 'अनुदात्त' है।")
        if any(m in input_text for m in ["॑", "'"]):
            st.info("**समाहारः स्वरितः (१.२.३१)**: उदात्त और अनुदात्त के समाहार से 'स्वरित' संज्ञा हुई है।")

    # --- ६. १८-भेद विश्लेषण सेक्शन (Matrix) ---
    st.divider()
    st.subheader("🧬 स्वर-भेद मेट्रिक्स (Vowel Genetic Matrix)")
    st.caption("यह तालिका स्वर के संभावित शास्त्रीय भेदों को दर्शाती है।")

    for v in processed_varnas:
        if v.is_vowel:
            with st.expander(f"📊 {v.char} के पाणिनीय भेद विश्लेषण"):
                matrix_data = generate_18_bheda_matrix(v)
                total_bheda = len(matrix_data)

                st.metric(label="कुल स्वीकृत भेद", value=f"{total_bheda}")

                # DataFrame बनाकर टेबल दिखाना
                df = pd.DataFrame(matrix_data)
                st.table(df)

                if total_bheda == 12:
                    reason = "दीर्घाभावात्" if v.char[0] == 'ऌ' else "ह्रस्वाभावात्"
                    st.warning(f"💡 नियम: '{v.char}' के केवल १२ भेद होते हैं ({reason})।")

# --- ७. संदर्भ ---
st.divider()