import streamlit as st
from logic.subanta_processor import SubantaProcessor

# Page Configuration
st.set_page_config(page_title="Pāṇinian Tagger", page_icon="🔍")

st.title("🔍 Pāṇinian Metadata Tagger")
st.markdown("### Sentence Analysis Engine")
st.write("Decomposing Vākyas into Padas and labeling Pāṇinian properties.")

# Initialize the generative engine
sp = SubantaProcessor()

# 1. Define Stems and Avyayas (Indeclinables)
stems = ["राम", "हरि", "गुरु", "रमा", "सर्व", "तद्", "यद्", "इदम्", "भगवत्", "जगत्"]
avyayas = ["सृष्ट्वा", "इति", "च", "एव"]

sentence = st.text_input("Enter Sanskrit Sentence", "स भगवान् सृष्ट्वा जगत्")

if st.button("Analyze Sentence"):
    if sentence:
        words = sentence.split()
        analysis_results = []

        for word in words:
            # Basic cleaning for Anusvara and punctuation
            clean_word = word.replace("ं", "म्").strip(" ,।")
            match_found = False

            # STEP 1: Check Avyayas first
            if clean_word in avyayas:
                analysis_results.append({
                    "Word": word, "Stem": clean_word, "Type": "Avyaya",
                    "Vibhakti": "N/A", "Vacana": "N/A", "Status": "✅ Matched"
                })
                match_found = True

            # STEP 2: Special Case 'स' (Tad Pronoun 1/1)
            if not match_found and clean_word == "स":
                analysis_results.append({
                    "Word": word, "Stem": "तद्", "Type": "Pronoun",
                    "Vibhakti": 1, "Vacana": 1, "Status": "✅ Matched"
                })
                match_found = True
            
            # STEP 3: Standard Subanta Paradigm Lookup
            if not match_found:
                for stem in stems:
                    for v in range(1, 9):
                        for w in range(1, 4):
                            # Compare against the generator
                            if sp.derive_pada(stem, v, w) == clean_word:
                                analysis_results.append({
                                    "Word": word, "Stem": stem, "Type": "Subanta",
                                    "Vibhakti": v, "Vacana": w, "Status": "✅ Matched"
                                })
                                match_found = True
                                break
                        if match_found: break
                    if match_found: break

            # STEP 4: Fallback for Unrecognized Words
            if not match_found:
                analysis_results.append({
                    "Word": word, "Stem": "-", "Type": "Unknown",
                    "Vibhakti": "-", "Vacana": "-", "Status": "❓ Review"
                })

        st.table(analysis_results)
    else:
        st.warning("Please enter a Sanskrit sentence to begin.")