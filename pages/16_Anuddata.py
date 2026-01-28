import streamlit as st
import json
import os
import random
import pandas as pd
from collections import Counter

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="Paninian Lab - Rigveda Edition", layout="wide", page_icon="⚖️")

# --- 2. CORE LOGIC ENGINE (Robust Rules) ---
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
    return json.load(open(path, "r", encoding="utf-8")) if os.path.exists(path) else []


def analyze_svara(text):
    results = []
    for i, char in enumerate(text):
        if char == '\u0952':  # Anudatta
            results.append({"Varna": text[i - 1], "Svara": "Anudatta", "Sutra": "1.2.30"})
        elif char == '\u0951':  # Svarit
            results.append({"Varna": text[i - 1], "Svara": "Svarit", "Sutra": "1.2.31"})
    return results


# --- 4. APP INTERFACE ---
def main():
    st.title("⚖️ Paninian Lab: Vedic & Morphological Engine")

    # --- RIGVEDA REFERENCE SECTION ---
    with st.expander("📖 Rigveda Digital Reference (Sanatana.in)", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("ऋग्वेद संहिता, पदपाठ और सायण भाष्य के लिए सीधे यहाँ क्लिक करें:")
            rik_link = "https://rigveda.sanatana.in/describe/rikMandala/001.004.004"
            st.markdown(f"### [🔗 ऋग्वेद मण्डल १, सूक्त ४, ऋक् ४]({rik_link})")
        with col2:
            st.info("यह वेबसाइट पाणिनीय सूत्रों के स्वर-विज्ञान (Accents) को सटीक रूप से दर्शाती है।")

    tab1, tab2, tab3 = st.tabs(["🔬 Vibhakti Diagnostic", "🎶 Vedic Svara Analyzer", "📐 Prakriya Map"])

    # --- TAB 1: VIBHAKTI ENGINE ---
    with tab1:
        st.header("Morphological Pattern Recognition")
        data = load_shabdroop()
        if data:
            all_symptoms = sorted(list(set([s for rules in LOGIC_RULES.values() for s in rules])))
            selected = st.selectbox("Select Suffix Symptom:", ["--सभी दिखाएं--"] + all_symptoms)
            matches = []
            cat_counter = Counter()
            random.shuffle(data)
            for entry in data:
                if len(matches) >= 50: break
                forms = entry.get("forms", "").split(";")
                if len(forms) < 21: continue
                targets = {"प्रथमा एकवचन": forms[0], "प्रथमा द्विवचन": forms[1], "प्रथमा बहुवचन": forms[2],
                           "द्वितीया बहुवचन": forms[5], "तृतीया एकवचन": forms[6], "चतुर्थी एकवचन": forms[9],
                           "षष्ठी एकवचन": forms[15], "सप्तमी एकवचन": forms[18]}
                for vib, roop in targets.items():
                    if cat_counter[vib] >= 7: continue
                    for p in LOGIC_RULES[vib]:
                        if roop.endswith(p) and (selected == "--सभी दिखाएं--" or roop.endswith(selected)):
                            matches.append(
                                {"order": VIBHAKTI_ORDER[vib], "Word": entry["word"], "Prathama 1.1": forms[0],
                                 "Vibhakti": vib, "Form": roop, "Suffix": p})
                            cat_counter[vib] += 1
                            break
            if matches:
                st.table(pd.DataFrame(sorted(matches, key=lambda x: x['order']))[
                             ["Word", "Prathama 1.1", "Vibhakti", "Form", "Suffix"]])

    # --- TAB 2: SVARA ANALYZER ---
    with tab2:
        st.header("Vedic Pitch Analysis (Svara)")
        vedic_input = st.text_area("Vedic Verse यहाँ पेस्ट करें (उदा. १.४.४):", value="यः क॒शिका॑सु ते॒ निष॑क्तो")

        if vedic_input:
            analysis = analyze_svara(vedic_input)
            if analysis:
                st.table(pd.DataFrame(analysis))
            else:
                st.info("सभी स्वर उदात्त (High Pitch) हैं।")

    # --- TAB 3: PRAKRIYA MAP ---
    with tab3:

        st.markdown("### १.२.२९-३१ के अनुसार स्वर प्रक्रिया का महत्व")


if __name__ == "__main__":
    main()