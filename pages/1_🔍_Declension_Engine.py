import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि यन्त्र", page_icon="🔍", layout="wide")

# --- CSS Styling for Clarity ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;700&display=swap');
    
    .sanskrit-text { font-family: 'Martel', serif; font-size: 1.4rem; color: #2c3e50; font-weight: bold; }
    .big-sanskrit { font-family: 'Martel', serif; font-size: 2.2rem; font-weight: bold; color: #8e44ad; }
    
    /* Container for each step */
    .step-box { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        border-left: 6px solid #8e44ad; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
    }
    
    /* Varna-Viccheda Style */
    .viccheda-box {
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        color: #d35400;
        font-size: 1.1rem;
        margin-top: 5px;
    }

    .rule-id { color: #e74c3c; font-weight: bold; font-size: 0.9rem; }
    .op-text { font-weight: bold; color: #2980b9; font-size: 1.1rem; }
    .label-text { font-size: 0.8rem; color: #7f8c8d; }
</style>
""", unsafe_allow_html=True)

# --- Data ---
VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def main():
    st.title("🔍 शब्द-रूप सिद्धि यन्त्र")
    st.markdown("**ग्लास-बॉक्स (Glassbox)** तकनीक: हर वर्ण का विश्लेषण देखें।")

    with st.sidebar:
        stem = st.text_input("प्रातिपदिक (Stem)", value="राम")
        st.info("केवल 'अकारांत पुल्लिंग' (जैसे राम, देव) के लिए।")

    if stem:
        # Table Generation Logic (Simplified for brevity in view)
        pass

    # --- Inspector Section ---
    c1, c2, c3 = st.columns(3)
    with c1: sel_vib = st.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with c2: sel_vac = st.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    with c3:
        st.write("")
        st.write("")
        derive_btn = st.button("वर्ण-विच्छेद दिखाएं (Show Analysis)", type="primary")

    if derive_btn:
        logger = PrakriyaLogger()
        result = SubantaProcessor.derive_pada(stem, sel_vib, sel_vac, logger)

        st.markdown(f"### अंतिम रूप: <span class='big-sanskrit'>{result}</span>", unsafe_allow_html=True)
        st.divider()

        history = logger.get_history()
        for step in history:
            viccheda_html = ""
            if step['viccheda']:
                viccheda_html = f"""
                <div class="label-text">🔍 वर्ण-विश्लेषण (Atomic Tokenization):</div>
                <div class="viccheda-box">{step['viccheda']}</div>
                """

            st.markdown(f"""
            <div class="step-box">
                <div class="rule-id">📖 सूत्र: {step['rule']}</div>
                <div class="op-text">कार्य: {step['operation']}</div>
                {viccheda_html}
                <div style="margin-top:8px;">
                    <span class="label-text">परिणाम:</span> 
                    <span class="sanskrit-text">{step['result']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
