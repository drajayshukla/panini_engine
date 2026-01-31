import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

# --- पेज कॉन्फ़िगरेशन (Page Config) ---
st.set_page_config(
    page_title="शब्द-रूप सिद्धि यन्त्र",
    page_icon="🔍",
    layout="wide"
)

# --- कस्टम CSS (Custom CSS for Sanskrit/Hindi) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;700&display=swap');

    /* संस्कृत टेक्स्ट के लिए */
    .sanskrit-text { 
        font-family: 'Martel', serif; 
        font-size: 1.3rem; 
        color: #2c3e50;
    }

    /* बड़े सिद्ध पदों के लिए */
    .big-sanskrit { 
        font-family: 'Martel', serif; 
        font-size: 2rem; 
        font-weight: bold; 
        color: #8e44ad; 
    }

    /* प्रक्रिया बॉक्स की स्टाइलिंग */
    .step-box { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 12px; 
        border-left: 6px solid #8e44ad; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
    }

    .rule-id { 
        color: #e74c3c; 
        font-weight: bold; 
        font-size: 1rem; 
        margin-bottom: 5px;
    }

    .op-text { 
        font-weight: bold; 
        color: #2980b9; 
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- हेल्पर डेटा (Helper Data in Sanskrit/Hindi) ---
VIBHAKTI_MAP = {
    1: "प्रथमा (Nominative)",
    2: "द्वितीया (Accusative)",
    3: "तृतीया (Instrumental)",
    4: "चतुर्थी (Dative)",
    5: "पञ्चमी (Ablative)",
    6: "षष्ठी (Genitive)",
    7: "सप्तमी (Locative)",
    8: "सम्बोधन (Vocative)"
}

VACANA_MAP = {
    1: "एकवचनम्",
    2: "द्विवचनम्",
    3: "बहुवचनम्"
}


def main():
    # --- मुख्य शीर्षक ---
    st.title("🔍 शब्द-रूप सिद्धि यन्त्र")
    st.markdown("पाणिनीय सूत्रों के आधार पर शब्द-रूपों की स्वचालित सिद्धि।")
    st.markdown("---")

    # --- साइडबार (Sidebar Inputs) ---
    with st.sidebar:
        st.header("इनपुट (Input)")

        # इनपुट फील्ड हिंदी में
        stem = st.text_input("प्रातिपदिक (मूल शब्द)", value="राम")

        st.info(
            """
            ℹ️ **नोट:** वर्तमान में यह इंजन केवल **'अकारांत पुल्लिंग'** (जैसे राम, देव, बाल) शब्दों के लिए अनुकूलित है।
            """
        )

    # --- तालिका निर्माण (Table Generation) ---
    if stem:
        st.subheader(f"📖 शब्द रूपावली: {stem} (अकारांत पुल्लिंग)")

        table_data = []
        for v in range(1, 9):
            row = {"विभक्ति": VIBHAKTI_MAP[v]}
            for n in range(1, 4):
                # सुबंत प्रोसेसर को कॉल करना
                word = SubantaProcessor.derive_pada(stem, v, n, None)
                row[VACANA_MAP[n]] = word
            table_data.append(row)

        # डेटाफ्रेम बनाना
        df = pd.DataFrame(table_data)

        # टेबल दिखाना
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "विभक्ति": st.column_config.TextColumn("विभक्ति", width="medium"),
                "एकवचनम्": st.column_config.TextColumn("एकवचनम्", width="large"),
                "द्विवचनम्": st.column_config.TextColumn("द्विवचनम्", width="large"),
                "बहुवचनम्": st.column_config.TextColumn("बहुवचनम्", width="large"),
            }
        )

    st.divider()

    # --- ग्लास-बॉक्स इंस्पेक्टर (Derivation Inspector) ---
    st.header("🔬 ग्लास-बॉक्स विश्लेषण (Siddhi Inspector)")
    st.info("नीचे दी गई सूची से विभक्ति और वचन चुनें और 'सिद्धि देखें' बटन दबाएं।")

    # 3 कॉलम लेआउट
    c1, c2, c3 = st.columns(3)

    with c1:
        sel_vib = st.selectbox("विभक्ति चुनें", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])

    with c2:
        sel_vac = st.selectbox("वचन चुनें", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])

    with c3:
        st.write("")  # स्पेसिंग के लिए खाली
        st.write("")
        derive_btn = st.button("सिद्धि प्रक्रिया देखें (Derive)", type="primary")

    # --- परिणाम प्रदर्शन ---
    if derive_btn:
        # लॉगर शुरू करें
        logger = PrakriyaLogger()
        result = SubantaProcessor.derive_pada(stem, sel_vib, sel_vac, logger)

        # अंतिम परिणाम दिखाएं
        st.markdown(f"### सिद्ध पद: <span class='big-sanskrit'>{result}</span>", unsafe_allow_html=True)
        st.write("---")

        # इतिहास (History) दिखाएं
        history = logger.get_history()

        if not history:
            st.warning("कोई प्रक्रिया उपलब्ध नहीं है।")
        else:
            st.subheader("चरण-दर-चरण प्रक्रिया (Step-by-Step Derivation)")

            for step in history:
                st.markdown(f"""
                <div class="step-box">
                    <div class="rule-id">📖 {step['rule']}</div>
                    <div class="op-text">{step['operation']}</div>
                    <div class="sanskrit-text">स्थिति: <b>{step['result']}</b></div>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()