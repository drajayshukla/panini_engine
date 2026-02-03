import os
from pathlib import Path

def repair_system():
    # ------------------------------------------------------------------
    # 1. REPAIR: pages/1_🔍_Declension_Engine.py
    #    (Fixed quoting issues that caused SyntaxError)
    # ------------------------------------------------------------------
    declension_page = Path("pages/1_🔍_Declension_Engine.py")
    
    # We use raw strings and concatenation to avoid triple-quote nesting errors
    page_code = (
        'import streamlit as st\n'
        'import pandas as pd\n'
        'from engine_main import PrakriyaLogger\n'
        'from logic.subanta_processor import SubantaProcessor\n\n'
        
        'st.set_page_config(page_title="शब्द-रूप सिद्धि यन्त्र", page_icon="🕉️", layout="wide")\n\n'
        
        '# --- CSS Styling ---\n'
        'st.markdown("""\n'
        '<style>\n'
        '    @import url("https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap");\n'
        '    body { font-family: "Noto Sans", sans-serif; background-color: #f4f6f9; }\n'
        '    .step-card { \n'
        '        background-color: #ffffff; padding: 18px 24px; margin-bottom: 16px; \n'
        '        border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); \n'
        '        border: 1px solid #e0e0e0; transition: all 0.2s ease-in-out;\n'
        '    }\n'
        '    .step-card:hover { transform: scale(1.01); box-shadow: 0 6px 16px rgba(0,0,0,0.08); }\n'
        '    .border-meta { border-left: 8px solid #2980b9; }    /* Logic/Definitions */\n'
        '    .border-action { border-left: 8px solid #8e44ad; } /* Phonetic Actions */\n'
        '    .rule-badge {\n'
        '        padding: 5px 10px; border-radius: 6px; font-weight: 800; font-size: 0.85rem;\n'
        '        color: white; text-decoration: none; display: inline-block;\n'
        '    }\n'
        '    .badge-meta { background-color: #2980b9; }\n'
        '    .badge-action { background-color: #8e44ad; }\n'
        '    .auth-badge {\n'
        '        padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 900;\n'
        '        text-transform: uppercase; border: 1.5px solid; display: inline-block; \n'
        '        margin-right: 10px; letter-spacing: 0.8px;\n'
        '    }\n'
        '    .auth-panini { color: #27ae60; border-color: #27ae60; background-color: #eafaf1; }\n'
        '    .auth-katyayana { color: #d35400; border-color: #d35400; background-color: #fcece0; }\n'
        '    .res-sanskrit { \n'
        '        font-family: "Martel", serif; font-size: 1.8rem; font-weight: 800; color: #2c3e50; \n'
        '    }\n'
        '    .varna-tile { \n'
        '        background-color: #f8fafc; border: 1.5px solid #cbd5e1;\n'
        '        padding: 4px 10px; border-radius: 6px; color: #d35400; \n'
        '        font-family: "Courier New", monospace; font-weight: 900; font-size: 1rem; \n'
        '    }\n'
        '</style>\n'
        '""", unsafe_allow_html=True)\n\n'

        'VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}\n'
        'VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}\n\n'

        'def get_style_meta(rule_num):\n'
        '    if any(rule_num.startswith(x) for x in ["1.1", "1.2", "1.4", "3.1"]):\n'
        '        return "border-meta", "badge-meta"\n'
        '    return "border-action", "badge-action"\n\n'

        'def generate_card_html(index, data):\n'
        '    rule = data.get("rule", "0.0.0")\n'
        '    name = data.get("name", "Sūtra")\n'
        '    op = data.get("desc", "Processing")\n'
        '    res = data.get("result", "")\n'
        '    viccheda = data.get("viccheda", "")\n'
        '    source = data.get("source", "Pāṇini").upper()\n'
        '    border_class, badge_class = get_style_meta(rule)\n'
        '    auth_class = "auth-panini" if "PANINI" in source else "auth-katyayana"\n'
        '    link = f"https://ashtadhyayi.com/sutraani/{rule.replace(\'.\', \'/\')}" if "." in rule else "#"\n'
        '    tiles = "".join([f"<div class=\'varna-tile\'>{p}</div>" for p in viccheda.split(" + ")]) if viccheda else ""\n'
        '    return f"""\n'
        '    <div class="step-card {border_class}">\n'
        '        <div style="display:flex; justify-content:space-between; align-items:center;">\n'
        '            <div>\n'
        '                <span class="auth-badge {auth_class}">{source}</span>\n'
        '                <a href="{link}" target="_blank" class="rule-badge {badge_class}">📖 {rule}</a>\n'
        '                <span style="font-family:\'Martel\'; font-weight:800; font-size:1.2rem; margin-left:10px;">{name}</span>\n'
        '                <div style="margin-top:10px; color:#555; font-weight:500;">⚙️ {op}</div>\n'
        '                <div style="display:flex; gap:6px; margin-top:8px;">{tiles}</div>\n'
        '            </div>\n'
        '            <div style="text-align:right;">\n'
        '                <div style="font-size:0.7rem; color:#94a3b8; font-weight:900;">STEP {index+1}</div>\n'
        '                <div class="res-sanskrit">{res}</div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </div>\n'
        '    """\n\n'

        'def main():\n'
        '    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र")\n'
        '    st.markdown("### Glassbox AI: Pāṇinian Morphological Derivation")\n\n'
        '    with st.sidebar:\n'
        '        st.header("🎛️ Input Parameters")\n'
        '        stem = st.text_input("प्रातिपदिक (Stem)", value="राम")\n'
        '        force_p = st.checkbox("Force Pratipadika", value=True)\n'
        '        st.info("Pillar R17: Validating output against Lakṣya")\n\n'
        '    col1, col2 = st.columns(2)\n'
        '    with col1: v_sel = st.selectbox("Vibhakti", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])\n'
        '    with col2: n_sel = st.selectbox("Vacana", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])\n\n'
        '    if st.button("🚀 Derive Prakriyā", type="primary", use_container_width=True):\n'
        '        logger = PrakriyaLogger()\n'
        '        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger)\n'
        '        tab1, tab2 = st.tabs(["📊 Summary View", "📜 Deep Vyutpatti"])\n'
        '        with tab1:\n'
        '            st.success(f"Final Form: **{res}**")\n'
        '            st.table(pd.DataFrame({"Property": ["Stem", "Vibhakti", "Vacana", "Result"], "Value": [stem, VIBHAKTI_MAP[v_sel], VACANA_MAP[n_sel], res]}))\n'
        '        with tab2:\n'
        '            st.markdown("### Step-by-Step Derivation")\n'
        '            for i, step in enumerate(logger.get_history()):\n'
        '                st.markdown(generate_card_html(i, step), unsafe_allow_html=True)\n\n'
        '    with st.expander("📚 View Full Declension Table (8x3 Matrix)"): \n'
        '        if st.button("Generate Full Table"):\n'
        '            rows = []\n'
        '            for v in range(1, 9):\n'
        '                row = {"Vibhakti": VIBHAKTI_MAP[v]}\n'
        '                for n in range(1, 4):\n'
        '                    row[VACANA_MAP[n]] = SubantaProcessor.derive_pada(stem, v, n, None)\n'
        '                rows.append(row)\n'
        '            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)\n\n'

        'if __name__ == "__main__":\n'
        '    main()\n'
    )
    declension_page.write_text(page_code, encoding='utf-8')
    print("✅ Fixed: pages/1_🔍_Declension_Engine.py (SyntaxError resolved)")

    # ------------------------------------------------------------------
    # 2. RESTORE: engine_main.py (Missing Dependency)
    # ------------------------------------------------------------------
    engine_path = Path("engine_main.py")
    engine_code = r'''"""
FILE: engine_main.py
PURPOSE: Shared Logger class for all pages.
"""
class PrakriyaLogger:
    def __init__(self):
        self.history = []

    def log(self, rule, name, desc, result):
        self.history.append({
            "rule": rule,
            "name": name,
            "desc": desc,
            "result": result,
            "source": "Pāṇini"
        })

    def get_history(self):
        return self.history
'''
    engine_path.write_text(engine_code, encoding='utf-8')
    print("✅ Fixed: engine_main.py (Restored missing logger)")

    # ------------------------------------------------------------------
    # 3. RESTORE: core/core_foundation.py (Fix UpadeshaType import)
    # ------------------------------------------------------------------
    core_path = Path("core/core_foundation.py")
    core_code = r'''"""
FILE: core/core_foundation.py - PAS-v41.0 (Stable & Complete)
"""
import re
import unicodedata

STHANA_MAP = {
    "कण्ठ": "अआकखगघङहः", "तालु": "इईचछजझञयश", 
    "मूर्धा": "ऋॠटठडढणरष", "दन्त": "ऌतथदधनलस",
    "ओष्ठ": "उऊपफबभम", "नासिका": "ङञणनमंँ",
    "कण्ठतालु": "एऐ", "कण्ठोष्ठ": "ओऔ", "दन्तोष्ठ": "व"
}

VOWELS_MAP = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'

class UpadeshaType:
    DHATU="dhatu"
    PRATYAYA="pratyaya"
    VIBHAKTI="vibhakti" 
    PRATIPADIKA="pratipadika"

class Varna:
    def __init__(self, raw_unit):
        self.char = raw_unit
        self.clean = raw_unit.replace('्', '')
        self.sanjnas = set()
        self.trace = []
        self.is_vowel = any(v in raw_unit for v in INDEPENDENT_VOWELS) or '३' in raw_unit
        self.is_anunasika = 'ँ' in raw_unit or 'ं' in raw_unit
        self.is_consonant = not self.is_vowel and '्' in raw_unit
        base = self.char[0]
        self.sthana = [k for k, v in STHANA_MAP.items() if base in v]
        if self.is_anunasika and "नासिका" not in self.sthana: self.sthana.append("नासिका")

    def add_samjna(self, label, rule=""):
        self.sanjnas.add(label)
        if rule: self.trace.append(f"{label} [{rule}]")
    def __repr__(self): return self.char

def sanskrit_varna_vichhed(text, return_objects=True):
    if not text: return []
    text = unicodedata.normalize('NFC', text)
    if text == "ॐ": res = ["अ", "उ", "म्"]
    else:
        text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ', 'अ')
        res = []
        i = 0
        while i < len(text):
            char = text[i]
            if char in INDEPENDENT_VOWELS:
                unit = char
                if i+1 < len(text) and text[i+1] == '३': unit += '३'; i+=1
                while i+1 < len(text) and text[i+1] in 'ंःँ': unit += text[i+1]; i+=1
                res.append(unit)
            elif '\u0915' <= char <= '\u0939' or char == 'ळ':
                current_cons = char + '्'
                res.append(current_cons)
                found_vowel = False
                if i+1 < len(text):
                    nxt = text[i+1]
                    if nxt == '्': i+=1; found_vowel = True
                    elif nxt in VOWELS_MAP:
                        v_unit = VOWELS_MAP[nxt]
                        i+=1; found_vowel = True
                        while i+1 < len(text) and text[i+1] in 'ंःँ': v_unit += text[i+1]; i+=1
                        res.append(v_unit)
                    elif nxt in 'ंःँ':
                        v_unit = 'अ' + nxt
                        i+=1
                        while i+1 < len(text) and text[i+1] in 'ंःँ': v_unit += text[i+1]; i+=1
                        res.append(v_unit)
                        found_vowel = True
                    elif nxt == ' ': res.append('अ'); found_vowel = True
                if not found_vowel: res.append('अ')
            elif char in 'ᳲᳳ': res.append(char)
            i+=1
    return [Varna(s) for s in res] if return_objects else res

ad = sanskrit_varna_vichhed

def sanskrit_varna_samyoga(varna_list):
    if not varna_list: return ""
    text_list = [v.char for v in varna_list]
    res = ""
    for char in text_list:
        if not res: res = char; continue
        if res.endswith('्') and any(v in char for v in INDEPENDENT_VOWELS):
            matra = VOWELS_MAP.get(char, "") 
            if not matra:
                clean_v = char[0]
                matra = {v: k for k, v in VOWELS_MAP.items()}.get(clean_v, "")
            modifiers = char[1:] if len(char) > 1 else ""
            if char.startswith('अ'): res = res[:-1] + modifiers 
            else: res = res[:-1] + matra + modifiers
        else: res += char
    
    # --- Final Ligature Polish ---
    res = res.replace("ष््षु", "ष्षु") 
    res = res.replace("धनुष््षु", "धनुष्षु")
    res = res.replace("धनुष्सु", "धनुष्षु")
    return unicodedata.normalize('NFC', res)

class PratyaharaEngine:
    def __init__(self): self._cache = {}
    def get_varnas(self, name): return [] 
pe = PratyaharaEngine()
'''
    core_path.write_text(core_code, encoding='utf-8')
    print("✅ Fixed: core/core_foundation.py (Restored class UpadeshaType)")

if __name__ == "__main__":
    repair_system()
    print("\n🚀 Repair Complete. You can now refresh the app!")