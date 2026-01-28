import streamlit as st
import json
import os
import random
import pandas as pd
from collections import Counter

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="Paninian Diagnostic Lab", layout="wide", page_icon="⚖️")

# --- 2. CORE LOGIC ENGINE ---
LOGIC_RULES = {
    "प्रथमा एकवचन": ["ः", "न्", "म्", "ा", "ी", "ू", "ऋ", "क्", "ट्", "प्", "त्", "ाः", "व", "ा", "ह"],
    "प्रथमा द्विवचन": ["औ", "ौ", "ए", "े", "ई", "ी", "नी", "णी"],
    "प्रथमा बहुवचन": ["ाः", "यः", "वः", "णि", "सि", "अः", "हः", "धः", "शः", "तः", "नः", "य", "ए", "ा"],
    "द्वितीया बहुवचन": ["आन्", "ईन्", "ून्", "ॄन्", "ः", "ईः", "ऊः", "अः", "ाः", "ानि", "ाणि"],
    "तृतीया एकवचन": ["एण", "णा", "ना", "या", "त्रा", "सा", "वा", "ा", "ता", "धा", "भा", "या", "ना", "इना"],
    "चतुर्थी एकवचन": ["आय", "ये", "वे", "त्रे", "यै", "स्मै", "भ्यम्", "ते", "ने", "से", "ए", "ने", "ये", "ए"],
    "षष्ठी एकवचन": ["स्य", "अः", "ओः", "आः", "याः", "तुः", "सः", "तः", "नः", "चः", "जः", "षः", "हः", "शः"],
    "सप्तमी एकवचन": ["ए", "औ", "रि", "ति", "नि", "वि", "यि", "याम्", "वाम्", "इ", "षि", "धि", "स्मिन्", "आम्", "ौ"]
}

VIBHAKTI_ORDER = {
    "प्रथमा एकवचन": 1, "प्रथमा द्विवचन": 2, "प्रथमा बहुवचन": 3,
    "द्वितीया बहुवचन": 6, "तृतीया एकवचन": 7, "चतुर्थी एकवचन": 10,
    "षष्ठी एकवचन": 16, "सप्तमी एकवचन": 19
}


# --- 3. UTILITY FUNCTIONS ---
@st.cache_data
def load_shabdroop():
    path = os.path.join("data", "shabdroop.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def sanskrit_match(word, suffix):
    word = str(word).strip()
    v_to_m = {'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू', 'ऋ': 'ृ', 'ॠ': 'ॄ', 'ए': 'े', 'ऐ': 'ै', 'ओ': 'ो',
              'औ': 'ौ'}
    if suffix.startswith('अ'):
        core = suffix[1:]
        if not word.endswith(core): return False
        pos = len(word) - len(core) - 1
        return pos >= 0 and '\u0915' <= word[pos] <= '\u0939'
    for v, m in v_to_m.items():
        if suffix.startswith(v) and word.endswith(m + suffix[1:]): return True
    return word.endswith(suffix)


def analyze_svara(text):
    results = []
    for i, char in enumerate(text):
        if char == '\u0952':  # Anudatta
            results.append({"Varna": text[i - 1], "Svara": "Anudatta (नीचैरनुदात्तः)", "Sutra": "1.2.30"})
        elif char == '\u0951':  # Svarit
            results.append({"Varna": text[i - 1], "Svara": "Svarit (समाहारः स्वरितः)", "Sutra": "1.2.31"})
    return results


# --- 4. APP INTERFACE ---
def main():
    st.title("⚖️ Paninian Morphology & Phonetics Lab")

    tab1, tab2, tab3 = st.tabs(["🔬 Vibhakti Diagnostic", "🎶 Vedic Svara Analyzer", "📐 Prakriya Map"])

    # --- TAB 1: VIBHAKTI ENGINE ---
    with tab1:
        st.header("Vibhakti Pattern Recognition")
        data = load_shabdroop()
        if not data:
            st.warning("Data file not found at data/shabdroop.json")
        else:
            all_symptoms = sorted(list(set([s for rules in LOGIC_RULES.values() for s in rules])))
            selected = st.selectbox("Select Suffix Symptom:", ["--Show All--"] + all_symptoms)

            matches = []
            cat_counter = Counter()
            random.shuffle(data)

            for entry in data:
                if len(matches) >= 50: break
                forms = entry.get("forms", "").split(";")
                if len(forms) < 21: continue

                targets = {
                    "प्रथमा एकवचन": forms[0], "प्रथमा द्विवचन": forms[1], "प्रथमा बहुवचन": forms[2],
                    "द्वितीया बहुवचन": forms[5], "तृतीया एकवचन": forms[6], "चतुर्थी एकवचन": forms[9],
                    "षष्ठी एकवचन": forms[15], "सप्तमी एकवचन": forms[18]
                }

                for vib, roop in targets.items():
                    if cat_counter[vib] >= 7: continue
                    for p in LOGIC_RULES[vib]:
                        if sanskrit_match(roop, p):
                            if selected == "--Show All--" or sanskrit_match(roop, selected):
                                matches.append({
                                    "order": VIBHAKTI_ORDER[vib], "Word": entry["word"],
                                    "Prathama 1.1": forms[0], "Vibhakti": vib, "Form": roop, "Suffix": p
                                })
                                cat_counter[vib] += 1
                                break

            if matches:
                df = pd.DataFrame(sorted(matches, key=lambda x: x['order']))
                st.table(df[["Word", "Prathama 1.1", "Vibhakti", "Form", "Suffix"]])

    # --- TAB 2: SVARA ANALYZER ---
    with tab2:
        st.header("Vedic Pitch Analysis (Svara)")
        vedic_input = st.text_input("Enter Vedic Verse:", value="अ॒ग्निमी॑ळे पु॒रोहि॑तं")

        if vedic_input:
            analysis = analyze_svara(vedic_input)
            if analysis:
                st.table(pd.DataFrame(analysis))
                st.success("Analysis based on Sutras 1.2.29-31")
            else:
                st.info("No specific Anudatta/Svarit marks detected. Vowels are high pitch (Udatta 1.2.29).")

    # --- TAB 3: PRAKRIYA MAP ---
    with tab3:
        st.header("Ashtadhyayi Derivation Logic")
        st.markdown("""
        The derivation of any Sanskrit form follows this chronological flow in the **Ashtadhyayi**:
        1. **Upadesha:** The original element (Dhatu/Pratipadika).
        2. **It-Sanjna:** Identification of technical markers.
        3. **Lopa:** Removal of markers.
        4. **Pratyaya-Vidhana:** Adding the Suffixes.
        """)


if __name__ == "__main__":
    main()