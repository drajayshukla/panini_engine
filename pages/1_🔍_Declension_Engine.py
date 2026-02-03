import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि", page_icon="🕉️", layout="wide")
st.markdown("""<style>.step-card {background-color:#ffffff;padding:16px;margin-bottom:12px;border-radius:8px;border-left:5px solid #2980b9;box-shadow:0 2px 5px rgba(0,0,0,0.05);} .viccheda-box {background:#fff3cd;padding:8px;border-radius:4px;font-family:'Courier New';font-weight:bold;color:#856404;margin-top:5px;}</style>""", unsafe_allow_html=True)

def generate_card(step):
    viccheda_html = f'<div class="viccheda-box">Padaccheda: {step["viccheda"]}</div>' if step.get('viccheda') else ""
    return f"""<div class="step-card"><b>📖 {step["rule"]} {step["name"]}</b><br>⚙️ {step["desc"]}{viccheda_html}<div style="text-align:right;font-size:1.4em;font-weight:bold;color:#8e44ad;">{step["result"]}</div></div>"""

def main():
    st.title("🕉️ शब्द-रूप सिद्धि (Siddhānta Mode)")
    with st.sidebar:
        stem = st.text_input("प्रातिपदिक", value="राम")
    c1,c2 = st.columns(2)
    v_sel = c1.selectbox("विभक्ति", range(1,9))
    n_sel = c2.selectbox("वचन", range(1,4))
    if st.button("🚀 सिद्धि करें"):
        logger = PrakriyaLogger()
        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger)
        st.success(f"Final: **{res}**")
        for step in logger.get_history(): st.markdown(generate_card(step), unsafe_allow_html=True)
if __name__ == "__main__": main()
