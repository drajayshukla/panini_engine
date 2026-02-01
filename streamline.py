"""
FILE: restore_clean_ui.py
PURPOSE: Revert UI to single-page Declension Engine (Table + Derivation).
         Removes Reverse Analyzer to declutter the interface.
"""
import os
import sys

# ==============================================================================
# CLEAN UI CODE (No Tabs, Focus on Table & Derivation)
# ==============================================================================
CLEAN_UI_CODE = r'''import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="शब्द-रूप सिद्धि यन्त्र",
    page_icon="🕉️",
    layout="wide"
)

# --- 2. CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    
    body { font-family: 'Noto Sans', sans-serif; background-color: #f4f6f9; }

    .step-card {
        background-color: #ffffff; padding: 20px; margin-bottom: 20px;
        border-radius: 12px; border-left: 6px solid #8e44ad;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08); transition: transform 0.2s;
    }
    .step-card:hover { transform: translateY(-2px); }

    .card-header {
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #f0f0f0; padding-bottom: 10px; margin-bottom: 15px;
    }
    
    .rule-tag {
        background: linear-gradient(135deg, #8e44ad, #9b59b6); color: white;
        padding: 6px 14px; border-radius: 20px; font-size: 0.9rem; font-weight: bold;
        box-shadow: 0 2px 4px rgba(142, 68, 173, 0.3); text-decoration: none;
        display: inline-block;
    }
    
    .auth-tag {
        font-size: 0.75rem; color: #95a5a6; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.5px;
    }

    .operation-text { font-size: 1.2rem; font-weight: 700; color: #2c3e50; margin: 10px 0; }

    .varna-container {
        background-color: #f8f9fa; padding: 12px; border-radius: 8px;
        border: 1px solid #e9ecef; margin: 10px 0; display: flex; flex-wrap: wrap; gap: 8px;
    }
    
    .varna-tile {
        background-color: #fff; border: 1px solid #bdc3c7; border-bottom: 3px solid #bdc3c7;
        padding: 5px 10px; border-radius: 6px; color: #d35400;
        font-family: 'Courier New', monospace; font-weight: bold; font-size: 1.1rem;
        min-width: 30px; text-align: center;
    }
    
    .plus-sep { color: #bdc3c7; font-weight: bold; font-size: 1.2rem; }

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

# --- 3. HTML GENERATOR ---
def generate_card_html(step_index, step_data):
    rule_str = step_data['rule']
    op = step_data['operation']
    res = step_data['result']
    viccheda = step_data['viccheda']
    source = step_data.get('source', 'Maharshi Pāṇini')
    
    # Link Logic
    rule_html = f'<span class="rule-tag">📖 {rule_str}</span>'
    try:
        if rule_str and "." in rule_str:
            parts = rule_str.split()[0].split('.')
            if len(parts) == 3:
                c, p, s = parts
                link = f"https://ashtadhyayi.com/sutraani/{c}/{p}/{s}"
                rule_html = f'<a href="{link}" target="_blank" class="rule-tag" style="color:white;">📖 {rule_str} ↗</a>'
    except:
        pass

    # Varna Logic
    viccheda_html = ""
    if viccheda:
        parts = viccheda.split(" + ")
        tile_list = []
        for p in parts:
            tile_list.append(f'<div class="varna-tile">{p}</div>')
        tiles = '<div class="plus-sep">+</div>'.join(tile_list)
        
        viccheda_html = f"""
        <div style="font-size:0.85rem; color:#7f8c8d; margin-bottom:5px;">🔍 वर्ण-विश्लेषण (Atomic View):</div>
        <div class="varna-container">{tiles}</div>
        """

    html = f"""
    <div class="step-card">
        <div class="card-header">
            {rule_html}
            <span class="auth-tag">— {source}</span>
        </div>
        <div class="operation-text">{op}</div>
        {viccheda_html}
        <div class="result-row">
            <span class="step-num">चरण {step_index + 1}</span>
            <span class="res-sanskrit">{res}</span>
        </div>
    </div>
    """
    return html

# --- 4. MAIN LOGIC ---
VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def main():
    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र")
    st.markdown("---")

    with st.sidebar:
        st.header("🎛️ इनपुट (Input)")
        stem = st.text_input("प्रातिपदिक (Stem)", value="रमा")
        
        st.success("✅ **समर्थित शब्द (Supported):**")
        st.markdown("""
        1. **राम** (अकारांत पुंलिङ्ग)
        2. **हरि** (इकारांत पुंलिङ्ग - घि)
        3. **गुरु** (उकारांत पुंलिङ्ग - घि)
        4. **रमा** (आकारांत स्त्रीलिङ्ग) ✨
        """)
        
        st.info("ℹ️ अब 'टाप्' (आकारांत) और 'घि' (इ/उ) दोनों सिद्धियां उपलब्ध हैं।")

    # --- FULL TABLE VIEW ---
    if stem:
        st.subheader(f"📖 सम्पूर्ण शब्द-रूप सारिणी: **{stem}**")
        with st.expander("तालिका देखें (Click to Expand)", expanded=True):
            table_data = []
            # Calculate all forms silently
            for v in range(1, 9):
                row = {"विभक्ति": VIBHAKTI_MAP[v]}
                for n in range(1, 4):
                    try:
                        word = SubantaProcessor.derive_pada(stem, v, n, None)
                    except:
                        word = "Error"
                    row[VACANA_MAP[n]] = word
                table_data.append(row)
            
            # Show Table
            st.dataframe(
                pd.DataFrame(table_data), 
                use_container_width=True, 
                hide_index=True
            )

    st.markdown("---")
    st.header("🔬 ग्लास-बॉक्स सिद्धि (Step-by-Step Derivation)")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1: v_sel = st.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with col2: n_sel = st.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    with col3: 
        st.write(""); st.write("")
        btn = st.button("🚀 सिद्धि दिखाएं", type="primary", use_container_width=True)

    if btn:
        logger = PrakriyaLogger()
        final_res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger)
        
        st.success(f"सिद्ध पद: **{final_res}**")
        
        history = logger.get_history()
        for i, step in enumerate(history):
            st.markdown(generate_card_html(i, step), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
'''

with open("pages/1_🔍_Declension_Engine.py", "w", encoding="utf-8") as f:
    f.write(CLEAN_UI_CODE)

print("🚀 UI Restored to Clean Table Mode (Reverse Engineering Removed).")