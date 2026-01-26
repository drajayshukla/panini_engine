import streamlit as st
from core.phonology import sanskrit_varna_vichhed
from core.it_sanjna_engine import apply_halantyam
from core.analyzer import analyze_sanjna
# एरर सुधार: morph_rules को इम्पोर्ट करना आवश्यक है
from core.morph_rules import apply_ata_upadhayah_7_2_116

# पेज सेटअप
st.set_page_config(page_title="अष्टाध्यायी-यंत्र", layout="wide", initial_sidebar_state="expanded")

st.title("🕉️ अष्टाध्यायी-यंत्र (The Paninian Engine)")
st.caption("एक ओपन-सोर्स पाणिनीय व्याकरण इंजन | Developed by Dr. Ajay Shukla")

# साइडबार
with st.sidebar:
    st.header("🎯 विजन और मिशन")
    st.info("यह इंजन वर्तमान में 'इत्-संज्ञा', 'संज्ञा प्रकरण' और 'वृद्धि विधि' पर कार्य कर रहा है।")
    st.write("### 📜 वर्तमान सूत्र")
    st.write("1.1.1, 1.1.2, 1.3.3, 7.2.116")

# मुख्य इनपुट
input_text = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value="पठ्")

if input_text:
    # 1. विच्छेद प्रक्रिया
    varna_list = sanskrit_varna_vichhed(input_text)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("१. वर्ण-विच्छेद (Phonology)")
        st.code(" + ".join(varna_list), language=None)

    # 2. इत्-संज्ञा प्रक्रिया
    remaining, its = apply_halantyam(varna_list.copy())
    with col2:
        st.subheader("२. इत्-संज्ञा (It-Sanjna)")
        if its:
            st.error(f"लोप: {' , '.join(its)} (Sutra 1.3.3)")
        else:
            st.warning("कोई इत् वर्ण नहीं मिला।")

    st.markdown("---")

    # 3. संज्ञा विश्लेषण
    st.subheader("🔍 ३. संज्ञा विश्लेषण (Sanjna Analysis)")
    analysis = analyze_sanjna(varna_list)
    cols = st.columns(len(varna_list) if len(varna_list) > 0 else 1)
    for idx, item in enumerate(analysis):
        with cols[idx]:
            if item['tags']:
                st.success(f"**{item['varna']}**\n\n`{', '.join(item['tags'])}`")
            else:
                st.info(f"**{item['varna']}**\n\n-")

    # 4. विधि-सूत्र (7.2.116 - अत उपधायाः)
    # इसे 'पठ्' के लिए विशिष्ट बनाया गया है जैसा आपने चाहा था
    if "अ" in varna_list:
        st.markdown("---")
        st.subheader("🛠️ ४. विधि-सूत्र कार्यान्वयनम् (Vidhi Sutra)")

        # विधि सूत्र लागू करना
        result_varnas, is_applied = apply_ata_upadhayah_7_2_116(varna_list.copy())

        if is_applied:
            st.success(f"**परिवर्तित रूप (वृद्धि):** {' + '.join(result_varnas)}")
            st.info("**प्रयुक्त सूत्रम्:** ७.२.११६ अत उपधायाः")

            # विजुअल ट्रांसफॉर्मेशन
            st.latex(r"पठ् \xrightarrow{7.2.116} पाठ्")

    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश")
    steps = [
        {"क्रम": 1, "प्रक्रिया": "मूल रूप", "स्थिति": input_text, "सूत्र": "-"},
        {"क्रम": 2, "प्रक्रिया": "वर्ण-विच्छेद", "स्थिति": " + ".join(varna_list), "सूत्र": "Phonology Rules"},
        {"क्रम": 3, "प्रक्रिया": "उपधा वृद्धि",
         "स्थिति": " + ".join(result_varnas) if 'result_varnas' in locals() else "-", "सूत्र": "७.२.११६"}
    ]
    st.table(steps)