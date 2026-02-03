import streamlit as st
import sys
import os
# PATH HACK for Streamlit Cloud
sys.path.append(os.path.abspath('.'))

import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि", page_icon="🕉️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    body { font-family: 'Noto Sans', sans-serif; background-color: #fcfbf9; }
    .prakriya-container {
        background-color: white; padding: 30px; border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;
        font-size: 1.1rem; line-height: 1.8;
    }
    .step-arrow { color: #d35400; font-weight: bold; margin-right: 10px; }
    .rupam { font-family: 'Martel', serif; font-weight: 800; color: #2c3e50; font-size: 1.3rem; }
    .commentary { color: #555; font-family: 'Martel', serif; font-size: 1rem; color: #666; }
    .padaccheda-box {
        background-color: #fef9e7; border-left: 5px solid #f1c40f;
        padding: 15px; margin-bottom: 20px; font-family: 'Martel', serif; font-size: 1.4rem; color: #795548;
    }
</style>
""", unsafe_allow_html=True)

VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def render_step(step):
    if step['name'] == 'Padaccheda':
        return f'<div class="padaccheda-box">पदच्छेदः: <strong>{step["result"]}</strong></div>'
    return f'<div><span class="step-arrow">→</span><span class="rupam">{step["result"]}</span> <span class="commentary">[ {step["desc"]} ]</span></div>'

def main():
    st.title("🕉️ शब्द-रूप सिद्धि (Siddhānta Mode)")
    with st.sidebar:
        stem = st.text_input("प्रातिपदिक", value="राम")
    
    c1, c2, c3 = st.columns(3)
    v_sel = c1.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    n_sel = c2.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    
    if c3.button("🚀 View Prakriyā", type="primary"):
        logger = PrakriyaLogger()
        final_res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger)
        st.markdown('<div class="prakriya-container">', unsafe_allow_html=True)
        for step in logger.get_history():
            st.markdown(render_step(step), unsafe_allow_html=True)
        st.markdown(f'<hr><div style="text-align:center; color:#27ae60; font-size:1.4rem;">इति <strong>{final_res}</strong> सिद्धम् ॥</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
