"""
FILE: core/sanjna_engine.py
PAS-v2.0: 5.0 (Siddha)
ROLE: The Sanjñā Orchestrator & Query Interface
"""

from core.pratyahara_engine import PratyaharaEngine
# We import the strict logic we defined in the logic layer
import logic.sanjna_rules as rules

# Initialize the Zone 1 Decoder
pe = PratyaharaEngine()


class SanjnaEngine:
    """
    अथ संज्ञा-प्रकरणम्: The Definition Engine.
    Role 1: Query Interface (is_hal?) for Sandhi/Analyzer.
    Role 2: Process Orchestrator (run_prakaranam) for Derivation.
    """

    # --- ROLE 1: The Query Interface (Fast Boolean Checks) ---

    @staticmethod
    def is_vriddhi_1_1_1(char: str) -> bool:
        """[Query]: Is this char Vriddhi? (Used by Analyzer/Sandhi)"""
        return char == 'आ' or pe.is_in(char, "ऐच्")

    @staticmethod
    def is_guna_1_1_2(char: str) -> bool:
        """[Query]: Is this char Guna?"""
        return char == 'अ' or pe.is_in(char, "एङ्")

    @staticmethod
    def is_hal(char: str) -> bool:
        """[Query]: Is this a Consonant?"""
        return pe.is_in(char, "हल्")

    @staticmethod
    def is_ac(char: str) -> bool:
        """[Query]: Is this a Vowel?"""
        return pe.is_in(char, "अच्")

    @staticmethod
    def is_samyoga_1_1_7(varna_list: list) -> bool:
        """[Query]: Is this block a Conjunct?"""
        if len(varna_list) < 2: return False
        # Robust check handles both Varna objects and raw strings
        return all(SanjnaEngine.is_hal(v.char if hasattr(v, 'char') else v) for v in varna_list)

    # --- ROLE 2: The Process Orchestrator (Active Labeling) ---

    @staticmethod
    def run_sanjna_prakaranam(varna_list):
        """
        [PROCESS]: Orchestrates the ordered application of rules 1.1.x - 1.4.x.
        This modifies the Varna objects in-place with 'trace' and 'sanjnas'.
        """
        # 1. Apply Definitions (1.1.x)
        varna_list = rules.apply_1_1_1_vriddhi(varna_list)
        varna_list = rules.apply_1_1_2_guna(varna_list)
        varna_list = rules.apply_1_1_7_samyoga(varna_list)

        # 2. Apply It-Sanjna is handled by ItEngine, but if there were 
        # specific Svarita/Udatta marking rules, they would go here.

        return varna_list