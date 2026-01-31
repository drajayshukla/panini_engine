import streamlit as st
import pandas as pd
import textwrap
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

# --- 1. पेज कॉन्फ़िगरेशन ---
st.set_page_config(
    page_title="शब्द-रूप सिद्धि यन्त्र",
    page_icon="🕉️",
    layout="wide"
)

# --- 2. CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    
    body { font-family: 'Noto Sans', sans-serif; }

    .step-card {
        background-color: white;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 10px;
        border-left: 5px solid #8e44ad;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .card-header {
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;
    }
    
    .rule-tag {
        background-color: #8e44ad; color: white; padding: 4px 12px; 
        border-radius: 15px; font-size: 0.85rem; font-weight: bold;
    }
    
    .auth-tag {
        font-size: 0.75rem; color: #888; font-weight: bold; text-transform: uppercase;
    }

    .operation-text {
        font-size: 1.1rem; font-weight: 700; color: #2c3e50; margin-bottom: 8px;
    }

    .varna-box {
        background-color: #f8f9fa; padding: 10px; border-radius: 6px; 
        border: 1px solid #eee; margin: 8px 0; line-height: 2.0;
    }
    
    .varna-token {
        display: inline-block; background: white; border: 1px solid #bdc3c7; 
        padding: 4px 8px; margin: 0 3px; border-radius: 4px; 
        color: #d35400; font-family: monospace; font-weight: bold; font-size: 1rem;
    }
    
    .plus-sep { color: #ccc; font-weight: bold; font-size: 1.2rem; }

    .result-row {
        margin-top: 10px; padding-top: 5px; border-top: 1px dashed #eee;
        display: flex; justify-content: space-between; align-items: center;
    }
    
    .res-sanskrit {
        font-family: 'Martel', serif; font-size: 1.5rem; font-weight: 800; color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. हेल्पर फंक्शन (CLEAN HTML GENERATOR) ---
def generate_card_html(step_index, step_data):
    rule = step_data['rule']
    operation = step_data['operation']
    result = step_data['result']
    viccheda = step_data['viccheda']
    source = step_data.get('source', 'Maharshi Pāṇini')
    
    viccheda_html = ""
    if viccheda:
        parts = viccheda.split(" + ")
        # टाइल्स बनाना
        token_spans = [f'<span class="varna-token">{p}</span>' for p in parts]
        # सेपरेटर जोड़ना
        separator = '<span class="plus-sep">+</span>'
        tokens_html = separator.join(token_spans)
        
        # HTML Block (No Indentation to prevent Code Block rendering)
        viccheda_html = f"""
<div style="font-size:0.8rem; color:#777; margin-bottom:4px;">🔍 वर्ण-विश्लेषण:</div>
<div class="varna-box">{tokens_html}</div>
"""

    # मुख्य कार्ड HTML (Use textwrap.dedent to strip indentation)
    raw_html = f"""
    <div class="step-card">
        <div class="card-header">
            <span class="rule-tag">📖 {rule}</span>
            <span class="auth-tag">— {source}</span>
        </div>
        <div class="operation-text">{operation}</div>
        {viccheda_html}
        <div class="result-row">
            <span style="color:#777; font-size:0.8rem;">चरण {step_index + 1}</span>
            <span class="res-sanskrit">{result}</span>
        </div>
    </div>
    """
    return textwrap.dedent(raw_html)

# --- 4. मुख्य ऐप लॉजिक ---
VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def main():
    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र")
    st.markdown("---")

    with st.sidebar:
        st.header("🎛️ इनपुट")
        stem = st.text_input("प्रातिपदिक", value="राम")
        st.caption("केवल अकारांत पुल्लिंग (Ram-like) के लिए।")

    if stem:
        with st.expander("📖 तालिका देखें (View Table)", expanded=True):
            table_data = []
            for v in range(1, 9):
                row = {"विभक्ति": VIBHAKTI_MAP[v]}
                for n in range(1, 4):
                    word = SubantaProcessor.derive_pada(stem, v, n, None)
                    row[VACANA_MAP[n]] = word
                table_data.append(row)
            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    st.markdown("### 🔬 सिद्धि प्रक्रिया (Glassbox)")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: v_sel = st.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with c2: n_sel = st.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    with c3: 
        st.write(""); st.write("")
        btn = st.button("🚀 सिद्धि करें", type="primary")

    if btn:
        logger = PrakriyaLogger()
        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger)
        st.success(f"सिद्ध पद: **{res}**")
        
        history = logger.get_history()
        for i, step in enumerate(history):
            # HTML Generate करें और Render करें
            st.markdown(generate_card_html(i, step), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
