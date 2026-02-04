"""
FILE: pages/3_🏷️_Sanjna_Lab.py
PURPOSE: Interactive Sanjna Lab with Integrated Siddhānta Knowledge Base.
"""
import streamlit as st
import sys
import os

# Path Hack for Modular Imports
sys.path.append(os.path.abspath('.'))
from shared.varnas import ad, join
from shared.anubandha import AnubandhaEngine
from shared.knowledge_base import PaniniKnowledgeBase

st.set_page_config(page_title="Sanjna Lab", page_icon="🏷️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .result-box { font-size: 2em; font-weight: bold; color: #2c3e50; }
    .tag-badge { 
        background-color: #8e44ad; 
        color: white; 
        padding: 5px 12px; 
        border-radius: 20px; 
        font-size: 1.1em; 
        margin-right: 8px; 
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .karya-card {
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        border-left: 6px solid #27ae60;
        margin-top: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .karya-title { font-weight: bold; color: #2c3e50; font-size: 1.1em; }
    .karya-sutra { color: #7f8c8d; font-size: 0.9em; font-family: monospace; }
    .sanskrit-text { font-family: 'Sanskrit 2003', 'Noto Sans Devanagari', sans-serif; line-height: 1.6; font-size: 1.05em; }
    .dev-label { color: #f1c40f; margin-right: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("🏷️ Sanjñā Lab (The Invisible Tags)")
st.markdown("### 1.3.9 Tasya Lopaḥ: The Body dies, the Soul (Tag) remains.")

# --- INPUT SECTION ---
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    raw_input = st.text_input("Upadeśa (Input)", value="ष्वुन्", help="Try: डुकृञ्, ष्फ, जस्, शप्")
with c2:
    context = st.selectbox("Context", ["Pratyaya", "Dhatu", "Vibhakti"])
with c3:
    st.write("") # Spacer
    run_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)

if run_btn:
    st.divider()
    
    # 1. PROCESS LOGIC
    varnas = ad(raw_input)
    clean, trace, tags = AnubandhaEngine.process(varnas, context)
    final_form = join(clean)

    # 2. DISPLAY VISUALS
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("👁️ Drishya (Visible Form)")
        st.markdown(f'<div class="result-box">{final_form}</div>', unsafe_allow_html=True)
        st.info("This is the 'Body' used in Sandhi/Declension.")

    with col_right:
        st.subheader("👻 Adrishya (Meta-Tags)")
        if tags:
            tag_html = ""
            for t in tags:
                # Get Devanagari Label from Knowledge Base
                dev_label, _, _ = PaniniKnowledgeBase.get_karya(t)
                tag_html += f'<span class="tag-badge"><span class="dev-label">{dev_label}</span>{t}</span>'
            st.markdown(tag_html, unsafe_allow_html=True)
        else:
            st.warning("No It-Tags found.")

    # 3. KARYA MAPPING (From Engine)
    st.subheader("🚀 Kārya (Grammatical Effects)")
    if tags:
        found = False
        for tag in tags:
            # RETRIEVE DATA FROM ENGINE LAYER
            dev_label, sutra, desc = PaniniKnowledgeBase.get_karya(tag)
            
            if sutra != "Unknown":
                found = True
                st.markdown(f"""
                <div class="karya-card">
                    <span class="tag-badge" style="font-size:0.8em;">{dev_label} ({tag})</span>
                    <span class="karya-title">{desc}</span><br>
                    <span class="karya-sutra">📖 {sutra}</span>
                </div>
                """, unsafe_allow_html=True)
        
        if not found:
            st.caption("Tags detected, but no specific effect hardcoded in Engine DB.")
    else:
        st.caption("No tags = No special grammatical triggers.")

    # 4. TRACE LOG
    with st.expander("📜 View Derivation Logic (Prakriyā)"):
        for step in trace:
            if "SAVED" in step: st.success(step)
            elif "disappears" in step: st.error(step)
            else: st.write(step)

# --- SHASTRA REFERENCE (FROM ENGINE) ---
# --- SHASTRA REFERENCE (FROM ENGINE) ---
st.markdown("---")
with st.expander("📚 Siddhānta Knowledge Base (Theory & Rules)", expanded=False):
    st.markdown("### 📖 शास्त्र-विवरणम् (Theory)")
    
    # Updated Dynamic Tabs to include 1.3.7 (Cuṭū) and 1.3.8 (Laśakvataddhite)
    tabs = st.tabs([
        "1.3.2 Anunāsika", 
        "1.3.3 Halantyam", 
        "1.3.5 Ādi Rules", 
        "1.3.6 Ṣaḥ Pratyayasya", 
        "1.3.7 Cuṭū", 
        "1.3.8 Laśakvataddhite",
        "1.4.104 Vibhakti"
    ])

    # Mapping engine-level text to the UI tabs
    # We use .get() to prevent crashes if a key is missing in shared/knowledge_base.py
    with tabs[0]: 
        st.markdown(PaniniKnowledgeBase.SIDDHANTA_TEXTS.get("1.3.2", "Data Missing"), unsafe_allow_html=True)
    
    with tabs[1]: 
        st.markdown(PaniniKnowledgeBase.SIDDHANTA_TEXTS.get("1.3.3", "Data Missing"), unsafe_allow_html=True)
    
    with tabs[2]: 
        st.markdown(PaniniKnowledgeBase.SIDDHANTA_TEXTS.get("1.3.5", "Data Missing"), unsafe_allow_html=True)
    
    with tabs[3]: 
        st.markdown(PaniniKnowledgeBase.SIDDHANTA_TEXTS.get("1.3.6", "Data Missing"), unsafe_allow_html=True)
    
    with tabs[4]: 
        st.markdown(PaniniKnowledgeBase.SIDDHANTA_TEXTS.get("1.3.7", "Data Missing"), unsafe_allow_html=True)
    
    with tabs[5]: 
        st.markdown(PaniniKnowledgeBase.SIDDHANTA_TEXTS.get("1.3.8", "Data Missing"), unsafe_allow_html=True)
    
    with tabs[6]: 
        st.markdown(PaniniKnowledgeBase.SIDDHANTA_TEXTS.get("1.4.104", "Data Missing"), unsafe_allow_html=True)

st.caption("Architecture Note: All text content is managed via shared/knowledge_base.py")