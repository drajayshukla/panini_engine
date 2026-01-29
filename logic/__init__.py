"""
FILE: logic/__init__.py
PAS-v2.0: 5.0 (Siddha)
ROLE: The Legal Interface (Exposing the Shastric Laws)
"""

# --- १. संज्ञा-प्रकरणम् (Definitions & Technical Labels) ---
# Sourced from the consolidated PAS-5 'logic/sanjna_rules.py'

from .sanjna_rules import (
    # Section 1.1: Foundations
    apply_1_1_1_vriddhi,  # वृद्धिरादैच्
    apply_1_1_2_guna,  # अदेङ्गुणः
    apply_1_1_7_samyoga,  # हलोऽनन्तराः संयोगः

    # Section 1.3: It-Sanjna (Markers)
    apply_1_3_2_ajanunasika,  # उपदेशेऽजनुनासिक इत्
    apply_1_3_3_halantyam,  # हलन्त्यम्
    apply_1_3_4_na_vibhaktau,  # न विभक्तौ तुस्माः
    apply_1_3_5_adir_nitudavah,  # आदिर्ञिटुडवः
    apply_1_3_8_lashakva,  # लशक्वतद्धिते

    # Section 1.4: Pada
    apply_1_4_14_pada  # सुप्तिङन्तं पदम्
)

# --- २. अतिदेश (Extension Logic) ---
# Used for 1.1.56 Stahnivadbhava
# (Ensure core/atidesha_mapper.py is accessible via core, 
# but if specific logic rules exist here, expose them.)

# --- ३. सन्धि (Sandhi - Future Zone 2) ---
# from .sandhi_rules import ...