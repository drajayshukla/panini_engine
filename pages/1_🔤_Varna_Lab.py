import streamlit as st
import sys
import os
import pandas as pd

# --- PATH HACK ---
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.varnas import ad, join

st.set_page_config(page_title="Varna Lab", page_icon="🔤", layout="wide")

# --- STYLING ---
st.markdown("""
<style>
    .varna-box { 
        display: inline-block; 
        padding: 8px 16px; 
        margin: 5px; 
        border-radius: 8px; 
        font-weight: bold; 
        font-size: 1.2em;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .v-swara { background-color: #e3f2fd; color: #1565c0; border: 1px solid #1565c0; } /* Vowels */
    .v-vyanjana { background-color: #ffebee; color: #c62828; border: 1px solid #c62828; } /* Consonants */
    .v-yoga { background-color: #fff3e0; color: #ef6c00; border: 1px solid #ef6c00; } /* Ayogavaha */
    .meta-text { font-size: 0.6em; display: block; color: #555; font-weight: normal;}
</style>
""", unsafe_allow_html=True)

st.title("🔤 Varna Lab (Phonetic Engine)")
st.caption("The Atomic Foundation: Viccheda (Analysis) & Samyoga (Synthesis)")

# --- HELPER: STHANA MAP ---
def get_sthana_info(char):
    # Simplified Sthana Map for Display
    base = char.replace('्', '').replace('ँ', '').replace('ः', '').replace('ं', '')
    if not base: return "—"
    
    map_data = {
        "कण्ठ": "अआकखगघङह",
        "तालु": "इईचछजझञयश",
        "मूर्धा": "ऋॠटठडढणरष",
        "दन्त": "ऌतथदधनलस",
        "ओष्ठ": "उऊपफबभम",
        "नासिका": "ङञणनम", # Nasals also belong to others, strictly speaking
        "कण्ठतालु": "एऐ",
        "कण्ठोष्ठ": "ओऔ",
        "दन्तोष्ठ": "व"
    }
    
    for place, chars in map_data.items():
        if base in chars: return place
    
    if char == 'ः': return "कण्ठ"
    if char == 'ं': return "नासिका"
    return "Unknown"

# --- INPUT ---
c1, c2 = st.columns([3, 1])
with c1:
    text_input = st.text_input("Enter Sanskrit Text (Devanagari):", value="रामः सुँ")
with c2:
    st.write("") # Spacer
    analyze = st.button("🔬 Analyze", type="primary", use_container_width=True)

if text_input:
    st.divider()
    
    # 1. ATOMIC DECOMPOSITION
    varnas = ad(text_input)
    
    # METRICS
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total Atoms (Varnas)", len(varnas))
    col_m2.metric("Vowels (Ac)", sum(1 for v in varnas if v.is_vowel))
    col_m3.metric("Consonants (Hal)", sum(1 for v in varnas if v.is_consonant))

    # 2. VISUALIZATION
    st.subheader("1. Varna-Viccheda (Atomic Split)")
    
    html_out = ""
    data_rows = []
    
    for v in varnas:
        # Determine Style
        css_class = "v-vyanjana"
        type_lbl = "Consonant"
        if v.is_vowel: 
            css_class = "v-swara"
            type_lbl = "Vowel"
        elif v.is_ayogavaha:
            css_class = "v-yoga"
            type_lbl = "Ayogavaha"
            
        sthana = get_sthana_info(v.char)
            
        # Build Card HTML
        html_out += f"""
        <div class="varna-box {css_class}">
            {v.char}
            <span class="meta-text">{sthana}</span>
        </div>
        """
        
        # Build Data Row for Table
        data_rows.append({
            "Varna": v.char,
            "Type": type_lbl,
            "Sthana": sthana,
            "Is Nasal?": "Yes" if v.is_anunasika else "No",
            "Clean": v.clean
        })

    st.markdown(f"<div>{html_out}</div>", unsafe_allow_html=True)
    
    # 3. DETAILED TABLE (Expander)
    with st.expander("📊 View Technical X-Ray (Properties Table)"):
        df = pd.DataFrame(data_rows)
        st.dataframe(df, use_container_width=True)

    # 4. SYNTHESIS CHECK
    st.subheader("2. Varna-Samyoga (Resynthesis)")
    joined = join(varnas)
    
    c_res1, c_res2 = st.columns([1, 4])
    with c_res1:
        if joined == text_input:
            st.success("✅ Match")
        else:
            st.error("❌ Error")
            
    with c_res2:
        st.code(f"Input:  {text_input}\nOutput: {joined}", language="text")
        if joined != text_input:
            st.warning("The re-joined text does not match the input. Check the 'join' logic in shared/varnas.py")