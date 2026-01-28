import streamlit as st
import json
import pandas as pd
import os

# --- 1. पेज सेटअप और कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Shabd Roop Analyzer - अष्टाध्यायी-यंत्र", layout="wide", page_icon="🔬")


@st.cache_data
def load_shabd_data():
    # आपके नए फाइल पाथ के अनुसार (shabdroop.json)
    file_path = os.path.join("data", "shabdpath", "shabdroop.json")
    try:
        if not os.path.exists(file_path):
            st.error(f"फाइल नहीं मिली: {file_path}")
            return []
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"डेटा लोड करने में त्रुटि: {e}")
        return []


# --- 2. 'Surgical' लॉजिक फंक्शन्स ---

def split_forms(forms_str):
    """सेमीकोलन से अलग की गई स्ट्रिंग को लिस्ट में बदलना"""
    if isinstance(forms_str, list): return forms_str
    return [f.strip() for f in forms_str.split(";")]


def get_automatic_suffixes(forms_list):
    """Common Prefix हटाकर स्वतः प्रत्यय (Suffix) निकालना"""
    # सम्बोधन (ह्ए) को हटाकर स्टेम (Stem) ढूंढना
    filtered = [f for f in forms_list if not f.startswith("हे")]
    if not filtered: return forms_list

    prefix = os.path.commonprefix(filtered)
    # प्रत्यय निकालना
    return [f.replace(prefix, "", 1) if f.startswith(prefix) else f for f in forms_list]


def generate_vibhakt_table(forms_list, is_suffix=False):
    """21-24 रूपों को 3x8 टेबल में व्यवस्थित करना"""
    vibhakti_names = ["प्रथमा", "द्वितीया", "तृतीया", "चतुर्थी", "पञ्चमी", "षष्ठी", "सप्तमी", "सम्बोधन"]

    # 0::3 (एकवचन), 1::3 (द्विवचन), 2::3 (बहुवचन)
    ek = forms_list[0::3]
    dv = forms_list[1::3]
    bh = forms_list[2::3]

    # पैडिंग (Padding) ताकि टेबल फटे नहीं
    for l in [ek, dv, bh]:
        while len(l) < 8: l.append("—")

    df = pd.DataFrame({
        "विभक्ति": vibhakti_names,
        "एकवचनम्": ek[:8],
        "द्विवचनम्": dv[:8],
        "बहुवचनम्": bh[:8]
    })
    return df.set_index("विभक्ति")


# --- 3. UI रेंडरिंग (Main Page) ---

def main():
    st.title("🔬 संस्कृत शब्द-रूप विश्लेषक (Shabd Roop)")
    st.caption("सुप्-प्रत्यय एवं प्रातिपदिक विश्लेषण यंत्र")

    data = load_shabd_data()
    if not data:
        st.stop()

    # --- साइडबार फ़िल्टर्स ---
    st.sidebar.header("🔍 अन्वेषण फ़िल्टर")

    def get_uniques(key):
        return sorted(list(set(str(entry.get(key, "N/A")) for entry in data)))

    # आपके नए स्ट्रक्चर के अनुसार फ़िल्टर (linga, artha)
    sel_ling = st.sidebar.selectbox("लिंग (Linga)", ["All"] + get_uniques("linga"))
    sel_artha = st.sidebar.text_input("अर्थ से खोजें (Artha)", "")

    # डेटा फ़िल्टरिंग
    filtered = [
        e for e in data
        if (sel_ling == "All" or e.get("linga") == sel_ling) and
           (sel_artha.lower() in str(e.get("artha_hin", "")).lower() or sel_artha == "")
    ]

    if not filtered:
        st.warning("कोई शब्द मेल नहीं खाता।")
        st.stop()

    # शब्द चयन
    selected_word = st.sidebar.selectbox("शब्द चुनें (Select Word)", [e["word"] for e in filtered])
    entry = next(e for e in filtered if e["word"] == selected_word)

    # --- मुख्य प्रदर्शन (Display) ---
    st.header(f"शब्द विश्लेषण: {selected_word}")

    # इन्फो कार्ड्स
    m1, m2, m3 = st.columns(3)
    m1.metric("लिंग", "पुल्लिङ्ग" if entry.get('linga') == 'P' else entry.get('linga'))
    m2.metric("अर्थ", entry.get('artha_hin', 'N/A'))
    m3.metric("Base Index", entry.get('zbaseindex', '1.1'))

    # १. मूल शब्द-रूप टेबल
    st.subheader("📋 संपूर्ण शब्द-रूप चक्र (Full Declension)")
    raw_forms = split_forms(entry["forms"])
    st.table(generate_vibhakt_table(raw_forms))

    # २. ऑटो-जनरेटेड प्रत्यय विश्लेषण (Morphological Analysis)
    st.divider()
    st.subheader("🧬 स्वतः प्रत्यय निष्कर्षण (Automatic Suffix Extraction)")

    suffixes = get_automatic_suffixes(raw_forms)

    col_left, col_right = st.columns(2)

    with col_left:
        st.info("💡 यहाँ सिस्टम मूल शब्द (Stem) को हटाकर केवल प्रत्ययों को दिखा रहा है।")
        st.dataframe(generate_vibhakt_table(suffixes), use_container_width=True)

    with col_right:
        with st.expander("📝 शब्द की व्याख्या एवं नोट्स"):
            st.write(f"**व्युत्पत्ति:** {entry.get('vyutpatti', 'उपलब्ध नहीं')}")
            st.write(f"**विशेष टिप्पणी:** {entry.get('shabda_notes', 'कोई नहीं')}")
            st.write(f"**English Artha:** {entry.get('artha_eng', 'N/A')}")

    # --- डाउनलोड सेक्शन ---
    st.sidebar.divider()
    st.sidebar.download_button(
        label="📥 क्लीन डेटा डाउनलोड करें",
        data=json.dumps(data, ensure_ascii=False, indent=4),
        file_name="cleaned_shabdroop.json",
        mime="application/json"
    )


if __name__ == "__main__":
    main()