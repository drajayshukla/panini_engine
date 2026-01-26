import streamlit as st
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType
from utils.sanskrit_utils import sanskrit_varna_vichhed, sanskrit_varna_samyoga

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Panini Simulation Lab", layout="wide")
st.title("🧪 पाणिनीय सिमुलेशन लैब: सर्व-इत्-संज्ञा अभ्यास")

st.markdown("""
इस लैब में आप अब तक कोड किए गए **सभी इत्-संज्ञा नियमों** का अभ्यास कर सकते हैं। 
यह लैब उपदेश के प्रकार (Dhatu/Pratyaya/Vibhakti) के आधार पर सही सूत्रों को सक्रिय करती है।
""")

# --- २. साइडबार: क्लिनिकल सेटिंग्स ---
with st.sidebar:
    st.header("⚙️ लैब सेटिंग्स")

    # उपदेश का प्रकार चुनना (Critical for 1.3.4, 1.3.7, 1.3.8)
    source_type_val = st.selectbox(
        "उपदेश का प्रकार (Source Type):",
        options=[e.value for e in UpadeshaType],
        index=0
    )
    source_type = UpadeshaType(source_type_val)

    # तद्धित प्रत्यय के लिए फ्लैग (1.3.8 निषेध हेतु)
    is_taddhita = False
    if source_type == UpadeshaType.PRATYAYA:
        is_taddhita = st.checkbox("क्या यह तद्धित प्रत्यय है?", value=False)

    st.markdown("---")
    st.subheader("📚 प्रैक्टिस सेट्स")

    # श्रेणीबद्ध उदाहरण (Categorized Samples)
    sample_sets = {
        "Dhatus (1.3.5)": ["ञिमिदाँ", "टुनदीँ", "डुकृञ्"],
        "Pratyayas (1.3.6-8)": ["ष्वुन्", "ञ्युट्", "ल्युट्", "क्त्वा", "ण्यत्"],
        "Vibhaktis (1.3.4 Shield)": ["जस्", "शस्", "टा", "ङे"],
        "General (1.3.2-3)": ["गाधृँ", "डुदाञ्"]
    }

    category = st.selectbox("श्रेणी चुनें:", options=list(sample_sets.keys()))
    sample_input = st.selectbox("उदाहरण चुनें:", options=sample_sets[category])

# --- ३. मुख्य इनपुट एरिया ---
st.subheader("🔍 डायग्नोस्टिक इनपुट")
input_val = st.text_input("संस्कृत उपदेश लिखें या उदाहरण चुनें:", value=sample_input)

if st.button("Run Full Analysis"):
    # १. विच्छेद
    v_list = sanskrit_varna_vichhed(input_val)

    # २. मास्टर इंजन को कॉल करना (All rules run inside this)
    remaining, tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list=v_list.copy(),
        original_input=input_val,
        source_type=source_type,
        is_taddhita=is_taddhita
    )

    st.markdown("---")

    # --- ४. विज़ुअल ट्रेस (Mark then Delete) ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("१. इत्-संज्ञा (Identification)")

        # 'Strikethrough' विज़ुअलाइज़ेशन
        marked_display = []
        temp_remaining = remaining.copy()
        for v in v_list:
            if v in temp_remaining:
                marked_display.append(v)
                temp_remaining.remove(v)
            else:
                marked_display.append(f"~~{v}~~")

        st.markdown(f"### {' + '.join(marked_display)}")

        # सभी सक्रिय सूत्रों की सूची
        if tags:
            st.write("**सक्रिय सूत्र (Active Rules):**")
            for t in tags:
                st.warning(f"🚩 {t}")
        else:
            st.info("कोई इत्-संज्ञा नियम लागू नहीं हुआ।")

    with col2:
        st.subheader("२. तस्य लोपः (Execution)")
        st.markdown(f"### {' + '.join(remaining)}")

        final_anga = sanskrit_varna_samyoga(remaining)
        st.success(f"अन्तिम अङ्ग (१.३.९): **{final_anga}**")

    # --- ५. सूत्र विश्लेषण टेबल ---
    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश (Workflow Summary)")

    workflow_data = [
        {"चरण": "विच्छेद", "स्थिति": " + ".join(v_list), "सूत्र": "-"},
        {"चरण": "टैगिंग", "स्थिति": " + ".join(marked_display), "सूत्र": "१.३.२ - १.३.८"},
        {"चरण": "लोप", "स्थिति": final_anga, "सूत्र": "१.३.९"}
    ]
    st.table(workflow_data)