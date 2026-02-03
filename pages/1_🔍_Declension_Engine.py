import streamlit as st
import sys, os
# PATH HACK
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि", page_icon="🕉️", layout="wide")

# --- CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    body { font-family: 'Noto Sans', sans-serif; }
    
    .step-card { 
        background-color: #ffffff; padding: 16px; margin-bottom: 12px; 
        border-radius: 8px; border: 1px solid #e0e0e0; border-left: 5px solid #2980b9;
    }
    .sutra-name { font-family: 'Martel', serif; font-weight: 800; font-size: 1.1rem; color: #2c3e50; }
    .op-text { font-size: 0.95rem; color: #555; margin-top: 5px; }
    .res-sanskrit { font-family: 'Martel', serif; font-size: 1.4rem; font-weight: bold; color: #8e44ad; }
    .auth-badge { background-color: #eafaf1; color: #27ae60; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; border: 1px solid #27ae60; }
    
    .viccheda-box {
        background-color: #fff3cd; padding: 8px; border-radius: 4px; 
        font-family: 'Courier New', monospace; font-weight: bold; color: #856404;
        margin-top: 5px; font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def generate_card(step_data):
    viccheda_html = ""
    if step_data.get('viccheda'):
        viccheda_html = f'<div class="viccheda-box">Padaccheda: {step_data["viccheda"]}</div>'

    return f"""
    <div class="step-card">
        <div>
            <span class="auth-badge">{step_data.get('source', 'पाणिनि')}</span>
            <span class="sutra-name">📖 {step_data.get('rule', '')} {step_data.get('name', '')}</span>
        </div>
        <div class="op-text">⚙️ {step_data.get('desc', '')}</div>
        {viccheda_html}
        <div style="text-align:right; margin-top:5px;">
            <span class="res-sanskrit">{step_data.get('result', '')}</span>
        </div>
    </div>
    """

def main():
    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र")
    st.markdown("### पाणिनीय प्रक्रिया (Glassbox Engine)")

    with st.sidebar:
        st.header("🎛️ इनपुट (Input)")
        stem = st.text_input("प्रातिपदिक (Stem)", value="राम")
        st.info("True Logic Active for: राम, हरि, गुरु")

    c1, c2 = st.columns(2)
    with c1: v_sel = st.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with c2: n_sel = st.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])

    if st.button("🚀 सिद्धि करें (Derive)", type="primary", use_container_width=True):
        logger = PrakriyaLogger()
        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger)

        tab1, tab2 = st.tabs(["📊 सिद्धि सारिणी", "📜 पूर्ण व्युत्पत्ति"])

        with tab1:
            st.success(f"सिद्ध पद: **{res}**")
            st.table(pd.DataFrame({
                "विवरण": ["प्रातिपदिक", "विभक्ति", "वचन", "अन्तिम रूप"],
                "मान": [stem, VIBHAKTI_MAP[v_sel], VACANA_MAP[n_sel], res]
            }))

        with tab2:
            history = logger.get_history()
            if not history:
                st.warning("No Pāṇinian steps recorded.")
            else:
                for step in history:
                    st.markdown(generate_card(step), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
