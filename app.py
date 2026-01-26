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
    source_type_input = st.selectbox(
        "उपदेश का प्रकार चुनें (Upadesha Type):",
        options=[e.value for e in UpadeshaType],
        index=0
    )
    source_type = UpadeshaType(source_type_input)

    st.info("यह इंजन वर्तमान में 'इत्-संज्ञा', 'संज्ञा प्रकरण' और 'वृद्धि विधि' पर कार्य कर रहा है।")
    st.write("### 📜 वर्तमान सूत्र")
    st.write("1.1.1, 1.1.2, 1.3.2, 1.3.3, 1.3.5, 7.2.116")

# मुख्य इनपुट
input_text = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value="पठँ")

if input_text:
    # --- नया वैलिडेशन लॉजिक ---
    is_valid = UpadeshaType.validate_input(input_text, source_type)

    if is_valid:
        st.success(f"✅ यह एक प्रामाणिक **{source_type.value}** उपदेश है (डेटाबेस में उपलब्ध)।")
    else:
        st.warning(
            f"⚠️ ध्यान दें: '{input_text}' आपके वर्तमान **{source_type.value}** डेटाबेस में नहीं मिला। इसे कस्टम इनपुट माना जा रहा है।")
    st.markdown("---")

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
                st.error(f"इत् संज्ञा/लोप: {tag}")
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

    # वृद्धि केवल तभी चेक करें जब 'अ' उपधा में हो
    if len(remaining_varnas) >= 2:
        st.markdown("---")
        st.subheader("🛠️ ४. विधि-सूत्र कार्यान्वयनम् (Vidhi Sutra)")
        result_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy())

        if is_applied:
            st.success(f"**परिवर्तित रूप (वृद्धि):** {' + '.join(result_varnas)}")
            st.info("**प्रयुक्त सूत्रम्:** ७.२.११६ अत उपधायाः")
            # डायनामिक लेटेक्स डिस्प्ले
            final_form = "".join(result_varnas).replace('्', '')
            st.latex(rf"{input_text} \xrightarrow{{7.2.116}} {final_form}")

    # 5. सारांश तालिका
    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश")
    steps = [
        {"क्रम": 1, "प्रक्रिया": "मूल रूप", "स्थिति": input_text, "सूत्र": "-"},
        {"क्रम": 2, "प्रक्रिया": "वर्ण-विच्छेद", "स्थिति": " + ".join(varna_list), "सूत्र": "Phonology Rules"},
        {"क्रम": 3, "प्रक्रिया": "इत्-लोप", "status": "Done", "स्थिति": " + ".join(remaining_varnas),
         "सूत्र": "1.3.2, 1.3.3, 1.3.5"},
        {"क्रम": 4, "प्रक्रिया": "विधि (वृद्धि)", "status": "Applied" if is_applied else "Skipped",
         "स्थिति": " + ".join(result_varnas) if is_applied else "कोई परिवर्तन नहीं", "सूत्र": "७.२.११६"}
    ]
    st.table(steps)