import streamlit as st
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType
# --- नया इम्पोर्ट यहाँ है ---
from utils.sanskrit_utils import sanskrit_varna_vichhed, sanskrit_varna_samyoga

st.set_page_config(page_title="Sutra Practice Lab", layout="wide")

st.title("🧪 Sutra Practice Lab: १.३.५ आदिर्ञिटुडवः")

st.markdown("""
इस लैब में हम **धातु के आदि** में आने वाले विशिष्ट समुदायों की इत्-संज्ञा का अभ्यास करेंगे।
- **ञि** (Nyi) → ञीत्
- **टु** (Tu) → ट्वित्
- **डु** (Du) → ड्वित्
""")

# अभ्यास के लिए धातु डेटाबेस
lab_samples = {
    "ञिमिदाँ (स्नेहने)": "ञिमिदाँ",
    "टुनदीँ (समृद्धौ)": "टुनदीँ",
    "डुकृञ् (करणे)": "डुकृञ्",
    "ञिक्ष्विदाँ (स्नेहने)": "ञिक्ष्विदाँ",
    "टुक्षु (शब्दे)": "टुक्षु"
}

selection = st.selectbox("अभ्यास के लिए धातु चुनें:", options=list(lab_samples.keys()))
input_val = lab_samples[selection]

if st.button("Analyze Sutra 1.3.5"):
    # १. विच्छेद (अब एरर नहीं आएगा)
    v_list = sanskrit_varna_vichhed(input_val)

    # २. इंजन को कॉल करें
    remaining, tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list=v_list.copy(),
        original_input=input_val,
        source_type=UpadeshaType.DHATU
    )

    st.markdown("---")
    st.subheader("🔬 विश्लेषण परिणाम")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**मूल वर्ण क्रम:**")
        st.write(" + ".join(v_list))

        # आदिर्ञिटुडवः (1.3.5) का विशिष्ट टैग दिखाएं
        sutra_5_tags = [t for t in tags if "१.३.५" in t]
        if sutra_5_tags:
            for t in sutra_5_tags:
                st.warning(f"🎯 सक्रिय सूत्र: {t}")
        else:
            st.info("इस धातु के आदि में ञि, टु, या डु नहीं है।")

    with col2:
        st.write("**तस्य लोपः (१.३.९) के बाद:**")
        st.write(" + ".join(remaining))
        st.success(f"शुद्ध अङ्ग: **{sanskrit_varna_samyoga(remaining)}**")