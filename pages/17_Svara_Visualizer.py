import streamlit as st
import pandas as pd

st.set_page_config(page_title="Svara Visualization Lab", layout="wide")

st.title("⚖️ Paninian Svara Visualizer (Sutras 1.2.27 - 1.2.32)")

# --- १. पैरामीटर सिलेक्शन ---
st.sidebar.header("🔬 Diagnostic Parameters")
kala = st.sidebar.selectbox("Kala (1.2.27):", ["ह्रस्व (1 मात्रा)", "दीर्घ (2 मात्रा)", "प्लुत (3 मात्रा)"])
pitch_type = st.sidebar.radio("Pitch (1.2.29-31):", ["उदात्त", "अनुदात्त", "स्वरित"])
nasality = st.sidebar.checkbox("अनुनासिक (Nasality)")

# --- २. कैलकुलेशन इंजन ---
# कुल १८ भेद: 3 (काल) * 3 (स्थान) * 2 (अनुनासिक)
base_matra = {"ह्रस्व (1 मात्रा)": 1.0, "दीर्घ (2 मात्रा)": 2.0, "प्लुत (3 मात्रा)": 3.0}[kala]

st.subheader(f"📊 {kala} {pitch_type} का विश्लेषण")

col1, col2 = st.columns([1, 1])

with col1:
    if pitch_type == "स्वरित":
        st.info("💡 सूत्र 1.2.32: तस्यादित उदात्तमर्धह्रस्वम्")
        st.write(f"प्रथम {base_matra/2} मात्रा: **उदात्त** (High Pitch)")
        st.write(f"अन्तिम {base_matra/2} मात्रा: **अनुदात्त** (Low Pitch)")
    else:
        st.write(f"सम्पूर्ण {base_matra} मात्रा: **{pitch_type}**")

with col2:
    # सिम्युलेटेड ग्राफ डेटा
    time_points = [0, base_matra/2, base_matra]
    if pitch_type == "उदात्त": pitch_levels = [10, 10, 10]
    elif pitch_type == "अनुदात्त": pitch_levels = [2, 2, 2]
    else: pitch_levels = [10, 10, 2] # स्वरित drops from 10 to 2

    chart_data = pd.DataFrame({"Time (Matra)": time_points, "Pitch Level": pitch_levels})
    st.line_chart(chart_data, x="Time (Matra)", y="Pitch Level")

# --- ३. १८ भेदों की मास्टर तालिका ---
st.divider()
st.subheader("🧬 स्वर वर्गीकरण (18 Types of Vowels)")
st.markdown("सूत्रों के अनुसार प्रत्येक अच् (जैसे 'अ') के १८ रूप होते हैं:")

categories = []
for k in ["ह्रस्व", "दीर्घ", "प्लुत"]:
    for p in ["उदात्त", "अनुदात्त", "स्वरित"]:
        for n in ["अननुनासिक", "अनुनासिक"]:
            categories.append({"काल": k, "Pitch": p, "नासिका": n})

st.dataframe(pd.DataFrame(categories), use_container_width=True)

st.divider()