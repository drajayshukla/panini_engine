import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि", page_icon="🕉️", layout="wide")

# --- CSS Styling (Devanagari Font Optimization) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    body { font-family: 'Noto Sans', sans-serif; }
    .step-card { 
        background-color: #ffffff; padding: 16px; margin-bottom: 12px; 
        border-radius: 8px; border: 1px solid #e0e0e0; border-left: 5px solid #2980b9;
    }
    .sutra-name { font-family: 'Martel', serif; font-weight: 800; font-size: 1.2rem; color: #2c3e50; }
    .op-text { font-size: 1rem; color: #555; }
    .res-sanskrit { font-family: 'Martel', serif; font-size: 1.5rem; font-weight: bold; color: #8e44ad; }
    .auth-badge { background-color: #eafaf1; color: #27ae60; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; border: 1px solid #27ae60; }
</style>
""", unsafe_allow_html=True)

VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def generate_card(step_index, step_data):
    return f"""
    <div class="step-card">
        <div>
            <span class="auth-badge">{step_data.get('source', 'पाणिनि')}</span>
            <span class="sutra-name">📖 {step_data['rule']} {step_data['name']}</span>
        </div>
        <div class="op-text">⚙️ {step_data['desc']}</div>
        <div style="text-align:right; margin-top:5px;">
            <span class="res-sanskrit">{step_data['result']}</span>
        </div>
    </div>
    """

def main():
    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र")
    st.markdown("### पाणिनीय प्रक्रिया (Glassbox Engine)")

    with st.sidebar:
        st.header("🎛️ इनपुट (Input)")
        stem = st.text_input("प्रातिपदिक (Stem)", value="राम")
        force_p = st.checkbox("प्रातिपदिक मान लें (Force)", value=False)
        st.success("✅ समर्थित: राम, हरि, गुरु, रमा, सर्व")

    c1, c2, c3 = st.columns(3)
    with c1: v_sel = st.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with c2: n_sel = st.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    with c3: 
        st.write(""); st.write("")
        btn = st.button("🚀 सिद्धि करें (Derive)", type="primary", use_container_width=True)

    if btn:
        logger = PrakriyaLogger()
        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger, force_p)

        st.success(f"सिद्ध पद: **{res}**")
        for i, step in enumerate(logger.get_history()):
            st.markdown(generate_card(i, step), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
