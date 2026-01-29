import streamlit as st
import pandas as pd
from logic.prakriya_engine import PrakriyaEngine

# --- CONFIG ---
st.set_page_config(page_title="Taddhita Siddhi", page_icon="⚡", layout="wide")
st.title("⚡ Taddhita Lab: Secondary Derivatives")
st.markdown("---")

# --- SIDEBAR INPUT ---
with st.sidebar:
    st.header("Derivation Settings")
    base_word = st.text_input("Pratipadika (Base)", value="उपगु")
    suffix = st.selectbox("Taddhita Pratyaya", ["अण्", "ढक्", "यत्", "छ"])

    st.info("""
    **Common Examples:**
    * उपगु + अण् = औपगव
    * भृगु + अण् = भार्गव
    * कुरु + अण् = कौरव
    """)

# --- MAIN LOGIC ---
if base_word and suffix:
    st.subheader(f"Deriving: {base_word} + {suffix}")

    # 1. Initialize Engine
    engine = PrakriyaEngine()

    # 2. Run Recipe
    # Note: Currently supports 'Aṇ' logic generally.
    # Logic for Dhak/Yat would need new recipes in PrakriyaEngine later.
    final_form = engine.derive_taddhita(base_word, suffix)

    # 3. Display Result
    st.success(f"### Siddha Rupa: **{final_form}**")

    # 4. Show Step-by-Step Table
    history = engine.get_history()

    if history:
        st.write("### 🧬 Derivation Trace")

        # Format for Streamlit
        data = []
        for step in history:
            data.append({
                "Step": step["step"],
                "Rule": step["rule"],
                "Operation": step["description"],
                "Result": step["form"]
            })

        st.table(pd.DataFrame(data))

    # 5. Visual Explainer
    st.markdown("---")
    st.caption("Morphological Path:")
    steps = [h['form'] for h in history]
    st.code(" → ".join(steps))