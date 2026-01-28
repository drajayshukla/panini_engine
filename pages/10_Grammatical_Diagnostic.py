import streamlit as st
import json
import os

# --- १. पेज सेटअप ---
st.set_page_config(page_title="Diagnostic Tool - अष्टाध्यायी-यंत्र", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .diagnostic-card { background-color: #f0f4f8; border-left: 5px solid #1a73e8; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
    .sutra-ref { color: #d32f2f; font-weight: bold; font-family: 'Sanskrit Text', serif; }
    .component-box { display: inline-block; padding: 5px 10px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; background: #fff; }
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


# --- ३. Diagnostic Logic Engine (Etiology) ---
def get_component_breakdown(roop, lakara):
    """
    Surgical Breakdown: यह फंक्शन रूप को प्रकृति, प्रत्यय और आगम में तोड़ने का प्रयास करेगा।
    (वर्तमान में यह एक 'Template-based' लॉजिक है, जिसे हम सूत्रों से और परिष्कृत करेंगे)
    """
    # उदाहरण: भविष्यति विश्लेषण
    if "िष्यति" in roop:
        return {
            "धातु": "भू",
            "आगम": "इट् (इ)",
            "विकरण": "स्य (लृट्)",
            "प्रत्यय": "ति (तिप्)",
            "सूत्र": "आर्धधातुकस्येड्वलादेः (७.२.३५)"
        }
    return None


# --- ४. मुख्य इंटरफेस ---
if db_meta and db_roopa:
    col_a, col_b = st.columns([1, 2])

    with col_a:
        st.subheader("🔍 लक्षण (Selection)")
        search_roop = st.text_input("रूप लिखें (e.g., भवति, भविष्यति):")
        st.info("💡 यह इंजन रूप को स्कैन करके उसकी 'Etiology' का पता लगाएगा।")

    with col_b:
        st.subheader("🧬 निदान (Diagnosis)")
        if search_roop:
            # १. रूप को डेटाबेस में ढूंढना
            found = False
            for d_id, lakaras in db_roopa.items():
                for lak, grid in lakaras.items():
                    for pur, vach in grid.items():
                        for v_type, val in vach.items():
                            if search_roop in val:
                                found = True
                                st.success(f"प्राप्त: यह धातु ID **{d_id}** का **{lak}** लकार है।")

                                # २. प्रकृति-प्रत्यय विभाग (Breakdown)
                                breakdown = get_component_breakdown(search_roop, lak)
                                if breakdown:
                                    st.markdown("<div class='diagnostic-card'>", unsafe_allow_html=True)
                                    st.markdown("### 🛠️ अङ्ग-प्रत्यय विभाग")
                                    cols = st.columns(len(breakdown) - 1)
                                    for i, (key, value) in enumerate(list(breakdown.items())[:-1]):
                                        cols[i].markdown(f"**{key}**\n<div class='component-box'>{value}</div>",
                                                         unsafe_allow_html=True)
                                    st.markdown(
                                        f"**प्रमुख सूत्र:** <span class='sutra-ref'>{breakdown['सूत्र']}</span>",
                                        unsafe_allow_html=True)
                                    st.markdown("</div>", unsafe_allow_html=True)
                                break
                if found: break
            if not found:
                st.warning("यह रूप डेटाबेस में नहीं मिला।")

    # --- ५. Comparative Gana Analysis (तुलनात्मक विश्लेषण) ---
    st.divider()
    st.subheader("🆚 Comparative Gana Analysis")
    st.write("चुनें कि कौन से दो गणों की प्रक्रियाओं में आप अंतर देखना चाहते हैं:")

    # गण तुलना के लिए छोटा लॉजिक
    ganas = ["भ्वादि", "अदादि", "जुहोत्यादि", "दिवादि", "स्वादि", "तुदादि", "रुधादि", "तन्वादि", "क्र्यादि", "चुरादि"]
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        g1 = st.selectbox("गण १:", ganas, index=0)
    with g_col2:
        g2 = st.selectbox("गण २:", ganas, index=1)

    st.info(f"💡 {g1} और {g2} के बीच मुख्य अंतर **'विकरण' (Shap vs Luk)** का है।")

else:
    st.error("डेटा उपलब्ध नहीं है।")