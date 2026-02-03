# Initialize the generative engine to use for reverse-matching
Line 12:      sp = SubantaProcessor()
Line 13:      
Line 14:      # Define stems and avyayas once, combining all requirements
Line 15:      stems = ["राम", "हरि", "गुरु", "रमा", "सर्व", "तद्", "यद्", "इदम्", "भगवत्", "जगत्"]
Line 16:      
Line 17:      # Add a list of known Avyayas (Indeclinables) for the engine
Line 1 prioritize the pronominal analysis.
avyayas = ["सृष्ट्वा", "इति", "च", "एव"]

sentence = st.text_input("Enter Sanskrit Sentence", "स भगवान् सृष्ट्वा जगत्")

# Combined analysis logic into a single button block
if st.button8:      # 'स' is included in avyayas for general checking, but the specific 'तद्' pronoun rule takes precedence.
Line 19:      avyayas = ["सृष्ट्वा", "इति", "च", "एव"]
Line 20:      
Line 21:Line("Analyze Sentence"):
    if sentence:
        words = sentence.split()
        analysis_results = []

        for word in words:
            # Basic cleaning for Anusvara and punctuation
            clean_word = word.replace("ं", "म्").strip(" ,।")
            match_found      sentence = st.text_input("Enter Sanskrit Sentence", "स भगवान् सृष्ट्वा जगत्")
Line 22:      
Line 23:      if st.button("Analyze Sentence"):
Line 24:          if sentence:
Line 25:              words = sentence. = False

            # Check Avyayas first
            if clean_word in avyayas:
                analysis_results.append({
                    "Word": word, "Stem": clean_word, "Type": "Avyaya",
                    "Vibhakti": "N/A", "Vacsplit()
Line 26:              analysis_results = []
Line 27:              
Line 28:              for word in words:
Line 29:                  # Basic cleaning for Anusvara and punctuation
Line 30:                  clean_word = word.replace("ं", 1: import streamlit as st
Line 2: from logic.subanta_processor import SubantaProcessor
Line 3:
Line 4: # Page Configuration
Line 5: st.set_page_config(page_title="Pāṇinian Tagger", page_icon="🔍") "म्").strip(" ,।")
Line 31:                  match_found = False
Line 32:                  
Line 33:                  # 1. Check Avyayas first
Line 34:                  if clean_word in avyayas:
Line 35:                      ana": "N/A", "Status": "✅ Matched"
                })
                match_found = True
            
            if not match_found: # Only proceed to check Subanta if not an Avyaya
                # Handle 'स' as a special case for 'तद्' (Mas
Line 6:
Line 7: st.title("🔍 Pāṇinian Metadata Tagger")
Line 8: st.markdown("### Sentence Analysis Engine")
Line 9: st.write("This tool decomposes a Vākya into its constituent Padas and labels their Pāṇinian propertiesanalysis_results.append({
Line 36:                          "Word": word, "Stem": clean_word, "Type": "Avyaya",
Line 37:                          "Vibhakti": "N/A", "Vacana": "N/A", "Status": "✅ Mat.")
Line 10:
Line 11: # Initialize the generative engine to use for reverse-matching
Line 12: sp = SubantaProcessor()
Line 13:
Line 14: # Consolidated list of stems for analysis
Line 15: stems = ["राम", "हरि", "गुरु", "रमा", "सर्व", "तद्", "यद्", "इदम्", "भगवत्", "जगत्"]
Line 16:
Line 17: # Add a list of known Avyayas (Indeclinables) for the engine
Line culine 1/1)
                if clean_word == "स":
                    analysis_results.append({
                        "Word": word, "Stem": "तद्", "Type": "Pronoun",
                        "Vibhakti": 1, "Vacana": 1, "ched"
Line 38:                      })
Line 39:                      match_found = True
Line 40:                  
Line 41:                  # 2. If not an Avyaya, check Subanta paradigms
Line 42:                  if not match_found:
18: avyayas = ["सृष्ट्वा", "इति", "च", "एव"]
Line 19:
Line 20: sentence = st.text_input("Enter Sanskrit Sentence", "स भगवान् सृष्ट्वा जगत्")
Line 21:
LineLine 43:                      for stem in stems:
Line 44:                          # Handle 'स' as a special case for 'तद्' (Masculine 1/1)
Line 45:                          if stem == "तद्" and clean_word == "स":
Line  22: if st.button("Analyze Sentence"):
Line 23:     if sentence:
Line 24:         words = sentence.split()
Line 25:         analysis_results = []
Line 26:
Line 27:         for word in words:
Status": "✅ Matched"
                    })
                    match_found = True
                
                if not match_found: # Only proceed to standard Subanta lookup if not matched as 'स'
                    # Logic: Check if 'clean_word' matches any generated form of our stems
                    forLine 28:             # Basic cleaning for Anusvara and punctuation
Line 29:             clean_word = word.replace("ं", "म्").strip(" ,।")
Line 30:             match_found = False
Line 31:
Line 32:             #46:                              analysis_results.append({
Line 47:                                  "Word": word, "Stem": "तद्", "Type": "Pronoun",
Line 48:                                  "Vibhakti": 1, "Vacana": 1, "Status": stem in stems:
                        # Skip 'तद्' if 'स' was already handled, unless other forms of 'तद्' are needed
                        # For simplicity, we'll let the derive_pada handle 'तद्' for non-'स' forms
                        if stem == "तद्" and clean_word "✅ Matched"
Line 49:                              })
Line 50:                              match_found = True
Line 51:                              break # Exit stem loop, as we found a match for 'स'
Line 52:                          
Line 53:                          # Standard lookup for other 1. Check Avyayas first
Line 33:             if clean_word in avyayas:
Line 34:                 analysis_results.append({
Line 35:                     "Word": word, "Stem": clean_word, "Type": "Avyaya",
Line  == "स": # This case was handled above. Can add more sophisticated checks here if needed.
                            continue

                        for vibhakti in range(1, 9):
                            for vacana in range(1, 4):
                                # Apply anusvara cleaning for comparison with derived pada
                                derived_pada = Subantas
Line 54:                          for vibhakti in range(1, 9):
Line 55:                              for vacana in range(1, 4):
Line 56:                                  # Use the SubantaProcessor to derive the pada and compare
Line 57 sp.derive_pada(stem, vibhakti, vacana)
                                if derived_pada == clean_word:
                                    analysis_results.append({
                                        "Word": word,
                                        "Stem": stem,
                                        "Type": "Subanta",
                                        "V36:                     "Vibhakti": "N/A", "Vacana": "N/A", "Status": "✅ Matched"
Line 37:                 })
Line 38:                 match_found = True
Line 39:
Line 40:             :                                  if sp.derive_pada(stem, vibhakti, vacana) == clean_word:
Line 58:                                      analysis_results.append({
Line 59:                                          "Word": word,
Line 60:                                          "Stem": stem,
Lineibhakti": vibhakti,
                                        "Vacana": vacana,
                                        "Status": "✅ Matched"
                                    })
                                    match_found = True
                                    break # Exit vacana loop
                            if match_found: break # Exit vibhakti loop
                        if match_found: break # Exit stem loop

            if not match_found:
                analysis_results.append({
                    "Word": word,
                    "Stem": "-",
                    "Type": "Unrecognized/Avyaya", # Changed 'Unknown' to 'Unrecognized/Avyaya' for consistency
                    "Vibhakti": "-",
                    "Vacana": "-",
                    "Status": "❓ Review"
                })

        # Display as a professional table
        st.table(analysis_results)
    else:
        st.warning("Please enter a Sanskrit sentence to begin.")
