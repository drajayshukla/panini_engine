import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि यन्त्र", page_icon="🕉️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    body { font-family: 'Noto Sans', sans-serif; background-color: #f4f6f9; }
    
    .step-card { 
        background-color: #ffffff; padding: 20px; margin-bottom: 20px; 
        border-radius: 12px; border-left: 6px solid #8e44ad; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.08); 
    }
    
    .rule-badge {
        background-color: #8e44ad; color: white; padding: 4px 10px; 
        border-radius: 6px; font-weight: bold; font-size: 0.85rem;
        display: inline-block; margin-right: 8px;
    }
    
    .sutra-name {
        font-family: 'Martel', serif; font-weight: 800; font-size: 1.1rem; color: #2c3e50;
    }
    
    .op-text {
        font-size: 0.95rem; color: #7f8c8d; margin-top: 4px; font-style: italic;
    }

    .res-sanskrit { 
        font-family: 'Martel', serif; font-size: 1.8rem; font-weight: 800; color: #2c3e50; 
    }
    
    .varna-tile { 
        background-color: #f8f9fa; border: 1px solid #dee2e6; 
        padding: 2px 8px; border-radius: 4px; color: #e67e22; 
        font-family: 'Courier New', monospace; font-weight: bold; font-size: 1rem; 
        display:inline-block; margin:2px;
    }
</style>
""", unsafe_allow_html=True)

VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def generate_card_html(step_index, step_data):
    rule_full = step_data['rule']
    op = step_data['operation']
    res = step_data['result']
    viccheda = step_data['viccheda']
    vartika = step_data.get('vartika_html', '')
    
    # Split Number and Name if possible
    if " " in rule_full:
        parts = rule_full.split(" ", 1)
        r_num = parts[0]
        r_name = parts[1]
    else:
        r_num = rule_full
        r_name = ""

    # Viccheda Tiles
    viccheda_html = ""
    if viccheda:
        parts = viccheda.split(" + ")
        tiles = "".join([f'<div class="varna-tile">{p}</div>' for p in parts])
        viccheda_html = f"<div style='margin-top:8px;'>{tiles}</div>"

    # Link to Ashtadhyayi.com
    link = "#"
    if "." in r_num:
        try:
            c, p, s = r_num.split('.')
            link = f"https://ashtadhyayi.com/sutraani/{c}/{p}/{s}"
        except: pass

    return f"""
    <div class="step-card">
        <div style="display:flex; align-items:center; flex-wrap:wrap;">
            <a href="{link}" target="_blank" style="text-decoration:none;">
                <span class="rule-badge">📖 {r_num}</span>
            </a>
            <span class="sutra-name">{r_name}</span>
        </div>
        
        {vartika}
        
        <div class="op-text">🛠️ {op}</div>
        
        {viccheda_html}
        
        <div style="margin-top:15px; border-top:1px dashed #eee; padding-top:10px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.8rem; color:#bdc3c7;">STEP {step_index + 1}</span>
            <span class="res-sanskrit">{res}</span>
        </div>
    </div>
    """

def main():
    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र")
    
    with st.sidebar:
        st.header("🎛️ इनपुट (Input)")
        stem = st.text_input("प्रातिपदिक (Stem)", value="राम")
        force_p = st.checkbox("Force Pratipadika (Override Rules)", value=False)
        st.info("✅ **समर्थित:** राम, हरि, गुरु, रमा, इ, उ, तितउ")

    if stem:
        with st.expander(f"📖 {stem} - सम्पूर्ण सारिणी", expanded=True):
            data = []
            for v in range(1, 9):
                row = {"विभक्ति": VIBHAKTI_MAP[v]}
                for n in range(1, 4):
                    try: w = SubantaProcessor.derive_pada(stem, v, n, None, force_p)
                    except: w = "Error"
                    row[VACANA_MAP[n]] = w
                data.append(row)
            st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: v_sel = st.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with c2: n_sel = st.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    with c3: 
        st.write(""); st.write("")
        btn = st.button("🚀 सिद्धि करें", type="primary", use_container_width=True)

    if btn:
        logger = PrakriyaLogger()
        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger, force_p)
        st.success(f"सिद्ध पद: **{res}**")
        for i, step in enumerate(logger.get_history()):
            st.markdown(generate_card_html(i, step), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
