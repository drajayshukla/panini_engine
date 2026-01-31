import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

# ───────────────────────────────────────────────
#  Page Configuration
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="शब्द-रूप सिद्धि यन्त्र",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ───────────────────────────────────────────────
#  Modern + Elegant CSS
# ───────────────────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

    :root {
        --primary: #6d28d9;
        --primary-dark: #5b21b6;
        --accent: #a78bfa;
        --text: #1e293b;
        --text-light: #64748b;
        --bg-card: #ffffff;
        --bg-light: #f8fafc;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Poppins', 'Noto Sans Devanagari', sans-serif !important;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }

    .stAppHeader, header {
        background: transparent !important;
    }

    h1, h2, h3 {
        color: var(--text);
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 2.8rem !important;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem;
    }

    .subtitle {
        color: var(--text-light);
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }

    /* Modern Card */
    .card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.8rem 2rem;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.08);
        border: 1px solid rgba(109,40,217,0.08);
        margin: 1.5rem 0;
        transition: all 0.28s ease;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px -15px rgba(109,40,217,0.15);
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: var(--primary);
        margin: 1.8rem 0 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 3px solid var(--accent);
        display: inline-block;
    }

    /* Input area */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 14px 16px !important;
        font-size: 1.05rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(109,40,217,0.15);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary), var(--primary-dark));
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem !important;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.25s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(109,40,217,0.3);
    }

    /* Sanskrit strong emphasis */
    .sanskrit {
        font-family: 'Noto Sans Devanagari', serif;
        font-weight: 700;
        color: #1e293b;
        font-size: 1.45rem;
        letter-spacing: 0.5px;
    }

    /* Viccheda tiles */
    .viccheda-container {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
        align-items: center;
    }
    .varna-tile {
        background: white;
        border: 1px solid #cbd5e1;
        color: #c2410c;
        padding: 0.55rem 1rem;
        border-radius: 10px;
        font-family: 'Noto Sans Devanagari', monospace;
        font-size: 1.25rem;
        font-weight: 500;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .plus-sign {
        color: #94a3b8;
        font-weight: bold;
        font-size: 1.4rem;
        margin: 0 0.2rem;
    }

    /* Badge */
    .badge {
        background: linear-gradient(90deg, var(--primary), var(--accent));
        color: white;
        padding: 0.35rem 1rem;
        border-radius: 2rem;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 0.8rem;
    }

    hr {
        margin: 2.2rem 0;
        border-color: #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  Constants
# ───────────────────────────────────────────────
VIBHAKTI_MAP = {
    1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी",
    5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"
}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

# ───────────────────────────────────────────────
#  UI
# ───────────────────────────────────────────────
st.markdown("<h1>🕉️ शब्द-रूप सिद्धि यन्त्र</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">पाणिनीय व्याकरण की प्रक्रिया को पारदर्शी रूप से समझें</div>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────
with st.sidebar:
    st.header("प्रातिपदिक इनपुट")
    stem = st.text_input("प्रातिपदिक", value="राम", help="वर्तमान में अकारान्त पुल्लिङ्ग शब्दों के लिए अनुकूलित")

    st.info("⚡ अकारान्त पुल्लिंग शब्द (राम, देव, हरि आदि)")

# ── Main Content ──────────────────────────────────
if stem.strip():
    # Full Table (beautiful expander)
    with st.expander("📊 पूर्ण शब्द-रूप तालिका", expanded=True):
        table_data = []
        for v in range(1, 9):
            row = {"विभक्ति": VIBHAKTI_MAP[v]}
            for n in range(1, 4):
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

    # ── Process Inspector ─────────────────────────────
    st.markdown('<div class="section-title">🔬 सिद्धि प्रक्रिया (Step-by-Step)</div>', unsafe_allow_html=True)

    col1, col2, _ = st.columns([2, 2, 3])
    with col1:
        sel_vib = st.selectbox("विभक्ति", options=list(VIBHAKTI_MAP.keys()),
                               format_func=lambda x: VIBHAKTI_MAP[x],
                               index=0)
    with col2:
        sel_vac = st.selectbox("वचन", options=list(VACANA_MAP.keys()),
                               format_func=lambda x: VACANA_MAP[x],
                               index=0)

    if st.button("🚀 सिद्ध पद & प्रक्रिया देखें", type="primary", use_container_width=True):
        with st.spinner("पाणिनि सूत्र चल रहे हैं..."):
            logger = PrakriyaLogger()
            final_res = SubantaProcessor.derive_pada(stem, sel_vib, sel_vac, logger)

            st.success(f"**सिद्ध पद →**  <span class='sanskrit'>{final_res}</span>", unsafe_allow_html=True)

            history = logger.get_history()

            if not history:
                st.info("कोई प्रक्रिया चरण उपलब्ध नहीं है।")
            else:
                for i, step in enumerate(history, 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="card">
                            <div class="badge">चरण {i}  •  सूत्र: {step['rule']}</div>
                            <div style="font-size:1.15rem; font-weight:600; margin:0.8rem 0;">
                                {step['operation']}
                            </div>
                        """, unsafe_allow_html=True)

                        # Improved viccheda tiles
                        if step.get('viccheda'):
                            parts = step['viccheda'].split(' + ')
                            tiles = ''.join([
                                f'<span class="varna-tile">{p}</span>'
                                if j == len(parts) - 1 else
                                f'<span class="varna-tile">{p}</span><span class="plus-sign">+</span>'
                                for j, p in enumerate(parts)
                            ])
                            st.markdown(f"""
                                <div class="viccheda-container">
                                    {tiles}
                                </div>
                            """, unsafe_allow_html=True)

                        st.markdown(f"""
                            <div style="margin-top:1.2rem; padding-top:1rem; border-top:1px dashed #e2e8f0;">
                                <strong style="color:var(--text-light);">वर्तमान अवस्था → </strong>
                                <span class="sanskrit">{step['result']}</span>
                            </div>
                            </div>
                        """, unsafe_allow_html=True)

else:
    st.warning("कृपया प्रातिपदिक प्रविष्ट करें (उदा. राम, देव, गुरु…)")

st.markdown("<br><br>", unsafe_allow_html=True)