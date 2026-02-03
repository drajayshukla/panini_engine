import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि", page_icon="🕉️", layout="wide")
st.markdown("""<style>.prakriya-container {background-color:white;padding:20px;border-radius:10px;border:1px solid #ddd;}.step-arrow{color:#d35400;font-weight:bold;margin-right:10px;}.rupam{font-weight:bold;color:#2c3e50;}.commentary{color:#666;font-size:0.95em;}</style>""", unsafe_allow_html=True)

def render_step(step):
    if step['name'] == 'Padaccheda':
        return f'<div style="background:#fff3cd;padding:10px;border-radius:5px;margin-bottom:15px;"><strong>Padaccheda:</strong> {step["result"]}</div>'
    return f'<div><span class="step-arrow">→</span><span class="rupam">{step["result"]}</span> <span class="commentary">[{step["desc"]}]</span></div>'

def main():
    st.title("🕉️ शब्द-रूप सिद्धि (Siddhānta Mode)")
    with st.sidebar:
        stem = st.text_input("प्रातिपदिक", value="राम")
    c1, c2, c3 = st.columns(3)
    v_sel = c1.selectbox("Vibhakti", [1,2,3,4,5,6,7,8])
    n_sel = c2.selectbox("Vacana", [1,2,3])
    if c3.button("🚀 View Prakriyā", type="primary"):
        logger = PrakriyaLogger()
        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger)
        st.markdown('<div class="prakriya-container">', unsafe_allow_html=True)
        for s in logger.get_history(): st.markdown(render_step(s), unsafe_allow_html=True)
        st.markdown(f'<hr><h3 style="text-align:center;color:green;">इति {res} सिद्धम् ॥</h3></div>', unsafe_allow_html=True)

if __name__ == "__main__": main()
