import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor
from logic.reverse_analyzer import ReverseAnalyzer

# --- CONFIG ---
st.set_page_config(page_title="Pāṇinian Engine", page_icon="🕉️", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    body { font-family: 'Noto Sans', sans-serif; background-color: #f4f6f9; }
    .step-card { background: white; padding: 15px; margin-bottom: 15px; border-radius: 10px; border-left: 5px solid #8e44ad; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .rev-card { background: #fffcf0; border-left: 5px solid #d35400; } /* Orange for Reverse */
    .rule-tag { background: #8e44ad; color: white; padding: 4px 10px; border-radius: 15px; font-weight: bold; font-size: 0.85rem; }
    .rev-tag { background: #d35400; }
    .sanskrit-big { font-family: 'Martel', serif; font-size: 1.6rem; font-weight: 800; color: #2c3e50; }
    .meta-box { background: #e8f6f3; padding: 10px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #d1f2eb; }
</style>
""", unsafe_allow_html=True)

# --- HELPER: CARD GEN ---
def render_history(history, is_reverse=False):
    # If reverse, we iterate backwards
    steps = reversed(history) if is_reverse else history
    
    for i, step in enumerate(steps):
        rule = step['rule']
        op = step['operation']
        res = step['result']
        
        # Style variations
        card_class = "step-card rev-card" if is_reverse else "step-card"
        tag_class = "rule-tag rev-tag" if is_reverse else "rule-tag"
        arrow = "↑" if is_reverse else "↓"
        step_label = f"Step {len(history) - i}" if is_reverse else f"Step {i + 1}"
        
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex; justify-content:space-between;">
                <span class="{tag_class}">📖 {rule}</span>
                <span style="color:#888; font-weight:bold;">{step_label}</span>
            </div>
            <div style="font-size:1.1rem; font-weight:bold; margin:8px 0;">{op}</div>
            <div style="margin-top:10px; border-top:1px dashed #ccc; padding-top:5px; display:flex; justify-content:space-between;">
                <span style="color:#555;">State: <span class="sanskrit-big">{res}</span></span>
                <span style="font-size:1.5rem; color:#ccc;">{arrow}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN ---
def main():
    st.title("🕉️ Pāṇinian Engine: Dual Mode")
    
    tab1, tab2 = st.tabs(["🚀 सिद्धि (Forward)", "🔄 विग्रह (Reverse)"])

    # === TAB 1: FORWARD ===
    with tab1:
        st.header("Stem + Suffix → Word")
        c1, c2, c3 = st.columns(3)
        stem = c1.text_input("Pratipadikam", "रमा")
        vib = c2.number_input("Vibhakti", 1, 8, 6)
        vac = c3.number_input("Vacana", 1, 3, 1)
        
        if st.button("Derive (सिद्धि)"):
            logger = PrakriyaLogger()
            res = SubantaProcessor.derive_pada(stem, vib, vac, logger)
            st.success(f"Final Form: **{res}**")
            render_history(logger.get_history(), is_reverse=False)

    # === TAB 2: REVERSE ===
    with tab2:
        st.header("Word → Stem + Suffix + Logic")
        st.info("Supported: राम, हरि, गुरु, रमा")
        
        target = st.text_input("Enter Sanskrit Word (e.g., रमायाः, हरये, गुरवे)", "रमायाः")
        
        if st.button("Analyze (विग्रह)"):
            matches = ReverseAnalyzer.analyze_word(target)
            
            if not matches:
                st.error("No match found in current supported database.")
            else:
                st.success(f"Found {len(matches)} valid derivation(s)!")
                
                for idx, m in enumerate(matches):
                    with st.expander(f"Match #{idx+1}: {m['stem']} (Vibhakti {m['vibhakti']}, Vacana {m['vacana']})", expanded=True):
                        # Metadata
                        st.markdown(f"""
                        <div class="meta-box">
                            <div><b>प्रातिपदिक (Stem):</b> {m['stem']}</div>
                            <div><b>प्रत्यय (Suffix):</b> {m['pratyaya']}</div>
                            <div><b>स्थान (Position):</b> Vibhakti {m['vibhakti']}, Vacana {m['vacana']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Reverse History
                        st.markdown("### ⏳ Reverse Trace (विपरीत क्रम)")
                        render_history(m['history'], is_reverse=True)

if __name__ == "__main__":
    main()
