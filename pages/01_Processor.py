import streamlit as st
import pandas as pd
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.upadesha_registry import UpadeshaType
from core.it_sanjna_engine import ItSanjnaEngine
from core.analyzer import analyze_sanjna
from core.morph_rules import apply_ata_upadhayah_7_2_116

# --- १. पेज सेटअप ---
st.set_page_config(page_title="इंजन - अष्टाध्यायी-यंत्र", layout="wide")
st.title("⚙️ पाणिनीय इंजन (Processor)")

# --- २. साइड पैनल (Sidebar) ---
with st.sidebar:
    st.header("📚 अभ्यास एवं सेटिंग्स")
    example_list = {
        "कस्टम": "",
        "गाधृँ (Dhatu)": "गाधृँ",
        "ष्वुन् (Shit-Krut)": "ष्वुन्",
        "ञ्युट् (Chuttu-Krut)": "ञ्युट्",
        "जस् (Vibhakti)": "जस्",
        "एधँ (Dhatu)": "एधँ"
    }
    selected_example = st.selectbox("प्रमुख उदाहरण चुनें:", options=list(example_list.keys()))

    st.markdown("---")
    source_type_input = st.selectbox(
        "Manual Override:",
        options=[e.value for e in UpadeshaType],
        index=0
    )
    manual_source_type = UpadeshaType(source_type_input)
    manual_taddhita = st.checkbox("Manual Taddhita Flag (Force)", value=False)

# --- ३. मुख्य इनपुट प्रोसेसिंग ---
default_input = example_list[selected_example] if selected_example != "कस्टम" else "गाधृँ"
raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value=default_input)

if raw_input:
    input_text = raw_input.strip()

    # १. ऑटो-डिटेक्शन (Registry Upgrade)
    detected_type, is_taddhita_flag = UpadeshaType.auto_detect(input_text)
    source_type = detected_type if detected_type else manual_source_type
    is_taddhita_final = is_taddhita_flag if detected_type else manual_taddhita

    # २. वर्ण विच्छेद (Varna Objects)
    varna_list = sanskrit_varna_vichhed(input_text)

    # ३. इत्-संज्ञा इंजन (Upgraded logic)
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list,
        input_text,
        source_type,
        is_taddhita=is_taddhita_final
    )

    # ४. UI फीडबैक
    if detected_type:
        st.sidebar.success(f"✅ ऑटो-डिटेक्ट: {detected_type.value}")
    else:
        st.sidebar.info(f"ℹ️ मोड: {manual_source_type.value}")

    # --- ४. विज़ुअलाइज़ेशन ---
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("१. इत्-संज्ञा (Identification)")
        # Object-safe display: Compare via indices to avoid object identity issues
        marked_display = []
        rem_chars = [v.char for v in remaining_varnas]

        for v in varna_list:
            if v in remaining_varnas:
                marked_display.append(v.char)
            else:
                marked_display.append(f"~~{v.char}~~")

        st.markdown(f"**मार्क किया गया रूप (तस्य लोपः पूर्वम्):**")
        st.markdown(f"### {' + '.join(marked_display)}")
        for tag in it_tags: st.markdown(f"🚩 {tag}")

    with col2:
        st.subheader("२. तस्य लोपः (Execution)")
        st.markdown(f"**लोप के बाद (१.३.९):**")
        st.markdown(f"### {' + '.join([v.char for v in remaining_varnas])}")
        shuddha_anga = sanskrit_varna_samyoga(remaining_varnas)
        st.success(f"अन्तिम अङ्ग: **{shuddha_anga}**")

    # --- ५. विश्लेषण (Analyzer Integration) ---
    st.markdown("---")
    st.subheader("🔍 ३. संज्ञा विश्लेषण (Phonetic Analysis)")
    analysis = analyze_sanjna(varna_list)

    cols = st.columns(len(varna_list))
    for idx, item in enumerate(analysis):
        with cols[idx]:
            # Determine if it was an 'it' varna
            is_it = varna_list[idx] not in remaining_varnas
            box_style = "🔴" if is_it else "🔵"
            st.info(f"{box_style} **{item['varna']}**\n\n{', '.join(item['tags']) if item['tags'] else '-'}")
            if 'sthana' in item:
                st.caption(f"स्थान: {item['sthana']}")

    # --- ६. विधि-सूत्र (Morphology) ---
    st.markdown("---")
    st.subheader("🧪 ४. विधि-सूत्र एवं अङ्ग-कार्य")

    # ७.२.११६ अत उपधायाः की जाँच (ञित्/णित् प्रत्यय का संदर्भ मानकर)
    # हम उदाहरण के लिए मान रहे हैं कि 'पठ्' के बाद 'ण्वुल्' जैसी स्थिति है
    morph_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy(), is_nit_prakaran=True)

    if is_applied:
        st.success(f"**अत उपधायाः (७.२.११६)** लागू हुआ!")
        st.markdown(f"### {sanskrit_varna_samyoga(remaining_varnas)} ➔ {sanskrit_varna_samyoga(morph_varnas)}")
    else:
        st.info("वर्तमान अङ्ग पर कोई विधि-सूत्र (Morphology) सक्रिय नहीं है।")

    # --- ७. प्रक्रिया सारांश ---
    st.table([
        {"क्रम": 1, "प्रक्रिया": "उपदेश", "स्थिति": input_text},
        {"क्रम": 2, "प्रक्रिया": "विच्छेद", "स्थिति": " + ".join([v.char for v in varna_list])},
        {"क्रम": 3, "प्रक्रिया": "अन्तिम रूप",
         "स्थिति": sanskrit_varna_samyoga(morph_varnas if is_applied else remaining_varnas)}
    ])