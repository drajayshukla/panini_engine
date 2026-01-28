import streamlit as st
import pandas as pd
import os

# कोर पाणिनीय मॉड्यूल्स
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.upadesha_registry import UpadeshaType
from core.it_sanjna_engine import ItSanjnaEngine
from core.analyzer import analyze_sanjna
from core.morph_rules import apply_ata_upadhayah_7_2_116
from utils.data_loader import get_all_dhatus

# --- १. पेज सेटअप एवं स्टाइलिंग ---
st.set_page_config(page_title="इंजन - अष्टाध्यायी-यंत्र", layout="wide", page_icon="⚙️")
st.title("⚙️ पाणिनीय इंजन (Processor)")
st.markdown("---")

# --- २. डेटा लोडिंग (Master Dhatupatha) ---
# १८००+ धातुओं को लोड करना ताकि यूजर सीधे सर्च कर सके
all_dhatus = get_all_dhatus()
dhatu_options = {f"{d['upadesha']} ({d['artha_sanskrit']})": d['upadesha'] for d in all_dhatus}

# --- ३. साइड पैनल (Sidebar Settings) ---
with st.sidebar:
    st.header("📚 उपदेश चयन एवं सेटिंग्स")

    # मास्टर सर्च बॉक्स
    search_input = st.selectbox(
        "धातुपाठ से धातु चुनें:",
        options=[""] + list(dhatu_options.keys()),
        index=0,
        help="यहाँ १८००+ धातुओं में से सर्च करें"
    )

    st.markdown("---")

    # मैन्युअल सेटिंग्स
    manual_source_type = st.selectbox(
        "उपदेश प्रकार (Override):",
        options=[e.value for e in UpadeshaType],
        index=0
    )

    manual_taddhita = st.checkbox("Manual Taddhita Flag", value=False)
    st.info("नोट: धातु चयन करने पर ऑटो-डिटेक्शन प्राथमिकता लेगा।")

# --- ४. मुख्य इनपुट प्रोसेसिंग ---
# यदि सर्च से कुछ चुना गया है तो वह डिफ़ॉल्ट बनेगा, अन्यथा 'गाधृँ'
default_val = dhatu_options[search_input] if search_input else "गाधृँ"
raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय/आगम) यहाँ लिखें:", value=default_val)

if raw_input:
    input_text = raw_input.strip()

    # १. ऑटो-डिटेक्शन (Registry Upgrade)
    detected_type, is_taddhita_flag = UpadeshaType.auto_detect(input_text)

    # फाइनल पैरामीटर्स का निर्धारण
    source_type = detected_type if detected_type else UpadeshaType(manual_source_type)
    is_taddhita_final = is_taddhita_flag if detected_type else manual_taddhita

    # २. वर्ण विच्छेद (Surgical Varna Objects)
    # यह ग् + आ + ध् + ऋ + ँ के रूप में विच्छेद करेगा
    varna_list = sanskrit_varna_vichhed(input_text)

    # ३. इत्-संज्ञा इंजन (Core Execution)
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list,
        input_text,
        source_type,
        is_taddhita=is_taddhita_final
    )

    # UI फीडबैक (Sidebar)
    if detected_type:
        st.sidebar.success(f"✅ पहचाना गया: {detected_type.value}")
    if is_taddhita_final:
        st.sidebar.warning("🛡️ तद्धित निषेध (१.३.८) सक्रिय")

    # --- ५. विज़ुअलाइज़ेशन (Main Display) ---
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("१. इत्-संज्ञा (Identification)")
        # विज़ुअलाइज़ेशन के लिए स्ट्रिंग मैपिंग
        marked_display = []
        for v in varna_list:
            if v in remaining_varnas:
                marked_display.append(v.char)
            else:
                marked_display.append(f"~~{v.char}~~")

        st.markdown(f"**मार्क किया गया रूप (तस्य लोपः पूर्वम्):**")
        st.markdown(f"### {' + '.join(marked_display)}")

        if it_tags:
            for tag in it_tags:
                st.markdown(f"🚩 {tag}")
        else:
            st.info("कोई इत्-संज्ञा प्राप्त नहीं हुई।")

    with col2:
        st.subheader("२. तस्य लोपः (Execution)")
        st.markdown(f"**लोप के बाद (१.३.९):**")
        st.markdown(f"### {' + '.join([v.char for v in remaining_varnas])}")

        # शुद्ध अङ्ग का संयोग
        shuddha_anga = sanskrit_varna_samyoga(remaining_varnas)
        st.success(f"अन्तिम अङ्ग: **{shuddha_anga}**")

    # --- ६. विश्लेषण (Phonetic Analysis Matrix) ---
    st.markdown("---")
    st.subheader("🔍 ३. वर्ण-विश्लेषण एवं संज्ञा मैट्रिक्स")

    # विश्लेषण डेटा प्राप्त करें
    analysis = analyze_sanjna(varna_list)

    # डायनामिक कॉलम्स (वर्णों की संख्या के आधार पर)
    cols = st.columns(len(varna_list) if varna_list else 1)
    for idx, item in enumerate(analysis):
        with cols[idx]:
            # क्या यह वर्ण लोप हो चुका है?
            is_it = varna_list[idx] not in remaining_varnas
            box_color = "🔴" if is_it else "🔵"

            st.info(f"{box_color} **{item['varna']}**\n\n{', '.join(item['tags']) if item['tags'] else '-'}")
            if 'sthana' in item:
                st.caption(f"स्थान: {item['sthana']}")

    # --- ७. विधि-सूत्र (Morphology & Anga-Karya) ---
    st.markdown("---")
    st.subheader("🧪 ४. विधि-सूत्र (Rule Application)")

    # ७.२.११६ अत उपधायाः की जाँच (णित्/ञित् प्रत्यय मानकर)
    morph_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy(), is_nit_prakaran=True)

    if is_applied:
        st.success(f"**अत उपधायाः (७.२.११६)** लागू हुआ!")
        st.markdown(f"### {shuddha_anga} ➔ {sanskrit_varna_samyoga(morph_varnas)}")
    else:
        st.info("वर्तमान अङ्ग पर कोई विधि-सूत्र सक्रिय नहीं है।")

    # --- ८. प्रक्रिया सारांश (Final Audit) ---
    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश (Workflow Summary)")
    steps_data = [
        {"क्रम": 1, "प्रक्रिया": "मूल उपदेश", "विवरण": input_text},
        {"क्रम": 2, "प्रक्रिया": "वर्ण विच्छेद", "विवरण": " + ".join([v.char for v in varna_list])},
        {"क्रम": 3, "प्रक्रिया": "इत्-लोप (१.३.९)", "विवरण": shuddha_anga},
        {"क्रम": 4, "प्रक्रिया": "अन्तिम अङ्ग रूप",
         "विवरण": sanskrit_varna_samyoga(morph_varnas) if is_applied else shuddha_anga}
    ]
    st.table(steps_data)