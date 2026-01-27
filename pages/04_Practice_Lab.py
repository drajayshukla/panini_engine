import streamlit as st
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Simulation Lab - अष्टाध्यायी-यंत्र", layout="wide")
st.title("🧪 पाणिनीय सिमुलेशन लैब: सूत्र-वार इत्-संज्ञा विश्लेषण")

# --- २. साइडबार सेटिंग्स ---
with st.sidebar:
    st.header("⚙️ डायग्नोस्टिक सेटिंग्स")

    # उपदेश का प्रकार (Critical for Sutras)
    source_type_val = st.selectbox(
        "उपदेश का प्रकार (Source Type):",
        options=[e.value for e in UpadeshaType],
        index=0
    )
    source_type = UpadeshaType(source_type_val)

    # तद्धित प्रत्यय के लिए फ्लैग
    is_taddhita = False
    if source_type == UpadeshaType.PRATYAYA:
        is_taddhita = st.checkbox("क्या यह तद्धित प्रत्यय है? (1.3.8 निषेध हेतु)", value=False)

    st.markdown("---")
    st.subheader("📚 प्रैक्टिस सेट्स")
    sample_sets = {
        "Dhatus (1.3.5)": ["ञिमिदाँ", "टुनदीँ", "डुकृञ्"],
        "Pratyayas (1.3.6-8)": ["ष्वुन्", "ञ्युट्", "ल्युट्", "क्त्वा", "ण्यत्"],
        "Vibhaktis (1.3.4 Shield)": ["जस्", "शस्", "टा", "ङे"],
        "General (1.3.2-3)": ["गाधृँ", "दधँ", "स्पर्धँ"]
    }
    category = st.selectbox("श्रेणी चुनें:", options=list(sample_sets.keys()))
    sample_input = st.selectbox("उदाहरण चुनें:", options=sample_sets[category])

# --- ३. मुख्य विश्लेषण लूप ---
input_val = st.text_input("संस्कृत उपदेश लिखें:", value=sample_input)

if input_val:
    # क. 'Gold Standard' विच्छेद
    v_list = sanskrit_varna_vichhed(input_val)

    st.markdown("### 🧬 विच्छेद विश्लेषण")
    st.code(" + ".join(v_list), language=None)

    # ख. मास्टर इंजन से डेटा प्राप्त करना
    # हम इंजन को इस तरह मॉडिफाई करेंगे कि वह 'Step-by-Step' डेटा दे
    remaining, tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list=v_list.copy(),
        original_input=input_val,
        source_type=source_type,
        is_taddhita=is_taddhita
    )

    st.markdown("---")

    # --- ४. सूत्र-वार 'Surgical' विज़ुअलाइज़ेशन ---
    st.subheader("🚩 इत्-संज्ञा प्रकरण (Sutra-wise Mapping)")

    # पाणिनीय सूत्रों का क्रमबद्ध डिस्प्ले
    cols = st.columns(3)

    sutra_info = {
        "१.३.२": "उपदेशेऽजनुनासिक इत् (अनुनासिक स्वर)",
        "१.३.३": "हलन्त्यम् (अन्त्य व्यंजन)",
        "१.३.५": "आदिर्ञिटुडवः (धातु-आदि ञि, टु, डु)",
        "१.३.६": "षः प्रत्ययस्य (प्रत्यय-आदि 'ष्')",
        "१.३.७": "चुट्टू (प्रत्यय-आदि च-वर्ग/ट-वर्ग)",
        "१.३.८": "लशक्वतद्धिते (अ-तद्धित प्रत्यय-आदि ल, श, कु)"
    }

    # सक्रिय सूत्रों को प्रदर्शित करना
    for idx, (s_num, s_name) in enumerate(sutra_info.items()):
        col_idx = idx % 3
        with cols[col_idx]:
            # चेक करें कि क्या यह सूत्र वर्तमान में सक्रिय (Active) हुआ है
            is_active = any(s_num in tag for tag in tags)
            status_color = "green" if is_active else "gray"
            opacity = "1.0" if is_active else "0.4"

            st.markdown(f"""
            <div style="border: 2px solid {status_color}; padding: 10px; border-radius: 5px; opacity: {opacity}; background-color: {'#e6ffed' if is_active else '#f9f9f9'};">
                <small>{s_num}</small><br>
                <b>{s_name}</b><br>
                {'✅ सक्रिय' if is_active else '➖ निष्क्रिय'}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- ५. अंतिम परिणाम (तस्य लोपः) ---
    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.subheader("🔬 मार्क किया गया रूप")
        marked_display = []
        temp_rem = remaining.copy()
        for v in v_list:
            if v in temp_rem:
                marked_display.append(v)
                temp_rem.remove(v)
            else:
                marked_display.append(f"~~{v}~~")
        st.markdown(f"### {' + '.join(marked_display)}")

    with res_col2:
        st.subheader("✨ तस्य लोपः (१.३.९)")
        final_anga = sanskrit_varna_samyoga(remaining)
        st.markdown(f"### {final_anga}")
        st.success(f"अवशेष अङ्ग: **{final_anga}**")

    # --- ६. विशेष निषेध विश्लेषण (Exceptions) ---
    if source_type == UpadeshaType.VIBHAKTI:
        st.info(
            "💡 **विभक्ति सुरक्षा कवच सक्रिय:** सूत्र १.३.४ (न विभक्तौ तुस्माः) के कारण अन्त्य त-वर्ग, 'स्' और 'म्' की इत्-संज्ञा नहीं हुई।")
    if is_taddhita:
        st.warning(
            "💡 **तद्धित निषेध सक्रिय:** सूत्र १.३.८ के 'अतद्धिते' क्लॉज के कारण 'ल', 'श' और 'कु' (क-वर्ग) को बचाया गया।")