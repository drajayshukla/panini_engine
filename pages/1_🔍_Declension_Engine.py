import streamlit as st
import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि यन्त्र", page_icon="🕉️", layout="wide")

# --- CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    body { font-family: 'Noto Sans', sans-serif; background-color: #f4f6f9; }

    /* Card Base */
    .step-card { 
        background-color: #ffffff; padding: 15px 20px; margin-bottom: 15px; 
        border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
        transition: transform 0.2s;
    }
    .step-card:hover { transform: translateY(-2px); }

    /* Color Coding based on Rule Type */
    .border-meta { border-left: 6px solid #2980b9; }   /* Blue for Definitions/Adhikara */
    .border-action { border-left: 6px solid #8e44ad; } /* Purple for Transformations */

    /* Badges */
    .rule-badge {
        padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 0.8rem;
        display: inline-block; margin-right: 8px; color: white;
    }
    .badge-meta { background-color: #2980b9; }
    .badge-action { background-color: #8e44ad; }

    /* Typography */
    .sutra-name {
        font-family: 'Martel', serif; font-weight: 800; font-size: 1.15rem; color: #2c3e50;
    }
    .op-text {
        font-size: 0.95rem; color: #555; margin-top: 6px; font-weight: 500;
    }
    .res-sanskrit { 
        font-family: 'Martel', serif; font-size: 1.6rem; font-weight: 800; color: #2c3e50; 
    }

    /* Varna Tiles (Sandhi Analysis) */
    .varna-tile { 
        background-color: #ecf0f1; border: 1px solid #bdc3c7; 
        padding: 2px 8px; border-radius: 4px; color: #e67e22; 
        font-family: 'Courier New', monospace; font-weight: bold; font-size: 0.9rem; 
        display:inline-block; margin:2px;
    }

    /* Step Counter */
    .step-num { font-size: 0.75rem; color: #95a5a6; font-weight: 700; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी",
                8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}


def get_card_style(rule_num):
    """Determines if a rule is Meta (Structural) or Action (Transformational)."""
    # Meta rules: 1.2.x (Sanjna), 1.4.x (Vibhakti/Vacana), 3.1.x (Pratyaya), 4.1.1 (Scope)
    if rule_num.startswith("1.2") or rule_num.startswith("1.4") or \
            rule_num.startswith("3.1") or rule_num.startswith("4.1.1"):
        return "border-meta", "badge-meta"
    return "border-action", "badge-action"


def generate_card_html(step_index, step_data):
    rule_full = step_data['rule']
    op = step_data['operation']
    res = step_data['result']
    viccheda = step_data['viccheda']
    vartika = step_data.get('vartika_html', '')

    # Split Number and Name
    if " " in rule_full:
        parts = rule_full.split(" ", 1)
        r_num = parts[0]
        r_name = parts[1]
    else:
        r_num = rule_full
        r_name = ""

    # Determine Style
    border_class, badge_class = get_card_style(r_num)

    # Viccheda Tiles
    viccheda_html = ""
    if viccheda:
        parts = viccheda.split(" + ")
        tiles = "".join([f'<div class="varna-tile">{p}</div>' for p in parts])
        viccheda_html = f"<div style='margin-top:8px;'>{tiles}</div>"

    # Link to Ashtadhyayi.com
    link = "#"
    if "." in r_num:
        try:
            c, p, s = r_num.split('.')
            link = f"https://ashtadhyayi.com/sutraani/{c}/{p}/{s}"
        except:
            pass

    return f"""
    <div class="step-card {border_class}">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div>
                <a href="{link}" target="_blank" style="text-decoration:none;">
                    <span class="rule-badge {badge_class}">📖 {r_num}</span>
                </a>
                <span class="sutra-name">{r_name}</span>
                {vartika}
                <div class="op-text">⚙️ {op}</div>
                {viccheda_html}
            </div>
            <div style="text-align:right; min-width: 80px;">
                <div class="step-num">STEP {step_index + 1}</div>
                <div class="res-sanskrit">{res}</div>
            </div>
        </div>
    </div>
    """


def main():
    st.title("🕉️ शब्द-रूप सिद्धि यन्त्र")
    st.markdown("### Paninian Derivation Engine")

    with st.sidebar:
        st.header("🎛️ इनपुट (Input)")
        stem = st.text_input("प्रातिपदिक (Stem)", value="राम")

        force_p = st.checkbox("Force Pratipadika", value=False,
                              help="Enable to bypass initial dictionary checks.")

        st.info("✅ **समर्थित:** राम, हरि, गुरु, रमा, इ, उ, तितउ, सर्व, विश्व...")
        st.markdown("---")
        st.markdown("**Color Code:**\n\n🔵 **Definitions/Scope**\n\n🟣 **Transformations**")

    # Main Action Area
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        v_sel = st.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    with c2:
        n_sel = st.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    with c3:
        st.write("");
        st.write("")
        btn = st.button("🚀 सिद्धि करें (Derive)", type="primary", use_container_width=True)

    if btn:
        logger = PrakriyaLogger()
        res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger, force_p)

        st.success(f"सिद्ध पद: **{res}**")

        # Display Cards
        for i, step in enumerate(logger.get_history()):
            st.markdown(generate_card_html(i, step), unsafe_allow_html=True)

    # Full Table Expansion (Bottom)
    if stem:
        with st.expander(f"📚 {stem} - सम्पूर्ण रूप सारिणी (Full Table)", expanded=False):
            data = []
            for v in range(1, 9):
                row = {"विभक्ति": VIBHAKTI_MAP[v]}
                for n in range(1, 4):
                    try:
                        w = SubantaProcessor.derive_pada(stem, v, n, None, force_p)
                    except:
                        w = "Error"
                    row[VACANA_MAP[n]] = w
                data.append(row)
            st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()