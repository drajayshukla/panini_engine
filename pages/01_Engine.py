import streamlit as st
from core.upadesha_registry import UpadeshaType
from core.it_sanjna_engine import ItSanjnaEngine
from core.phonology import sanskrit_varna_vichhed
from core.analyzer import analyze_sanjna
from core.morph_rules import apply_ata_upadhayah_7_2_116

st.set_page_config(page_title="इंजन - अष्टाध्यायी-यंत्र", layout="wide")

st.title("⚙️ पाणिनीय इंजन (Processor)")

# साइडबार ओवरराइड
with st.sidebar:
    st.header("🎯 इंजन सेटिंग्स")
    source_type_input = st.selectbox(
        "उपदेश का प्रकार (Manual):",
        options=[e.value for e in UpadeshaType],
        index=0
    )
    manual_source_type = UpadeshaType(source_type_input)

# मुख्य इनपुट
raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value="पठँ")

if raw_input:
    input_text = raw_input.strip()
    detected_type = UpadeshaType.auto_detect(input_text)
    source_type = detected_type if detected_type else manual_source_type

    if detected_type:
        st.success(f"✅ पहिचान: **{detected_type.value}**")

    st.markdown("---")

    # 1. विच्छेद
    varna_list = sanskrit_varna_vichhed(input_text)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("१. वर्ण-विच्छेद")
        st.code(" + ".join(varna_list), language=None)

    # 2. इत्-संज्ञा
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list.copy(), input_text, source_type
    )
    with col2:
        st.subheader("२. इत्-संज्ञा")
        if it_tags:
            for tag in it_tags: st.markdown(f"🚩 {tag}")
            st.success(f"अन्तिम अङ्ग: {''.join(remaining_varnas)}")
        else:
            st.warning("कोई इत् वर्ण नहीं मिला।")

    # 3. संज्ञा विश्लेषण
    st.markdown("---")
    st.subheader("🔍 ३. संज्ञा विश्लेषण")
    analysis = analyze_sanjna(varna_list)
    cols = st.columns(len(varna_list) if len(varna_list) > 0 else 1)
    for idx, item in enumerate(analysis):
        with cols[idx]:
            st.info(f"**{item['varna']}**\n\n`{', '.join(item['tags']) if item['tags'] else '-'}`")

    # 4. विधि-सूत्र (7.2.116)
    result_varnas = remaining_varnas.copy()
    is_applied = False
    if len(remaining_varnas) >= 2:
        st.markdown("---")
        st.subheader("🛠️ ४. विधि-सूत्र")
        result_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy())
        if is_applied:
            st.success(f"परिवर्तित रूप: {''.join(result_varnas)}")
            st.info("सूत्र: ७.२.११६ अत उपधायाः")

    # 5. सारांश तालिका
    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश")
    steps = [
        {"क्रम": 1, "प्रक्रिया": "मूल रूप", "स्थिति": input_text, "सूत्र": "-"},
        {"क्रम": 2, "प्रक्रिया": "इत्-लोप", "स्थिति": "".join(remaining_varnas), "सूत्र": "1.3.x"},
        {"क्रम": 3, "प्रक्रिया": "वृद्धि", "स्थिति": "".join(result_varnas) if is_applied else "यथावत्", "सूत्र": "7.2.116"}
    ]
    st.table(steps)