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
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


# --- २. प्रत्यय निष्कर्षण इंजन (Suffix Extraction) ---
def get_stem_and_suffix(word, forms_str):
    """शब्द और उसके रूपों से प्रत्यय पैटर्न निकालना"""
    forms = [f.strip() for f in forms_str.split(";")]
    # प्रथम-एकवचन से स्टेम का अनुमान लगाना
    first_form = forms[0].replace('ः', '').replace('म्', '')

    # प्रत्यय सूची तैयार करना (एकवचन के ७ रूप)
    suffixes = []
    for f in forms[:21]:  # सम्बोधन छोड़कर
        suffix = f.replace(word[:-1], "-", 1) if len(word) > 1 else f
        suffixes.append(suffix)
    return tuple(suffixes)


# --- ३. मुख्य इंटरफेस ---
def main():
    st.set_page_config(page_title="Suffix Explorer", layout="wide")
    st.title("🔬 Suffix-based Shabd Roop Categorization")
    st.caption("समान प्रत्यय पैटर्न वाले शब्दों का समूहिक विश्लेषण")

    data = load_shabd_data()
    if not data:
        st.error("डेटाबेस अप्राप्त!")
        st.stop()

    # --- ४. प्रत्यय आधारित वर्गीकरण (The Analysis) ---
    suffix_groups = defaultdict(list)

    for entry in data:
        forms = entry.get("forms", "")
        if forms:
            # प्रथम-एकवचन (Nominal Suffix) को 'Key' बनाना
            raw_list = [f.strip() for f in forms.split(";")]
            prathama_ek = raw_list[0]
            # प्रत्यय का मुख्य लक्षण (Ending)
            pattern_key = prathama_ek[-2:] if len(prathama_ek) > 2 else prathama_ek
            suffix_groups[pattern_key].append(entry)

    # --- ५. UI डिस्प्ले ---
    col_sidebar, col_main = st.columns([1, 3])

    with col_sidebar:
        st.subheader("📊 प्रत्यय श्रेणियाँ")
        sorted_keys = sorted(suffix_groups.keys(), key=lambda x: len(suffix_groups[x]), reverse=True)

        selected_pattern = st.radio(
            "मुख्य प्रत्यय अंत चुनें (Top 50+ Patterns):",
            sorted_keys[:60]  # सबसे विशिष्ट ५०+ प्रत्यय
        )

        st.metric("इस समूह में शब्द", len(suffix_groups[selected_pattern]))

    with col_main:
        st.header(f"श्रेणी: '...{selected_pattern}' प्रत्यय वाले शब्द")

        # चयनित समूह के शब्दों की तालिका
        group_data = []
        for e in suffix_groups[selected_pattern]:
            group_data.append({
                "शब्द": e['word'],
                "लिंग": e['linga'],
                "अर्थ": e['artha_hin'],
                "प्रथमा एकवचन": e['forms'].split(";")[0],
                "षष्ठी एकवचन": e['forms'].split(";")[15] if len(e['forms'].split(";")) > 15 else "-"
            })

        df = pd.DataFrame(group_data)
        st.dataframe(df, use_container_width=True)

        # विज़ुअलाइज़ेशन
        st.divider()
        st.subheader("💡 व्याकरणिक अंतर्दृष्टि (Insight)")
        st.info(f"'{selected_pattern}' पर समाप्त होने वाले शब्द प्रायः समान विभक्ति नियमों का पालन करते हैं। "
                f"इनमें संधि कार्य (जैसे णत्व विधान) प्रातिपदिक के अंतिम वर्ण पर निर्भर करते हैं।")

        # किसी एक शब्द का विस्तृत विवरण
        if not df.empty:
            selected_word = st.selectbox("विस्तृत विश्लेषण के लिए शब्द चुनें:", df["शब्द"])
            # यहाँ आपका पुराना ३x८ टेबल वाला कोड कॉल किया जा सकता है
            st.write(f"आप '{selected_word}' का संपूर्ण शब्द-रूप चक्र मुख्य 'Analyzer' पेज पर देख सकते हैं।")


if __name__ == "__main__":
    main()