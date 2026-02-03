import streamlit as st
from logic.subanta_processor import SubantaProcessor

# Page Configuration
st.set_page_config(page_title="Pāṇinian Tagger", page_icon="🔍")

st.title("🔍 Pāṇinian Metadata Tagger")
st.markdown("### Sentence Analysis Engine")
st.write("This tool decomposes a Vākya into its constituent Padas and labels their Pāṇinian properties.")

# Initialize the generative engine to use for reverse-matching
sp = SubantaProcessor()
# Common paradigms to check against
stems = ["राम", "हरि", "गुरु", "रमा", "सर्व", "तद्", "यद्", "इदम्"]

sentence = st.text_input("Enter Sanskrit Sentence", "स भगवान् सृष्ट्वा जगत्")

if st.button("Analyze Sentence"):
    if sentence:
        words = sentence.split()
        analysis_results = []
        
        for word in words:
            # Basic cleaning for Anusvara and punctuation
            clean_word = word.replace("ं", "म्").strip(" ,।")
            match_found = False
            
            # Logic: Check if 'clean_word' matches any generated form of our stems
            for stem in stems:
                for vibhakti in range(1, 9):
                    for vacana in range(1, 4):
                        if sp.derive_pada(stem, vibhakti, vacana) == clean_word:
                            analysis_results.append({
                                "Word": word,
                                "Stem": stem,
                                "Type": "Subanta",
                                "Vibhakti": vibhakti,
                                "Vacana": vacana,
                                "Status": "✅ Matched"
                            })
                            match_found = True
                            break
                    if match_found: break
                if match_found: break
            
            if not match_found:
                analysis_results.append({
                    "Word": word,
                    "Stem": "-",
                    "Type": "Unrecognized/Avyaya",
                    "Vibhakti": "-",
                    "Vacana": "-",
                    "Status": "❓ Review"
                })
        
        # Display as a professional table
        st.table(analysis_results)
    else:
        st.warning("Please enter a Sanskrit sentence to begin.")