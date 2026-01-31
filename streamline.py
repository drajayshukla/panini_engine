"""
FILE: add_sutra_links.py
PURPOSE: Update UI to hyperlink every Sutra badge to Ashtadhyayi.com.
"""
import os
import sys

NEW_UI_CODE = '''import streamlit as st
import pandas as pd
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
    
    body { font-family: 'Noto Sans', sans-serif; background-color: #f4f6f9; }

    /* कार्ड */
    .step-card {
        background-color: #ffffff;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 12px;
        border-left: 6px solid #8e44ad;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transition: transform 0.2s;
    }
    .step-card:hover { transform: translateY(-2px); }

    /* हेडर */
    .card-header {
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #f0f0f0; padding-bottom: 10px; margin-bottom: 15px;
    }
    
    /* सूत्र लिंक स्टाइल */
    .sutra-link { text-decoration: none; }
    
    .rule-tag {
        background: linear-gradient(135deg, #8e44ad, #9b59b6);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(142, 68, 173, 0.3);
        transition: background 0.2s;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .rule-tag:hover {
        background: linear-gradient(135deg, #9b59b6, #8e44ad);
        box-shadow: 0 4px 8px rgba(142, 68, 173, 0.5);
    }
    
    .auth-tag {
        font-size: 0.75rem; color: #95a5a6; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.5px;
    }

    /* ऑपरेशन */
    .operation-text {
        font-size: 1.2rem; font-weight: 700; color: #2c3e50; margin: 10px 0;
    }

    /* वर्ण विच्छेद */
    .varna-container {
        background-color: #f8f9fa; padding: 12px; border-radius: 8px;
        border: 1px solid #e9ecef; margin: 10px 0;
        display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
    }
    .varna-tile {
        background-color: #fff; border: 1px solid #bdc3c7; border-bottom: 3px solid #bdc3c7;
        padding: 5px 10px; border-radius: 6px; color: #d35400;
        font-family: 'Courier New', monospace; font-weight: bold; font-size: 1.1rem;
        min-width: 30px; text-align: center;
    }
    .plus-sep { color: #bdc3c7; font-weight: bold; font-size: 1.2rem; }

    /* परिणाम */
    .result-row {
        margin-top: 15px; padding-top: 10px; border-top: 2px dashed #f0f2f5;
        display: flex; justify-content: space-between; align-items: center;
    }
    .step-num {
        font-size: 0.85rem; color: #7f8c8d; background-color: #ecf0f1;
        padding: 4px 8px; border-radius: 4px;
    }
    .res-sanskrit {
        font-family: 'Martel', serif; font-size: 1.8rem; font-weight: 800; color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. हेल्पर फंक्शन (HTML + LINK GENERATOR) ---
def generate_card_html(step_index, step_data):
    rule_str = step_data['rule']
    op = step_data['operation']
    res = step_data['result']
    viccheda = step_data['viccheda']
    source = step_data.get('source', 'Maharshi Pāṇini')
    
    # --- Link Construction Logic ---
    # rule_str example: "8.2.66 (ससजुषोः रुः)" -> needs parsing "8.2.66"
    try:
        # पहला भाग लें (ex: "8.2.66")
        rule_number = rule_str.split()[0]
        c, p, s = rule_number.split('.')
        # ashtadhyayi.com URL format: /sutraani/C/P/S
        link_url = f"https://ashtadhyayi.com/sutraani/{c}/{p}/{s}"
        
        # Clickable Badge HTML
        rule_html = (
            f'<a href="{link_url}" target="_blank" class="sutra-link">'
            f'<span class="rule-tag">📖 {rule_str} <span style="font-size:0.7em;">↗</span></span>'
            f'</a>'
        )
    except:
        # Fallback if rule number is weird (e.g. "Final")
        rule_html = f'<span class="rule-tag">📖 {rule_str}</span>'

    # --- Varna Viccheda HTML ---
    viccheda_html = ""
    if viccheda:
        parts = viccheda.split(" + ")
        tiles = "".join([f'<div class="varna-tile">{p}</div><div class="plus-sep">+</div>' for p in parts])
        if tiles: tiles = tiles[:-29] # Remove last separator
        viccheda_html = f'<div style="font-size:0.85rem; color:#7f8c8d; margin-bottom:5px;">🔍 वर्ण-विश्लेषण (Atomic View):</div><div class="varna-container">{tiles}</div>'

    # --- Full Card HTML (Flattened) ---
    html = (
        f'<div class="step-card">'
            f'<div class="card-header">'
                f'{rule_html}'
                f'<span class="auth-tag">— {source}</span>'
            f'</div>'
            f'<div class="operation-text">{op}</div>'
            f'{viccheda_html}'
            f'<div class="result-row">'
                f'<span class="step-num">चरण {step_index + 1}</span>'
                f'<span class="res-sanskrit">{res}</span>'
            f'</div>'
        f'</div>'
    )
    return html

# --- 4. मुख्य ऐप ---
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
            st.markdown(generate_card_html(i, step), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
'''

with open("pages/1_🔍_Declension_Engine.py", "w", encoding="utf-8") as f:
    f.write(NEW_UI_CODE)

print("🚀 Sutra Linking Active. Badges are now clickable to Ashtadhyayi.com!")