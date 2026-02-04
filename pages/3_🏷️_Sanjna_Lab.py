import streamlit as st
import sys
import os

sys.path.append(os.path.abspath('.'))
from shared.varnas import ad, join
from shared.anubandha import AnubandhaEngine

st.set_page_config(page_title="Sanjna Lab", page_icon="🏷️", layout="wide")

st.markdown("""
<style>
    .result-box { font-size: 2em; font-weight: bold; color: #2c3e50; }
    .tag-badge { 
        background-color: #e74c3c; 
        color: white; 
        padding: 5px 10px; 
        border-radius: 15px; 
        font-size: 0.9em; 
        margin-right: 5px; 
        font-weight: bold;
        display: inline-block;
    }
    .karya-box {
        background-color: #ecf0f1;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #3498db;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏷️ Sanjñā Lab (The Invisible Tags)")
st.markdown("### 1.3.9 Tasya Lopaḥ: The Body dies, the Soul (Tag) remains.")

# INPUT
c1, c2 = st.columns([2, 1])
with c1:
    raw_input = st.text_input("Upadeśa (Input)", value="ष्वुन्")
with c2:
    context = st.selectbox("Context", ["Pratyaya", "Dhatu", "Vibhakti"])

if st.button("Analyze Upadeśa"):
    # 1. PROCESS
    varnas = ad(raw_input)
    clean, trace, tags = AnubandhaEngine.process(varnas, context)
    final_form = join(clean)

    # 2. DISPLAY RESULTS
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.subheader("Physical Result (Drishya)")
        st.markdown(f'<div class="result-box">{final_form}</div>', unsafe_allow_html=True)
        st.caption("(What remains after Lopa)")

    with col_res2:
        st.subheader("Metaphysical Tags (Adrishya)")
        if tags:
            tag_html = ""
            for t in tags:
                tag_html += f'<span class="tag-badge">{t}</span>'
            st.markdown(tag_html, unsafe_allow_html=True)
        else:
            st.info("No Tags generated.")
            
    # 3. KARYA (Why do these tags matter?)
    st.subheader("🚀 Function of these Tags (Kārya)")
    
    # Knowledge Base of Effects
    karya_map = {
        "Kit": "1.1.5 Kkniti ca: Blocks Guna/Vriddhi.",
        "Nit": "7.2.115 Aco'ñniti: Causes Vriddhi of initial vowel.",
        "Ñit": "7.2.115 Aco'ñniti: Causes Vriddhi of initial vowel.",
        "Ṣit": "4.1.41 Ṣidgaurādibhyaśca: Adds feminine suffix Ṅīṣ (e.g. Nartakī).",
        "Pit": "3.1.4 Anudāttau suppitau: Suffix has Anudatta accent.",
        "Lit": "6.1.193 Liti: Accent on the stem-final.",
        "Cit": "6.1.163 Citaḥ: Accent on the suffix-final.",
        "Idit": "7.1.58 Idito num dhātoḥ: Inserts 'Num' (n) infix.",
    }
    
    found_karya = False
    for t in tags:
        clean_t = t.replace("it", "it") # normalize
        if t in karya_map:
            st.markdown(f'<div class="karya-box"><b>{t}:</b> {karya_map[t]}</div>', unsafe_allow_html=True)
            found_karya = True
            
    if not found_karya and tags:
        st.caption("No specific Karya hardcoded for these tags yet.")
        
    # 4. TRACE
    with st.expander("View Derivation Trace"):
        for t in trace:
            st.write(t)
