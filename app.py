import streamlit as st
import os
from core.upadesha_registry import UpadeshaType
from core.it_sanjna_engine import ItSanjnaEngine
from core.phonology import sanskrit_varna_vichhed
from core.analyzer import analyze_sanjna
from core.morph_rules import apply_ata_upadhayah_7_2_116

# पेज सेटअप
st.set_page_config(page_title="अष्टाध्यायी-यंत्र", layout="wide", initial_sidebar_state="expanded")

st.title("🕉️ अष्टाध्यायी-यंत्र (The Paninian Engine)")
st.caption("एक ओपन-सोर्स पाणिनीय व्याकरण इंजन | Developed by Dr. Ajay Shukla")

# साइडबार
with st.sidebar:
    st.header("🎯 विजन और मिशन")

    # सूचना: अब टाइप अपने आप डिटेक्ट होता है, पर मैन्युअल विकल्प भी खुला है
    st.info("इंजन अब आपके इनपुट को स्वतः (Auto-detect) पहचानने में सक्षम है।")

    source_type_input = st.selectbox(
        "उपदेश का प्रकार चुनें (Manual Override):",
        options=[e.value for e in UpadeshaType],
        index=0
    )
    manual_source_type = UpadeshaType(source_type_input)

    st.write("### 📜 वर्तमान सूत्र")
    st.write("1.1.1, 1.1.2, 1.3.2, 1.3.3, 1.3.5, 7.2.116")

# मुख्य इनपुट
raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value="पठँ")

if raw_input:
    # १. स्पेस क्लीनिंग (Input Normalization)
    input_text = raw_input.strip()
    if raw_input != input_text:
        st.warning(f"⚠️ अतिरिक्त स्पेस पाया गया। '{input_text}' पर प्रक्रिया की जा रही है।")

    # २. ऑटो-डिटेक्शन लॉजिक
    detected_type = UpadeshaType.auto_detect(input_text)

    # यदि डेटाबेस में मिला तो वह टाइप लें, वरना साइडबार वाला मैन्युअल टाइप
    source_type = detected_type if detected_type else manual_source_type

    # ३. यूजर को फीडबैक दें
    if detected_type:
        st.success(f"✅ पहिचान: **{detected_type.value}** (डेटाबेस से प्रमाणित)")
    else:
        st.warning(
            f"🔬 ध्यान दें: '{input_text}' डेटाबेस में नहीं मिला। इसे **{source_type.value}** मानकर प्रक्रिया की जा रही है।")

    st.markdown("---")

    # --- प्रक्रिया प्रवाह (Process Flow) ---

    # 1. विच्छेद प्रक्रिया
    varna_list = sanskrit_varna_vichhed(input_text)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("१. वर्ण-विच्छेद (Phonology)")
        st.code(" + ".join(varna_list), language=None)

    # 2. इत्-संज्ञा प्रक्रिया
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list.copy(),
        input_text,
        source_type
    )

    with col2:
        st.subheader("२. इत्-संज्ञा (It-Sanjna)")
        if it_tags:
            for tag in it_tags:
                # Markdown का उपयोग करें ताकि Ashtadhyayi.com के लिंक काम करें
                st.markdown(f"🚩 {tag}")
            st.success(f"**अन्तिम अङ्ग:** {' + '.join(remaining_varnas)}")
        else:
            st.warning("कोई इत् वर्ण नहीं मिला।")

    # 3. संज्ञा विश्लेषण
    st.markdown("---")
    st.subheader("🔍 ३. संज्ञा विश्लेषण (Sanjna Analysis)")
    analysis = analyze_sanjna(varna_list)
    cols = st.columns(len(varna_list) if len(varna_list) > 0 else 1)
    for idx, item in enumerate(analysis):
        with cols[idx]:
            v = item['varna']
            tags = item['tags']
            if tags:
                st.success(f"**{v}**\n\n`{', '.join(tags)}`")
            else:
                st.info(f"**{v}**\n\n-")

    # 4. विधि-सूत्र (7.2.116 - अत उपधायाः)
    result_varnas = remaining_varnas.copy()
    is_applied = False

    if len(remaining_varnas) >= 2:
        st.markdown("---")
        st.subheader("🛠️ ४. विधि-सूत्र कार्यान्वयनम् (Vidhi Sutra)")
        result_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy())

        if is_applied:
            st.success(f"**परिवर्तित रूप (वृद्धि):** {' + '.join(result_varnas)}")
            st.info("**प्रयुक्त सूत्रम्:** ७.२.११६ अत उपधायाः")
            final_form = "".join(result_varnas).replace('्', '')
            st.latex(rf"{input_text} \xrightarrow{{7.2.116}} {final_form}")

    # 5. सारांश तालिका
    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश")
    steps = [
        {"क्रम": 1, "प्रक्रिया": "मूल रूप", "स्थिति": input_text, "सूत्र": "-"},
        {"क्रम": 2, "प्रक्रिया": "वर्ण-विच्छेद", "स्थिति": " + ".join(varna_list), "सूत्र": "Phonology"},
        {"क्रम": 3, "प्रक्रिया": "इत्-लोप", "स्थिति": " + ".join(remaining_varnas), "सूत्र": "1.3.x"},
        {"क्रम": 4, "प्रक्रिया": "विधि (वृद्धि)", "स्थिति": "".join(result_varnas) if is_applied else "यथावत्",
         "सूत्र": "7.2.116"}
    ]
    st.table(steps)