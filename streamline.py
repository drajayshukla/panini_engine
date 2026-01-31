"""
FILE: upgrade_ui_final.py
PURPOSE: Apply the final 'Premium' UI with Atomic Tiles, Authority Citations, and fixed HTML logic.
"""
import os
import sys

# ==============================================================================
# FINAL PREMIUM UI CODE
# ==============================================================================
NEW_UI_CODE = '''import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

# --- 1. पेज कॉन्फ़िगरेशन ---
st.set_page_config(
    page_title="शब्द-रूप सिद्धि यन्त्र",
    page_icon="🕉️",
    layout="wide"
)

# --- 2. आधुनिक CSS (Modern Styling) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans', sans-serif;
    }

    /* संस्कृत टेक्स्ट */
    .sanskrit-text {
        font-family: 'Martel', serif;
        font-weight: 800;
        color: #2c3e50;
    }

    /* चरण कार्ड (Step Card) */
    .step-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #8e44ad;
        transition: transform 0.2s;
    }
    .step-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
    }

    /* सूत्र बैज */
    .rule-badge {
        background: linear-gradient(135deg, #8e44ad, #9b59b6);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
    }

    /* ऋषि उद्धरण (Authority Citation) */
    .auth-text {
        font-size: 0.75rem;
        color: #8e44ad;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        float: right;
        margin-top: 4px;
    }

    /* ऑपरेशन हेडर */
    .op-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #34495e;
        margin: 12px 0;
    }

    /* वर्ण विच्छेद कंटेनर */
    .viccheda-container {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
        display: flex;
        flex-wrap: wrap;
        gap: 8px; /* टाइल्स के बीच गैप */
        align-items: center;
    }
    
    /* वर्ण टाइल (Atomic Tile) */
    .varna-tile {
        background-color: #ffffff;
        border: 1px solid #bdc3c7;
        color: #d35400;
        padding: 6px 10px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 2px 2px rgba(0,0,0,0.05);
    }
    
    .plus-sign {
        color: #95a5a6;
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: -3px;
    }

    /* परिणाम अनुभाग */
    .result-section {
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px dashed #ecf0f1;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .result-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .result-value {
        font-size: 1.6rem;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. डेटा ---
VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def main():
    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र")
    st.markdown("### पाणिनीय व्याकरण का 'ग्लास-बॉक्स' विश्लेषण")
    st.markdown("---")

    # --- साइडबार ---
    with st.sidebar:
        st.header("🎛️ इनपुट")
        stem = st.text_input("प्रातिपदिक (Stem)", value="राम")
        st.info("ℹ️ केवल 'अकारांत पुल्लिंग' (जैसे राम, देव) के लिए अनुकूलित।")

    # --- तालिका (Table Logic Restored) ---
    if stem:
        with st.expander("📖 पूरी तालिका देखें (Show Full Table)", expanded=True):
            table_data = []
            for v in range(1, 9):
                row = {"विभक्ति": VIBHAKTI_MAP[v]}
                for n in range(1, 4):
                    # लॉगर के बिना कॉल करें (केवल शब्द पाने के लिए)
                    word = SubantaProcessor.derive_pada(stem, v, n, None)
                    row[VACANA_MAP[n]] = word
                table_data.append(row)
            
            df = pd.DataFrame(table_data)
            st.dataframe(
                df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "विभक्ति": st.column_config.TextColumn("विभक्ति", width="medium"),
                    "एकवचनम्": st.column_config.TextColumn("एकवचनम्", width="large"),
                    "द्विवचनम्": st.column_config.TextColumn("द्विवचनम्", width="large"),
                    "बहुवचनम्": st.column_config.TextColumn("बहुवचनम्", width="large"),
                }
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- इंस्पेक्टर (Derivation Inspector) ---
    st.header("🔬 सिद्धि प्रक्रिया (Process Inspector)")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        sel_vib = st.selectbox("विभक्ति चुनें", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with col2:
        sel_vac = st.selectbox("वचन चुनें", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    with col3:
        st.write("")
        st.write("")
        derive_btn = st.button("🚀 सिद्धि देखें", type="primary", use_container_width=True)

    if derive_btn:
        logger = PrakriyaLogger()
        final_res = SubantaProcessor.derive_pada(stem, sel_vib, sel_vac, logger)
        
        st.success(f"सिद्ध पद: **{final_res}**")
        
        history = logger.get_history()
        
        for i, step in enumerate(history):
            # --- वर्ण विच्छेद विज़ुअलाइज़ेशन (Atomic Tiles) ---
            viccheda_html = ""
            if step['viccheda']:
                # 1. स्ट्रिंग को विभाजित करें (जैसे "र् + आ" -> ["र्", "आ"])
                parts = step['viccheda'].split(' + ')
                
                # 2. हर भाग को स्पैन में लपेटें
                tile_htmls = [f'<span class="varna-tile">{p}</span>' for p in parts]
                
                # 3. सुरक्षित रूप से जोड़ें (Join safely with separator)
                separator = '<span class="plus-sign">+</span>'
                final_html_str = separator.join(tile_htmls)
                
                viccheda_html = f"""
                <div style="font-size:0.8rem; color:#7f8c8d; margin-bottom:4px;">🔍 वर्ण-विश्लेषण (Atomic View):</div>
                <div class="viccheda-container">
                    {final_html_str}
                </div>
                """
            
            # --- ऋषि उद्धरण (Authority) ---
            source = step.get('source', 'Maharshi Pāṇini')

            # --- कार्ड रेंडरिंग ---
            st.markdown(f"""
            <div class="step-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="rule-badge">📖 सूत्र: {step['rule']}</span>
                    <span class="auth-text">— {source}</span>
                </div>
                
                <div class="op-header">{step['operation']}</div>
                
                {viccheda_html}
                
                <div class="result-section">
                    <span class="result-label">परिणाम (State)</span>
                    <span class="sanskrit-text result-value">{step['result']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
'''

with open("pages/1_🔍_Declension_Engine.py", "w", encoding="utf-8") as f:
    f.write(NEW_UI_CODE)

print("🚀 Premium UI Updated! Streamlit ऐप को Refresh (R) करें।")