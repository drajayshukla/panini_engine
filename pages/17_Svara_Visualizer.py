import streamlit as st
import pandas as pd

# --- १. पेज सेटअप ---
st.set_page_config(page_title="Paninian Svara Lab", layout="wide", page_icon="⚖️")

st.title("⚖️ Paninian Svara & Vowel Matrix Lab")
st.caption("Sutras: 1.1.8 (Nasality) | 1.2.27 (Kala) | 1.2.29-31 (Pitch) | 1.2.32 (Svarit Structure)")

# --- २. साइडबार: डायग्नोस्टिक पैरामीटर्स ---
st.sidebar.header("🔬 Diagnostic Engine")
vowel_choice = st.sidebar.selectbox("Vowel (अच्) चुनें:", ["अ", "इ", "उ", "ऋ", "ऌ", "ए", "ऐ", "ओ", "औ"])

# अष्टाध्यायी प्रतिबंध (Constraints 1.1.8)
has_dirgha = vowel_choice != "ऌ"
has_hrasva = vowel_choice not in ["ए", "ऐ", "ओ", "औ"]

# काल विकल्प
kala_list = []
if has_hrasva: kala_list.append("ह्रस्व (1 मात्रा)")
if has_dirgha: kala_list.append("दीर्घ (2 मात्रा)")
kala_list.append("प्लुत (3 मात्रा)")

selected_kala = st.sidebar.selectbox("Kala (काल) चुनें:", kala_list)
selected_pitch = st.sidebar.radio("Pitch (स्थान) चुनें:", ["उदात्त", "अनुदात्त", "स्वरित"])
is_nasal = st.sidebar.checkbox("अनुनासिक (Nasality) सक्रिय करें")

# --- ३. सेक्शन १: पिच विज़ुअलाइज़र (Graph & Demo) ---
st.header("📊 Section 1: Pitch & Duration Analysis")
base_matra = {"ह्रस्व (1 मात्रा)": 1.0, "दीर्घ (2 मात्रा)": 2.0, "प्लुत (3 मात्रा)": 3.0}[selected_kala]

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"विश्लेषण: {vowel_choice} ({selected_kala})")
    nasal_status = "मुख + नासिका (1.1.8)" if is_nasal else "केवल मुख"
    st.write(f"**नासिका स्थिति:** {nasal_status}")

    if selected_pitch == "स्वरित":
        st.info("💡 सूत्र 1.2.32: तस्यादित उदात्तमर्धह्रस्वम्")
        st.write(f"प्रथम {base_matra / 2} मात्रा: **उदात्त** (High)")
        st.write(f"अन्तिम {base_matra / 2} मात्रा: **अनुदात्त** (Low)")
    else:
        st.write(f"सम्पूर्ण {base_matra} मात्रा का स्वर: **{selected_pitch}**")

with col2:
    # ग्राफ डेटा निर्माण
    time_pts = [0, base_matra / 2, base_matra]
    if selected_pitch == "उदात्त":
        p_lvls = [10, 10, 10]
    elif selected_pitch == "अनुदात्त":
        p_lvls = [2, 2, 2]
    else:
        p_lvls = [10, 10, 2]  # स्वरित drops from 10 to 2

    chart_df = pd.DataFrame({"Time (Matra)": time_pts, "Pitch (Hz)": p_lvls})
    st.line_chart(chart_df, x="Time (Matra)", y="Pitch (Hz)")

st.divider()

# --- ४. सेक्शन २: कॉम्प्रिहेंसिव मैट्रिक्स (Matrix Engine) ---
st.header("🧬 Section 2: Full Vowel Matrix (The 18-Fold Logic)")

# डायनेमिक गणना (१.१.८ के आधार पर)
matrix_data = []
for k in ["ह्रस्व", "दीर्घ", "प्लुत"]:
    # प्रतिबंध लागू करना
    if k == "ह्रस्व" and not has_hrasva: continue
    if k == "दीर्घ" and not has_dirgha: continue

    for p in ["उदात्त", "अनुदात्त", "स्वरित"]:
        for n in ["अननुनासिक", "अनुनासिक"]:
            matrix_data.append({"Kala (1.2.27)": k, "Pitch (1.2.29-31)": p, "Nasality (1.1.8)": n})

st.subheader(f"🎯 स्वर '{vowel_choice}' के कुल {len(matrix_data)} शास्त्रीय भेद")

if vowel_choice == "ऌ":
    st.warning("💡 सूत्र १.१.८: ऌवर्णस्य द्वादश, तस्य दीर्घाभावात् (दीर्घ का अभाव)")
elif not has_hrasva:
    st.warning("💡 सूत्र १.१.८: एचामपि द्वादश, तेषां ह्रस्वाभावात् (ह्रस्व का अभाव)")

st.dataframe(pd.DataFrame(matrix_data), use_container_width=True)

# --- ५. विज़ुअलाइज़ेशन (Morphological Context) ---
st.divider()

st.caption("यह मैट्रिक्स 'अन्तरतम' (1.1.50) परीक्षा के लिए इंजन द्वारा उपयोग की जाती है।")