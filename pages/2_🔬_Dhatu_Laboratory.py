import streamlit as st
import pandas as pd
from logic.dhatu_processor import DhatuDiagnostic
from core.core_foundation import sanskrit_varna_samyoga

st.set_page_config(page_title="धातु-प्रयोगशाला (Dhātu Lab)", page_icon="🔬", layout="wide")

# --- UI Styling ---
st.markdown("""
<style>
    .reportview-container { background: #fdfbfb; }
    .phase-card {
        background-color: white; border: 1px solid #e0e0e0;
        border-left: 5px solid #d35400; padding: 15px;
        border-radius: 10px; margin-bottom: 20px;
    }
    .rule-id { color: #d35400; font-weight: bold; font-family: 'Martel', serif; }
    .varna-badge {
        background-color: #fef5e7; border: 1px solid #f5c06b;
        padding: 2px 8px; border-radius: 5px; color: #b7950b; font-weight: bold;
    }
    .final-res { font-size: 2.5rem; font-family: 'Martel', serif; color: #1e8449; text-align: center; }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("🔬 धातु-प्रयोगशाला: Upadeśa to Action")
    st.markdown("### Task 2: Functional Root Transformation Engine")

    with st.sidebar:
        st.header("🧪 Input Diagnostic")
        raw_input = st.text_input("Enter Upadeśa (Raw Root)", value="डुकृञ्")
        st.info("Examples: डुकृञ्, ष्मिँ, णीञ्, भिदिँर्, नदिँ")

    if raw_input:
        # Run the Task 2 Logic
        diag = DhatuDiagnostic(raw_input)

        c1, c2 = st.columns([1, 2])

        with c1:
            st.subheader("📋 Root Identity")
            st.metric("Input (Upadeśa)", diag.raw)
            st.metric("Output (Functional)", diag.get_final_root())

            st.write("**Active Anubandha Markers:**")
            if diag.it_tags:
                for tag in diag.it_tags:
                    st.markdown(f'<span class="varna-badge">{tag}</span>', unsafe_allow_html=True)
            else:
                st.write("None")

        with c2:
            st.subheader("⚙️ Transformation Timeline (Prakriyā)")

            for step in diag.history:
                rule, desc = step.split(": ", 1)
                st.markdown(f"""
                <div class="phase-card">
                    <span class="rule-id">📖 Sūtra {rule}</span><br>
                    {desc}
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # --- PHASE 6: Classification Table ---
        st.subheader("📊 Dhātu Classification Matrix")
        final_root = diag.get_final_root()

        # Simple Logic to detect group for UI display
        category = "Ajanta" if final_root[-1] in "अआइईउऊऋॠएऐओऔ" else "Halanta"

        data = {
            "Parameter": ["Action Form", "Category", "Voice (Pada)", "It-Status"],
            "Value": [final_root, category, "Pending Task 3", "Seṭ (per DB)"]
        }
        st.table(pd.DataFrame(data))


if __name__ == "__main__":
    main()