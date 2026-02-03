āṇinian Tagger", page_icon="🔍")

st.title("🔍 Pāṇinian Metadata Tagger")
st.markdown("### Sentence Analysis Engine")
st.write("This tool decomposes a Vākya into its a Vākya into its constituent Padas and labels their Pāṇinian properties.")

# Initialize the generative engine to use for reverse-matching
sp = SubantaProcessor()

# Consolidated list of stems for analysis
stems = ["राम", "हरि", "गुरु", "रमा", "सर्व", "तद्", "यद्", "इदम्", "भगवत्", "जगत्"]

# Add a list of known Avyayas (Indeclinables) for the engine
# 'स' is included in avyayas for general checking, but the specific 'तद्' pronoun rule takes precedence.
 constituent Padas and labels their Pāṇinian properties.")

# Initialize the generative engine to use for reverse-matching
sp = SubantaProcessor()

# Define stems and avyayas once, combining all requirements
stems = ["राम", "हरि", "गुरु", "रमा", "सर्व", "तद्", "यद्", "इदम्", "भगवत्", "जगत्"]

# Add a list of known Avyayas (Indeclinables) for the engine
# 'स' is included in avyayas for general checking, but the specific 'तद्' pronoun rule takes precedence.
avyayas = ["सृष्ट्वा", "इति", "च", "एव"]

sentence = st.text_input("Enter Sanskrit Sentence", "स भगवान् सृष्ट्वा जगत्")

# Combined analysis logic into a single button block
if st.button("Analyze Sentence"):
    if sentenceavyayas = ["सृष्ट्वा", "इति", "च", "एव", "स"] # Added 'स' here as per comment

sentence = st.text_input("Enter Sanskrit Sentence", "स भगवान् सृष्ट्वा जगत्")

# Combined analysis logic into a single button block
if st:
        words = sentence.split()
        analysis_results = []

        for word in words:
            # Basic cleaning for Anusvara and punctuation
            clean_word = word.replace("ं", "म्").strip(" ,।")
            match_found = False

            # 1.button("Analyze Sentence"):
    if sentence:
        words = sentence.split()
        analysis_results = []

        for word in words:
            # Basic cleaning for Anusvara and punctuation
            clean_word = word.replace("ं", "म्").strip(" ,।")
            match_foundimport streamlit as st
from logic.subanta_processor import SubantaProcessor

# Page Configuration
st. Check Avyayas first
            if clean_word in avyayas:
                analysis_results.append({
                    "Word": word, "Stem": clean_word, "Type": "Avyaya",
                    "Vibhakti": "N/A", "Vacana": "N/A",.set_page_config(page_title="Pāṇinian Tagger", page_icon="🔍")

st.title("🔍 Pāṇinian Metadata Tagger")
st.markdown("### Sentence Analysis Engine")
st.write("This tool decomposes a Vākya into its constituent Padas and = False

            # 1. Check Avyayas first
            if clean_word in avyayas:
                analysis_results.append({
                    "Word": word, "Stem": clean_word, "Type": "Avyaya",
                    "Vibhakti": "N "Status": "✅ Matched"
                })
                match_found = True
            
            # 2. If not an Avyaya, check Subanta paradigms
            if not match_found:
                # Handle 'स' as a special case for 'तद्' (Masculine 1/A", "Vacana": "N/A", "Status": "✅ Matched"
                })
                match_found = True
            
            # 2. If not an Avyaya, check Subanta paradigms
            if not match_found:
                # Handle 'स' as a labels their Pāṇinian properties.")

# Initialize the generative engine to use for reverse-matching
sp = SubantaProcessor()

# Consolidated list of stems for analysis
stems = ["राम", "हरि", "गुरु", "रमा", "सर्व", "तद्", "यद्", "इदम्", "भगवत्", "जगत्"]

# Add a list of known Avyayas (Indeclinables) for the engine
# Note: 'स' is included in avyayas for general checking, but the specific 'तद्' pronoun rule takes precedence.
avyayas = ["सृष्ट्वा", "इति", "च", "एव"]

sentence = st.text_input("Enter Sanskrit Sentence", "स भगवान् सृष्ट्वा जगत्")

# Combined analysis logic into a single button block
if st.button("Analyze Sentence"):
    if sentence:
        words =/1)
                if clean_word == "स":
                    analysis_results.append({
                        "Word": word, "Stem": "तद्", "Type": "Pronoun",
                        "Vibhakti": 1, "Vacana": 1, "Status": "✅ Mat special case for 'तद्' (Masculine 1/1)
                # This special handling allows prioritizing pronominal analysis for 'स'
                if clean_word == "स":
                    analysis_results.append({
                        "Word": word, "Stem": "तद्", "Type sentence.split()
        analysis_results = []

        for word in words:
            # Basic cleaning for Anusvara and punctuation
            clean_word = word.replace("ं", "म्").strip(" ,।")
            match_found = False

            # 1. Check Avyayas firstched"
                    })
                    match_found = True
                
                if not match_found: # Only proceed to standard Subanta lookup if not matched as 'स'
                    # Logic: Check if 'clean_word' matches any generated form of our stems
                    for stem in stems:
                        
            if clean_word in avyayas:
                analysis_results.append({
                    "Word": word, "Stem": clean_word, "Type": "Avyaya",
                    "Vibhakti": "N/A", "Vacana": "N/A", "Status": "✅ Mat# Skip 'तद्' if 'स' was already handled.
                        # For simplicity, we'll let the derive_pada handle 'तद्' for non-'स' forms
                        if stem == "तद्" and clean_word == "स": 
                            continue

                        for vibhakti in range(": "Pronoun",
                        "Vibhakti": 1, "Vacana": 1, "Status": "✅ Matched"
                    })
                    match_found = True
                
                if not match_found: # Only proceed to standard Subanta lookup if not matched as 'ched"
                })
                match_found = True

            # 2. If not an Avyaya, check for special case 'स' as 'तद्' pronoun
            if not match_found:
                if clean_word == "स": # Handle 'स' as a special1, 9):
                            for vacana in range(1, 4):
                                # Use the SubantaProcessor to derive the pada and compare
                                derived_pada = sp.derive_pada(stem, vibhakti, vacana)
                                if derived_pada == clean_word:स'
                    # Logic: Check if 'clean_word' matches any generated form of our stems
                    for stem in stems:
                        # Skip 'तद्' if 'स' was already handled (this prevents redundant checks if 'स' was matched above)
                        # For simplicity, we'll let the case for 'तद्' (Masculine 1/1)
                    analysis_results.append({
                        "Word": word, "Stem": "तद्", "Type": "Pronoun",
                        "Vibhakti": 1, "Vacana": 1, "Status": "
                                    analysis_results.append({
                                        "Word": word,
                                        "Stem": stem,
                                        "Type": "Subanta",
                                        "Vibhakti": vibhakti,
                                        "Vacana": vacana,
                                        "Status": "✅ derive_pada handle 'तद्' for non-'स' forms
                        if stem == "तद्" and clean_word == "स":
                             continue # 'स' specifically matched to 'तद्' as a pronoun already or handled by avyaya

                        for vibhakti in range( Matched"
                                    })
                                    match_found = True
                                    break # Exit vacana loop
                            if match_found: break # Exit vibhakti loop
                        if match_found: break # Exit stem loop

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
