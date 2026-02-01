"""
FILE: fix_ui_html_and_tags.py
PURPOSE:
  1. Fix broken HTML structure in UI cards (closing div tags).
  2. Add 'Authority Badges' (Panini, Katyayana, etc.) with color coding.
"""
import os

UI_CODE = r'''import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि यन्त्र", page_icon="🕉️", layout="wide")

# --- CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    body { font-family: 'Noto Sans', sans-serif; background-color: #f4f6f9; }
    
    /* Card Base */
    .step-card { 
        background-color: #ffffff; padding: 16px 20px; margin-bottom: 16px; 
        border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); 
        border: 1px solid #e0e0e0;
        transition: all 0.2s ease-in-out;
    }
    .step-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }

    /* Border Colors by Type */
    .border-meta { border-left: 6px solid #2980b9; }   /* Blue: Definitions */
    .border-action { border-left: 6px solid #8e44ad; } /* Purple: Transformations */
    
    /* Rule Badge (The Number) */
    .rule-badge {
        padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 0.85rem;
        display: inline-block; margin-right: 8px; color: white; vertical-align: middle;
    }
    .badge-meta { background-color: #2980b9; }
    .badge-action { background-color: #8e44ad; }

    /* Authority Badge (The Rishi) */
    .auth-badge {
        padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 700;
        text-transform: uppercase; border: 1px solid; display: inline-block; 
        margin-right: 8px; vertical-align: middle; letter-spacing: 0.5px;
    }
    
    /* Authority Colors */
    .auth-panini { color: #27ae60; border-color: #27ae60; background-color: #eafaf1; } /* Green */
    .auth-katyayana { color: #d35400; border-color: #d35400; background-color: #fcece0; } /* Orange */
    .auth-patanjali { color: #c0392b; border-color: #c0392b; background-color: #f9ebeb; } /* Red */
    .auth-other { color: #7f8c8d; border-color: #7f8c8d; background-color: #f4f6f7; } /* Grey */

    /* Typography */
    .sutra-name {
        font-family: 'Martel', serif; font-weight: 800; font-size: 1.2rem; color: #2c3e50;
        vertical-align: middle;
    }
    .op-text {
        font-size: 0.95rem; color: #555; margin-top: 8px; font-weight: 500; display: flex; align-items: center;
    }
    .res-sanskrit { 
        font-family: 'Martel', serif; font-size: 1.6rem; font-weight: 800; color: #2c3e50; 
    }
    
    /* Varna Tiles */
    .varna-container { margin-top: 8px; display: flex; flex-wrap: wrap; gap: 4px; }
    .varna-tile { 
        background-color: #fdfdfd; border: 1px solid #d1d5db; border-bottom: 2px solid #9ca3af;
        padding: 2px 8px; border-radius: 4px; color: #d35400; 
        font-family: 'Courier New', monospace; font-weight: bold; font-size: 0.95rem; 
    }
    
    /* Step Counter */
    .step-num { font-size: 0.7rem; color: #95a5a6; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def get_auth_class(source_text):
    """Returns CSS class based on Authority Name."""
    s = source_text.lower()
    if "panini" in s or "pāṇini" in s: return "auth-panini"
    if "katyayana" in s or "vartika" in s: return "auth-katyayana"
    if "patanjali" in s or "bhashya" in s: return "auth-patanjali"
    return "auth-other"

def get_card_style(rule_num):
    if rule_num.startswith("1.2") or rule_num.startswith("1.4") or \
       rule_num.startswith("3.1") or rule_num.startswith("4.1.1"):
        return "border-meta", "badge-meta"
    return "border-action", "badge-action"

def generate_card_html(step_index, step_data):
    rule_full = step_data['rule']
    op = step_data['operation']
    res = step_data['result']
    viccheda = step_data['viccheda']
    source = step_data.get('source', 'Unknown')
    vartika = step_data.get('vartika_html', '')
    
    # Split Number and Name
    if " " in rule_full:
        parts = rule_full.split(" ", 1)
        r_num = parts[0]
        r_name = parts[1]
    else:
        r_num = rule_full
        r_name = ""

    # Determine Styles
    border_class, badge_class = get_card_style(r_num)
    auth_class = get_auth_class(source)

    # Viccheda Tiles
    viccheda_html = ""
    if viccheda:
        parts = viccheda.split(" + ")
        tiles = "".join([f'<div class="varna-tile">{p}</div>' for p in parts])
        viccheda_html = f'<div class="varna-container">{tiles}</div>'

    # Link
    link = "#"
    if "." in r_num:
        try:
            c, p, s = r_num.split('.')
            link = f"https://ashtadhyayi.com/sutraani/{c}/{p}/{s}"
        except: pass

    # --- HTML STRUCTURE (FIXED) ---
    return f"""
    <div class="step-card {border_class}">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div style="flex-grow: 1;">
                <div style="margin-bottom: 6px;">
                    <span class="auth-badge {auth_class}">{source}</span>
                    <a href="{link}" target="_blank" style="text-decoration:none;">
                        <span class="rule-badge {badge_class}">📖 {r_num}</span>
                    </a>
                    <span class="sutra-name">{r_name}</span>
                </div>
                
                {vartika}
                
                <div class="op-text">
                    <span style="margin-right:6px;">⚙️</span> {op}
                </div>
                
                {viccheda_html}
            </div>
            
            <div style="text-align:right; min-width: 100px; margin-left: 15px;">
                <div class="step-num">STEP {step_index + 1}</div>
                <div class="res-sanskrit">{res}</div>
            </div>
        </div>
    </div>
    """

def main():
    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र")
    st.markdown("### Paninian Derivation Engine (Glassbox AI)")
    
    with st.sidebar:
        st.header("🎛️ इनपुट (Input)")
        stem = st.text_input("प्रातिपदिक (Stem)", value="राम")
        
        force_p = st.checkbox("Force Pratipadika", value=False, 
                              help="Enable to bypass initial dictionary checks.")
        
        st.success("✅ **Supported:** Ram, Hari, Guru, Sarva, etc.")
        st.markdown("---")
        st.markdown("**Legend:**")
        st.markdown('<span class="auth-badge auth-panini">PANINI</span> Sutra', unsafe_allow_html=True)
        st.markdown('<span class="auth-badge auth-katyayana">KATYAYANA</span> Vartika', unsafe_allow_html=True)

    # Main Action Area
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: v_sel = st.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with c2: n_sel = st.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    with c3: 
        st.write(""); st.write("")
        btn = st.button("🚀 सिद्धि करें (Derive)", type="primary", use_container_width=True)

    if btn:
        logger = PrakriyaLogger()
        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger, force_p)
        
        st.success(f"सिद्ध पद: **{res}**")
        
        # Display Cards
        for i, step in enumerate(logger.get_history()):
            st.markdown(generate_card_html(i, step), unsafe_allow_html=True)

    # Full Table Expansion
    if stem:
        with st.expander(f"📚 {stem} - सम्पूर्ण रूप सारिणी (Full Table)", expanded=False):
            data = []
            for v in range(1, 9):
                row = {"विभक्ति": VIBHAKTI_MAP[v]}
                for n in range(1, 4):
                    try: w = SubantaProcessor.derive_pada(stem, v, n, None, force_p)
                    except: w = "Error"
                    row[VACANA_MAP[n]] = w
                data.append(row)
            st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

if __name__ == "__main__":
    main()
'''

with open("pages/1_🔍_Declension_Engine.py", "w", encoding="utf-8") as f:
    f.write(UI_CODE)

print("🚀 UI HTML Fixed & Authority Tags (Panini/Katyayana) added.")
# No need to run master_runner unless you want to check tests again.
# Just launch streamlit to see the UI.
import subprocess
import sys
# subprocess.run([sys.executable, "master_runner.py"])