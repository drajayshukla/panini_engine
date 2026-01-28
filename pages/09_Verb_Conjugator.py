import streamlit as st
import json
import os

# --- १. पेज सेटअप ---
st.set_page_config(page_title="रूप-सिद्धि - अष्टाध्यायी-यंत्र", layout="wide", page_icon="📝")

st.title("📝 धातु-रूप सिद्घि (Verb Conjugator)")
st.caption("पाणिनीय ३x३ मैट्रिक्स आधारित लकार-रूप विश्लेषण")


# --- २. डायग्नोस्टिक लोडिंग (Diagnostic Loading) ---
def load_json_safe(file_name):
    path = os.path.join('data', file_name)
    if not os.path.exists(path):
        st.error(f"❌ फ़ाइल नहीं मिली: `{path}`")
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ `{file_name}` को पढ़ने में त्रुटि: {e}")
        return None


db_conjugation = load_json_safe('active_voice.json')
db_metadata = load_json_safe('dhatu_master_structured.json')

# --- ३. डेटा वैलिडेशन और मैपिंग ---
if db_conjugation is not None and db_metadata is not None:
    # एक 'Mapping' तैयार करें जो केवल वही धातु दिखाए जिनके रूप उपलब्ध हैं
    dhatu_map = {}

    # db_metadata एक लिस्ट है, इसे स्कैन करें
    for entry in db_metadata:
        k_index = entry.get('kaumudi_index')
        if k_index in db_conjugation:
            label = f"{entry.get('upadesha', '???')} ({entry.get('artha_sanskrit', 'अर्थ अनुपलब्ध')})"
            dhatu_map[label] = k_index

    if not dhatu_map:
        st.warning("⚠️ डेटा तो लोड हो गया, पर 'Kaumudi Index' मैच नहीं हो रहे हैं।")
        st.stop()

    # --- ४. यूज़र इंटरफेस (Selection) ---
    col1, col2 = st.columns([2, 1])

    with col1:
        selected_label = st.selectbox("धातु खोजें और चुनें:", options=list(dhatu_map.keys()))
        target_id = dhatu_map[selected_label]

    # लकार मैपिंग
    lakara_labels = {
        "plat": "लट् (वर्तमान)", "plit": "लिट् (परोक्ष अनद्यतन परोक्ष)",
        "plut": "लुट् (अनद्यतन भविष्य)", "plrut": "लृट् (सामान्य भविष्य)",
        "plot": "लोट् (आज्ञा/आशीष)", "plang": "लङ् (अनद्यतन भूत)",
        "pvidhiling": "विधिलिङ् (विधि/संभावना)", "pashirling": "आशीर्लिङ् (आशीर्वाद)",
        "plung": "लुङ् (सामान्य भूत)", "plrung": "लृङ् (हेतुहेतुमद्भाव)",
        "alat": "लट् (आत्मनेपद)", "alit": "लिट् (आत्मनेपद)",
        "alut": "लुट् (आत्मनेपद)", "alrut": "लृट् (आत्मनेपद)",
        "alot": "लोट् (आत्मनेपद)", "alang": "लङ् (आत्मनेपद)",
        "avidhiling": "विधिलिङ् (आत्मनेपद)", "aashirling": "आशीर्लिङ् (आत्मनेपद)",
        "alung": "लुङ् (आत्मनेपद)", "alrung": "लृङ् (आत्मनेपद)"
    }

    available_lakaras = db_conjugation[target_id].keys()

    with col2:
        selected_lakara_key = st.selectbox(
            "लकार चुनें:",
            options=list(available_lakaras),
            format_func=lambda x: lakara_labels.get(x, x)
        )

    # --- ५. ३x३ मैट्रिक्स डिस्प्ले ---
    st.markdown("---")
    st.subheader(f"🛡️ रूप विवरण: {selected_label}")

    grid = db_conjugation[target_id][selected_lakara_key]

    # पाणिनीय ग्रिड लेआउट
    # प्रथम पुरुष (P1), मध्यम (P2), उत्तम (P3)
    purushas = [("prathama", "प्रथम (III)"), ("madhyama", "मध्यम (II)"), ("uttama", "उत्तम (I)")]

    # हेडर
    h_col1, h_col2, h_col3, h_col4 = st.columns([1, 2, 2, 2])
    h_col2.markdown("<center><b>एकवचन</b></center>", unsafe_allow_html=True)
    h_col3.markdown("<center><b>द्विवचन</b></center>", unsafe_allow_html=True)
    h_col4.markdown("<center><b>बहुवचन</b></center>", unsafe_allow_html=True)

    for p_key, p_name in purushas:
        r_col1, r_col2, r_col3, r_col4 = st.columns([1, 2, 2, 2])
        r_col1.markdown(f"**{p_name}**")

        # डेटा दिखाना
        val_ek = grid.get(p_key, {}).get('ekavachana', '-')
        val_dvi = grid.get(p_key, {}).get('dvivachana', '-')
        val_bah = grid.get(p_key, {}).get('bahuvachana', '-')

        r_col2.info(val_ek)
        r_col3.info(val_dvi)
        r_col4.info(val_bah)

else:
    st.info(
        "💡 कृपया सुनिश्चित करें कि `data/` फोल्डर में `active_voice.json` और `dhatu_master_structured.json` मौजूद हैं।")

# --- ६. फुटर ---
st.markdown("---")
st.caption("Developed for Dr. Ajay Shukla | Paninian Engine v1.0")