import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="Pāṇinian Engine",
    page_icon="🕉️",
    layout="wide"
)

# --- Styling ---
st.markdown("""
<style>
    .big-title { font-size: 3rem; font-weight: 800; color: #8e44ad; text-align: center; }
    .subtitle { font-size: 1.2rem; text-align: center; color: #555; }
    .feature-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #8e44ad; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)


def main():
    st.markdown('<p class="big-title">🕉️ The Pāṇinian Engine</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">A "Glassbox" Computational Approach to Sanskrit Grammar</p>',
                unsafe_allow_html=True)

    st.divider()

    c1, c2 = st.columns([2, 1])

    with c1:
        st.header("🎯 Mission")
        st.write("""
        This project is a precision-engineered implementation of **Pāṇini's Aṣṭādhyāyī**. 
        Unlike "Blackbox" AI models that guess patterns, this engine strictly follows the 
        4,000 algorithmic rules encoded 2,500 years ago.

        It currently masters the **Subanta (Nominal Declension)** process for *Rāma-shabda* (Masculine a-stem), achieving **100% SIDDHA status** across all 8 Vibhaktis.
        """)

        st.info("👈 Select **'Declension Engine'** from the sidebar to use the tool.")

    with c2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Panini_statue.jpg/440px-Panini_statue.jpg",
                 caption="Maharshi Pāṇini")

    st.divider()

    st.header("🏛️ The 20 Strategic Pillars")
    st.write("The engine architecture is grounded in these immutable principles:")

    with st.expander("View the 20 Pillars of Logic"):
        st.markdown("""
        1. **Upadeśa**: Raw data initialization.
        2. **Varṇaviccheda**: Atomic tokenization.
        3. **Saṃjñā**: Class tagging (OOP logic).
        4. **Anubandha**: Metadata flags (IT markers).
        5. **Anuvṛtti**: Recursive state persistence.
        6. **Sthānyādeśa**: Substitution mapping.
        7. **Paribhāṣā**: Spatial/Context logic.
        8. **Balīyaḥ**: Conflict resolution hierarchy.
        9. **Asiddhatvam**: The Tripādī "invisibility" wall.
        10. **Sūtra-bheda**: Taxonomy of rules.
        11. **Niyama**: Constraint validation.
        12. **Adhikāra**: Governing headers.
        13. **Sthānivadbhāva**: Inheritance of properties.
        14. **Antaraṅga-Bahiraṅga**: Proximity priority.
        15. **Jñāpaka**: Inference from redundancy.
        16. **Yogavibhāga**: Rule splitting.
        17. **Lakṣya-Lakṣaṇa**: Empirical validation (TDD).
        18. **Kārakānvaya**: Semantic dependency mapping.
        19. **Vivakṣā**: User intent (Speaker's desire).
        20. **Arthabheda**: Semantic middleware.
        """)


if __name__ == "__main__":
    main()