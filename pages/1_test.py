import streamlit as st
import sys
import os

# --- PATH HACK (CRITICAL for Streamlit Cloud) ---
# This allows the page to find the 'logic' and 'engine_main' modules
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि यन्त्र", page_icon="🕉️", layout="wide")

# --- Glassbox CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    body { font-family: 'Noto Sans', sans-serif; background-color: #f4f6f9; }
    
    .step-card { 
        background-color: #ffffff; padding: 18px 24px; margin-bottom: 16px; 
        border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
        border: 1px solid #e0e0e0; transition: all 0.2s ease-in-out;
    }
    .step-card:hover { transform: scale(1.01); box-shadow: 0 6px 16px rgba(0,0,0,0.08); }
    .border-meta { border-left: 8px solid #2980b9; }    /* Logic/Definitions */
    .border-action { border-left: 8px solid #8e44ad; } /* Phonetic Actions */
    
    .rule-badge {
        padding: 5px 10px; border-radius: 6px; font-weight: 800; font-size: 0.85rem;
        color: white; text-decoration: none; display: inline-block;
    }
    .badge-meta { background-color: #2980b9; }
    .badge-action { background-color: #8e44ad; }
    
    .auth-badge {
        padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 900;
        text-transform: uppercase; border: 1.5px solid; display: inline-block; 
        margin-right: 10px; letter-spacing: 0.8px;
    }
    .auth-panini { color: #27ae60; border-color: #27ae60; background-color: #eafaf1; }
    .auth-katyayana { color: #d35400; border-color: #d35400; background-color: #fcece0; }

    .res-sanskrit { 
        font-family: 'Martel', serif; font-size: 1.8rem; font-weight: 800; color: #2c3e50; 
    }
    .varna-tile { 
        background-color: #f8fafc; border: 1.5px solid #cbd5e1;
        padding: 4px 10px; border-radius: 6px; color: #d35400; 
        font-family: 'Courier New', monospace; font-weight: 900; font-size: 1rem; 
    }
</style>
""", unsafe_allow_html=True)

VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def get_style_meta(rule_num):
    if any(rule_num.startswith(x) for x in ["1.1", "1.2", "1.4", "3.1"]):
        return "border-meta", "badge-meta"
    return "border-action", "badge-action"

def generate_card_html(index, data):
    rule = data.get('rule', '0.0.0')
    name = data.get('name', 'Sūtra')
    op = data.get('desc', 'Processing') # Fixed key match with Logger
    res = data.get('result', '')
    source = data.get('source', 'Pāṇini').upper()

    border_class, badge_class = get_style_meta(rule)
    auth_class = "auth-panini" if "PANINI" in source else "auth-katyayana"
    link = f"https://ashtadhyayi.com/sutraani/{rule.replace('.', '/')}" if "." in rule else "#"

    return f"""
    <div class="step-card {border_class}">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span class="auth-badge {auth_class}">{source}</span>
                <a href="{link}" target="_blank" class="rule-badge {badge_class}">📖 {rule}</a>
                <span style="font-family:'Martel'; font-weight:800; font-size:1.2rem; margin-left:10px;">{name}</span>
                <div style="margin-top:10px; color:#555; font-weight:500;">⚙️ {op}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.7rem; color:#94a3b8; font-weight:900;">STEP {index+1}</div>
                <div class="res-sanskrit">{res}</div>
            </div>
        </div>
    </div>
    """

def main():
    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र (Test Mode)")
    st.markdown("### Glassbox AI: Pāṇinian Morphological Derivation")

    with st.sidebar:
        st.header("🎛️ Input Parameters")
        stem = st.text_input("प्रातिपदिक (Stem)", value="राम")
        force_p = st.checkbox("Force Pratipadika", value=True)
        st.info("Pillar R17: Validating output against Lakṣya")
    
    col1, col2 = st.columns(2)
    with col1: v_sel = st.selectbox("Vibhakti", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with col2: n_sel = st.selectbox("Vacana", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])

    if st.button("🚀 Derive Prakriyā", type="primary", use_container_width=True):
        logger = PrakriyaLogger()
        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger)
        
        tab1, tab2 = st.tabs(["📊 Summary View", "📜 Deep Vyutpatti"])
        
        with tab1:
            st.success(f"Final Form: **{res}**")
            st.table(pd.DataFrame({
                "Property": ["Stem", "Vibhakti", "Vacana", "Result"],
                "Value": [stem, VIBHAKTI_MAP[v_sel], VACANA_MAP[n_sel], res]
            }))
        
        with tab2:
            st.markdown("### Step-by-Step Derivation")
            for i, step in enumerate(logger.get_history()):
                st.markdown(generate_card_html(i, step), unsafe_allow_html=True)

    with st.expander("📚 View Full Declension Table"):
        if st.button("Generate Full Table"):
            rows = []
            for v in range(1, 9):
                row = {"Vibhakti": VIBHAKTI_MAP[v]}
                for n in range(1, 4):
                    row[VACANA_MAP[n]] = SubantaProcessor.derive_pada(stem, v, n, None)
                rows.append(row)
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
