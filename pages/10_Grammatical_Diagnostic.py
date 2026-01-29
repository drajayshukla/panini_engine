#pages/10_Grammatical_Diagnostic.py
import streamlit as st
import json
import os

# --- १. पेज सेटअप ---
st.set_page_config(page_title="Diagnostic Tool - अष्टाध्यायी-यंत्र", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .diagnostic-card { background-color: #f0f4f8; border-left: 5px solid #1a73e8; padding: 20px; border-radius: 8px; margin-bottom: 10px; }
    .sutra-ref { color: #d32f2f; font-weight: bold; font-family: 'Sanskrit Text', serif; }
    .component-box { display: inline-block; padding: 5px 10px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; background: #fff; font-weight: bold; color: #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 Grammatical Diagnostic Tool")
st.caption("धातु-रूपों का वैज्ञानिक विश्लेषण एवं प्रकृति-प्रत्यय विभाग")


# --- २. डेटा लोडिंग ---
@st.cache_data
def load_data():
    meta_path = os.path.join('data', 'dhatu_master_structured.json')
    roopa_path = os.path.join('data', 'active_voice.json')
    if not os.path.exists(meta_path) or not os.path.exists(roopa_path): return None, None
    with open(meta_path, 'r', encoding='utf-8') as f: meta = json.load(f)
    with open(roopa_path, 'r', encoding='utf-8') as f: roopa = json.load(f)
    return meta, roopa


db_meta, db_roopa = load_data()

# लकारों के शुद्ध नाम (Reverse Mapping)
reverse_lakara_labels = {
    "plat": "लट् (वर्तमान)", "plit": "लिट् (परोक्ष भूत)", "plut": "लुट् (अनद्यतन भविष्य)",
    "plrut": "लृट् (सामान्य भविष्य)", "plot": "लोट् (आज्ञा/आशीष)", "plang": "लङ् (अनद्यतन भूत)",
    "pvidhiling": "विधिलिङ् (संभावना)", "pashirling": "आशीर्लिङ् (आशीर्वाद)",
    "plung": "लुङ् (सामान्य भूत)", "plrung": "लृङ् (हेतुहेतुमद्भाव)",
    "alat": "लट् (Atmanepada)", "alit": "लिट् (Atmanepada)", "alut": "लुट् (Atmanepada)",
    "alrut": "लृट् (Atmanepada)", "alot": "लोट् (Atmanepada)", "alang": "लङ् (Atmanepada)",
    "avidhiling": "विधिलिङ् (Atmanepada)", "aashirling": "आशीर्लिङ् (Atmanepada)",
    "alung": "लुङ् (Atmanepada)", "alrung": "लृङ् (Atmanepada)"
}


# --- ३. Diagnostic Logic Engine (Etiology) ---
def get_component_breakdown(roop, lakara):
    # भविष्यति/भविष्यामि आदि के लिए उदाहरण विश्लेषण
    if "िष्य" in roop:
        return {
            "धातु": "भू",
            "आगम": "इट् (इ)",
            "विकरण": "स्य (लृट्)",
            "प्रत्यय": "ति/सि/मि (तिङ्)",
            "सूत्र": "आर्धधातुकस्येड्वलादेः (७.२.३५)"
        }
    return None


# --- ४. मुख्य इंटरफेस ---
if db_meta and db_roopa:
    # मेटाडेटा मैप तैयार करना (Easy Retrieval)
    meta_map = {str(d.get('identifier')).strip(): d for d in db_meta}

    col_a, col_b = st.columns([1, 2])

    with col_a:
        st.subheader("🔍 लक्षण (Selection)")
        search_roop = st.text_input("रूप लिखें (e.g., भवति, भविष्यति):")
        st.info("💡 यह इंजन रूप को स्कैन करके उसकी 'Etiology' का पता लगाएगा।")

    with col_b:
        st.subheader("🧬 निदान (Diagnosis)")
        if search_roop:
            search_roop = search_roop.strip()
            found = False

            # पूरे डेटाबेस में रूप की तलाश
            for d_id, lakaras in db_roopa.items():
                for lak_code, grid in lakaras.items():
                    for pur, vach in grid.items():
                        for v_type, val in vach.items():
                            # कोमा से अलग रूपों को भी चेक करें
                            if search_roop in [v.strip() for v in val.split(',')]:
                                found = True

                                # डेटा रिट्रीवल
                                d_info = meta_map.get(d_id, {})
                                readable_lakara = reverse_lakara_labels.get(lak_code, lak_code)

                                # १. सफलता का संदेश
                                st.markdown(f"""
                                <div class='diagnostic-card'>
                                    <h3>✅ रूप की पहचान सफल!</h3>
                                    <p><b>धातु:</b> <span class='component-box'>{d_info.get('upadesha', '???')}</span> ({d_info.get('artha_sanskrit', 'N/A')})</p>
                                    <p><b>लकार:</b> <span class='component-box'>{readable_lakara}</span></p>
                                    <p><b>स्थान:</b> {pur.capitalize()} पुरुष - {v_type.capitalize()}</p>
                                    <p><b>ID:</b> {d_id}</p>
                                </div>
                                """, unsafe_allow_html=True)

                                # २. प्रकृति-प्रत्यय विभाग (Breakdown)
                                breakdown = get_component_breakdown(search_roop, lak_code)
                                if breakdown:
                                    st.markdown("### 🛠️ अङ्ग-प्रत्यय विभाग")
                                    b_cols = st.columns(len(breakdown) - 1)
                                    for i, (key, value) in enumerate(list(breakdown.items())[:-1]):
                                        b_cols[i].markdown(f"**{key}**\n<div class='component-box'>{value}</div>",
                                                           unsafe_allow_html=True)
                                    st.markdown(
                                        f"**प्रमुख सूत्र:** <span class='sutra-ref'>{breakdown['सूत्र']}</span>",
                                        unsafe_allow_html=True)
                                break
                        if found: break
                    if found: break
                if found: break

            if not found:
                st.warning(f"रूप '{search_roop}' डेटाबेस में नहीं मिला।")

    # --- ५. Comparative Gana Analysis ---
    st.divider()
    st.subheader("🆚 Comparative Gana Analysis")
    ganas = ["भ्वादि", "अदादि", "जुहोत्यादि", "दिवादि", "स्वादि", "तुदादि", "रुधादि", "तन्वादि", "क्र्यादि", "चुरादि"]
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        g1 = st.selectbox("गण १:", ganas, index=0)
    with g_col2:
        g2 = st.selectbox("गण २:", ganas, index=1)
    st.info(f"💡 {g1} और {g2} के बीच मुख्य अंतर **'विकरण' (Shap vs Luk)** का है।")

else:
    st.error("डेटा फाइलें अप्राप्त हैं।")

st.markdown("---")
st.caption("Paninian Diagnostic Module | Developed for Dr. Ajay Shukla")