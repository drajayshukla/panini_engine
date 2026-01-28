import streamlit as st
import json
import pandas as pd
import os
from collections import defaultdict


# --- १. डेटा लोडिंग ---
@st.cache_data
def load_shabd_data():
    file_path = os.path.join("data", "shabdroop.json")
    try:
        if not os.path.exists(file_path): return []
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


# --- २. प्रत्यय विश्लेषण इंजन ---
def get_ekavachana_pattern(forms_str):
    """एकवचन के प्रमुख विभक्तियों का प्रत्यय पैटर्न निकालना"""
    forms = [f.strip() for f in forms_str.split(";")]
    if len(forms) < 21: return None

    # विश्लेषण के लिए महत्वपूर्ण एकवचन स्थान:
    # प्रथमा(0), तृतीया(6), चतुर्थी(9), षष्ठी(15), सप्तमी(18)
    indices = [0, 6, 9, 15, 18]
    pattern = tuple(forms[i] for i in indices)
    return pattern


# --- ३. मुख्य इंटरफेस ---
def main():
    st.set_page_config(page_title="Unique Suffix Navigator", layout="wide", page_icon="🧬")
    st.title("🧬 Unique Suffix Navigator & Categorizer")
    st.info("यह यंत्र शब्दों को उनके 'एकवचन' प्रत्यय व्यवहार के आधार पर ५०+ समूहों में वर्गीकृत करता है।")

    data = load_shabd_data()
    if not data:
        st.error("डेटाबेस (shabdroop.json) नहीं मिला।")
        st.stop()

    # --- ४. ऑटो-वर्गीकरण (Categorization Logic) ---
    groups = defaultdict(list)
    for entry in data:
        pattern = get_ekavachana_pattern(entry.get("forms", ""))
        if pattern:
            # प्रथमा एकवचन के अंत को 'Key' बनाना (जैसे 'अः', 'इः', 'ई')
            main_suffix = pattern[0][-2:] if len(pattern[0]) > 1 else pattern[0]
            groups[main_suffix].append(entry)

    # ५०+ विशिष्ट समूहों को सॉर्ट करना
    sorted_suffixes = sorted(groups.keys(), key=lambda x: len(groups[x]), reverse=True)

    # --- ५. UI लेआउट ---
    st.sidebar.header("📁 प्रत्यय श्रेणियाँ (Top 50+)")
    selected_suffix = st.sidebar.radio(
        "मुख्य प्रत्यय अंत चुनें:",
        sorted_suffixes[:60]  # टॉप ६० यूनिक पैटर्न्स
    )

    if selected_suffix:
        entries = groups[selected_suffix]
        st.subheader(f"📊 समूह '...{selected_suffix}' के विशिष्ट शब्द-रूप (एकवचन विश्लेषण)")

        # टेबल के लिए डेटा तैयार करना
        table_list = []
        for e in entries:
            f = [forms.strip() for forms in e["forms"].split(";")]
            table_list.append({
                "शब्द": e["word"],
                "लिंग": e["linga"],
                "प्रथमा (1.1)": f[0],
                "तृतीया (3.1)": f[6],
                "चतुर्थी (4.1)": f[9],
                "षष्ठी (6.1)": f[15],
                "सप्तमी (7.1)": f[18],
                "अर्थ": e["artha_hin"]
            })

        df = pd.DataFrame(table_list)

        # इंटरएक्टिव टेबल
        st.dataframe(
            df.style.applymap(lambda x: 'color: #d32f2f; font-weight: bold' if selected_suffix in str(x) else ''),
            use_container_width=True,
            height=500
        )

        # विज़ुअलाइज़ेशन और तुलना
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✅ इस श्रेणी में कुल **{len(entries)}** विशिष्ट शब्द मिले हैं।")
            st.write("**व्याकरणिक टिप:** समान अंत वाले शब्दों में विभक्ति परिवर्तन प्रायः एक जैसे होते हैं।")

        with col2:
            st.download_button(
                "📥 इस श्रेणी का डेटा डाउनलोड करें",
                df.to_csv(index=False).encode('utf-8'),
                f"suffix_{selected_suffix}.csv",
                "text/csv"
            )


if __name__ == "__main__":
    main()