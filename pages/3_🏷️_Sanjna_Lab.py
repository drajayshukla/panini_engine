import streamlit as st
import sys
import os

# Path Hack for Modular Imports
sys.path.append(os.path.abspath('.'))
from shared.varnas import ad, join
from shared.anubandha import AnubandhaEngine

st.set_page_config(page_title="Sanjna Lab", page_icon="🏷️", layout="wide")

st.markdown("""
<style>
    .result-box { font-size: 2em; font-weight: bold; color: #2c3e50; }
    .tag-badge { 
        background-color: #8e44ad; 
        color: white; 
        padding: 5px 12px; 
        border-radius: 20px; 
        font-size: 1em; 
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
</style>
""", unsafe_allow_html=True)

st.title("🏷️ Sanjñā Lab (The Invisible Tags)")
st.markdown("### 1.3.9 Tasya Lopaḥ: The Body dies, the Soul (Tag) remains.")
st.caption("Enter an Upadeśa to see its Tags and their grammatical power.")

# --- KNOWLEDGE BASE: THE FUNCTION OF TAGS ---
KARYA_DB = {
    # Consonant Tags
    "Kit": ("1.1.5 Gkniti ca", "🚫 Blocks Guna & Vriddhi."),
    "Ghit": ("1.1.5 Gkniti ca", "🚫 Blocks Guna & Vriddhi (specifically for Kutva)."),
    "Ñit": ("1.3.12 / 7.2.115", "🔄 Atmanepada (if Dhatu) OR Vriddhi of initial vowel (if Taddhita)."),
    "Nit": ("7.2.115 Aco'ñniti", "📈 Causes Vriddhi of the initial vowel."),
    "Ṣit": ("4.1.41 Ṣidgaurādibhyaśca", "👩 Adds Feminine suffix Ṅīṣ (e.g., Nartakī)."),
    "Pit": ("3.1.4 Anudāttau suppitau", "📉 Suffix has Anudatta (Low) accent."),
    "Cit": ("6.1.163 Citaḥ", "🔝 Final syllable gets Udatta (High) accent."),
    "Tit": ("6.1.185 Titaḥ", "〰️ Svarita accent on the tag itself."),
    "Mit": ("1.1.47 Midaco'ntyātparaḥ", "👉 Inserts itself after the last vowel (e.g. Num, Snam)."),
    
    # Vowel Tags
    "Udit": ("7.2.56 Uditō vā", "⚡ Optional It-Agama in Ktva pratyaya."),
    "Idit": ("7.1.58 Idito num dhātoḥ", "➕ Inserts 'Num' (n) infix into the root (e.g. Vand)."),
    "Īdit": ("7.2.14 Śvīdito niṣṭhāyām", "🚫 Prohibits It-Agama in Niṣṭhā (Kta/Ktavatu)."),
    "Ṛdit": ("7.4.2 Nāglopiśāsvṛditām", "📏 Prevents shortening of penultimate vowel in Chang Aorist."),
    "Lṛdit": ("3.1.55 Puṣādyudyutā...", "🔁 Selects 'Aṅ' Vikarana instead of 'Cli' in Aorist."),
}

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
                tag_html += f'<span class="tag-badge">{t}</span>'
            st.markdown(tag_html, unsafe_allow_html=True)
        else:
            st.warning("No It-Tags found.")

    # 3. KARYA MAPPING
    st.subheader("🚀 Kārya (Grammatical Effects)")
    if tags:
        found = False
        for tag in tags:
            # Normalize tag lookup (handle Ñit/Nit variants)
            lookup_tag = tag
            if tag not in KARYA_DB:
                # Fallback for simple single-letter tags like 'kit' -> 'Kit'
                if tag.title() in KARYA_DB: lookup_tag = tag.title()
            
            if lookup_tag in KARYA_DB:
                found = True
                sutra, desc = KARYA_DB[lookup_tag]
                st.markdown(f"""
                <div class="karya-card">
                    <span class="tag-badge" style="font-size:0.8em;">{tag}</span>
                    <span class="karya-title">{desc}</span><br>
                    <span class="karya-sutra">📖 {sutra}</span>
                </div>
                """, unsafe_allow_html=True)
        
        if not found:
            st.caption("Tags detected, but no specific effect hardcoded in this demo DB.")
    else:
        st.caption("No tags = No special grammatical triggers.")

    # 4. TRACE LOG
    with st.expander("📜 View Derivation Logic (Prakriyā)"):
        for step in trace:
            if "SAVED" in step:
                st.success(step)
            elif "disappears" in step:
                st.error(step)
            else:
                st.write(step)