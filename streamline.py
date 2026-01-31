"""
FILE: update_landing_page.py
PURPOSE: Update app.py to reflect the expanded 34 Strategic Pillars (A1-A2, R1-R32).
"""
import os
import sys

NEW_APP_CODE = '''import streamlit as st

# --- 1. पेज कॉन्फ़िगरेशन ---
st.set_page_config(
    page_title="Pāṇinian Engine",
    page_icon="🕉️",
    layout="wide"
)

# --- 2. CSS स्टाइलिंग (Premium Look) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    
    body { font-family: 'Noto Sans', sans-serif; background-color: #fcfcfc; }
    
    .big-title { 
        font-family: 'Martel', serif; 
        font-size: 3.5rem; 
        font-weight: 800; 
        color: #8e44ad; 
        text-align: center; 
        margin-bottom: 0px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle { 
        font-size: 1.4rem; 
        text-align: center; 
        color: #555; 
        margin-top: -10px; 
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    .pillar-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #8e44ad;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .pillar-card:hover {
        transform: translateX(5px);
        background-color: #fdfbff;
    }
    
    .pillar-id {
        font-weight: bold;
        color: #8e44ad;
        margin-right: 8px;
    }
    
    .pillar-desc {
        color: #2c3e50;
        font-weight: 500;
    }

    .auth-box {
        background: linear-gradient(135deg, #f3e5f5, #e1bee7);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #d1c4e9;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # --- हेडर ---
    st.markdown('<p class="big-title">🕉️ The Pāṇinian Engine</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">A "Glassbox" Computational Approach to Sanskrit Grammar</p>', unsafe_allow_html=True)
    
    st.divider()

    # --- मिशन सेक्शन ---
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("🎯 Mission Statement")
        st.markdown("""
        This project is a precision-engineered implementation of **Maharshi Pāṇini's Aṣṭādhyāyī**. 
        Unlike "Blackbox" AI models that guess patterns based on statistics, this engine strictly follows the 
        **4,000 algorithmic rules** encoded 2,500 years ago.
        
        It currently masters the **Subanta (Nominal Declension)** process for *Rāma-shabda*, achieving **100% SIDDHA status** (verified by 29/29 regression tests).
        """)
        
        st.info("👈 **To start using the tool:** Select **'🔍 Declension_Engine'** from the sidebar.")

    with c2:
        # Placeholder for Panini Image or Logo
        st.markdown(
            """
            <div style="text-align: center; background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
                <div style="font-size: 4rem;">📜</div>
                <div style="margin-top: 10px; font-weight: bold; color: #555;">Sutra-Siddha Code</div>
            </div>
            """, unsafe_allow_html=True
        )

    st.divider()

    # --- 34 STRATEGIC PILLARS ---
    st.subheader("🏛️ The 34 Strategic Pillars (Architecture)")
    st.markdown("The engine's kernel is grounded in these immutable axioms:")

    with st.expander("📜 View All 34 Pillars (A1-A2, R1-R32)", expanded=True):
        
        # --- Authority (Axioms) ---
        st.markdown("### 👑 Authority (Pramāṇa)")
        st.markdown("""
        <div class="auth-box">
            <div><span class="pillar-id">A1:</span> <b>Follow Pāṇini, Kātyāyana, Patañjali, Bhartṛhari, Bhaṭṭojī Dīkṣita, and Nāgeśa Bhaṭṭa mathematically.</b></div>
            <div style="margin-top:10px;"><span class="pillar-id">A2:</span> <b>If confusion, read A1 again.</b></div>
        </div>
        """, unsafe_allow_html=True)

        # --- Rules (R1-R32) ---
        st.markdown("### ⚙️ Algorithmic Rules (Sūtra-Tantra)")
        
        col_a, col_b = st.columns(2)
        
        pillars_left = [
            ("R1", "Upadeśa (Data Initialization)"),
            ("R2", "Varṇaviccheda (Atomic Tokenization)"),
            ("R3", "Saṃjñā (Class Tagging/OOP)"),
            ("R4", "Anubandha (Metadata IT-Flags)"),
            ("R5", "Anuvṛtti (Recursive Persistence)"),
            ("R6", "Sthānyādeśa (Substitution Mapping)"),
            ("R7", "Paribhāṣā (Spatial Logic/Context)"),
            ("R8", "Balīyaḥ (Conflict Resolution)"),
            ("R9", "Asiddhatvam (Tripādī Isolation)"),
            ("R10", "Sūtra-bheda (Taxonomy)"),
            ("R11", "Niyama (Constraint Validation)"),
            ("R12", "Adhikāra (Governing Headers)"),
            ("R13", "Sthānivadbhāva (Property Inheritance)"),
            ("R14", "Antaraṅga-Bahiraṅga (Proximity Logic)"),
            ("R15", "Jñāpaka (Inference from Redundancy)"),
            ("R16", "Yogavibhāga (Rule Refactoring)")
        ]
        
        pillars_right = [
            ("R17", "Lakṣya-Lakṣaṇa (Empirical Validation/TDD)"),
            ("R18", "Kārakānvaya (Semantic Dependency)"),
            ("R19", "Vivakṣā (User Intent/Runtime Params)"),
            ("R20", "Arthabheda (Context-Aware Middleware)"),
            ("R21", "Sannipāta (Consistency/Non-Destruction)"),
            ("R22", "Pratyaya-Lopa (Ghost-Metadata Persistence)"),
            ("R23", "Tad-anta-Vidhi (Extension Logic)"),
            ("R24", "Sthāna-Antaratamya (Physics of Phonetics)"),
            ("R25", "Paratva (Chronological Priority)"),
            ("R26", "Ekādeśa (Fusion/Morphing)"),
            ("R27", "Bahiraṅga (External-Weight Logic)"),
            ("R28", "Lakṣaṇa-Pratipado-kta (Specificity Principle)"),
            ("R29", "Anuvṛtti-Sthiti (State Memory)"),
            ("R30", "Sthānivad-bhāva (Property-Parity Check)"),
            ("R31", "Nivṛtti (De-activation/Boundary Logic)"),
            ("R32", "Pratyākhyāna (Redundancy-Rejection)")
        ]

        with col_a:
            for pid, pdesc in pillars_left:
                st.markdown(f'<div class="pillar-card"><span class="pillar-id">{pid}:</span><span class="pillar-desc">{pdesc}</span></div>', unsafe_allow_html=True)

        with col_b:
            for pid, pdesc in pillars_right:
                st.markdown(f'<div class="pillar-card"><span class="pillar-id">{pid}:</span><span class="pillar-desc">{pdesc}</span></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(NEW_APP_CODE)

print("🚀 app.py Updated with 34 Strategic Pillars. Refresh the main page!")