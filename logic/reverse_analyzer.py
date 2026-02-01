"""
FILE: logic/reverse_analyzer.py
"""
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor
from core.knowledge_base import KnowledgeBase

class ReverseAnalyzer:
    # Knowledge of supported stems
    SUPPORTED_STEMS = ["राम", "हरि", "गुरु", "रमा"]
    
    @staticmethod
    def analyze_word(target_word):
        """
        Scans all declensions of supported stems to find the target word.
        Returns a list of matches (handling ambiguities like 5.1/6.1).
        """
        matches = []
        clean_target = target_word.strip()
        
        # Brute-force scan (Optimization: Fast because scope is limited)
        for stem in ReverseAnalyzer.SUPPORTED_STEMS:
            for vib in range(1, 9):
                for vac in range(1, 4):
                    # 1. Derive silently first
                    # We pass None logger to be fast
                    result = SubantaProcessor.derive_pada(stem, vib, vac, None)
                    
                    # 2. Check Match
                    if result == clean_target:
                        # 3. If Match, Derive AGAIN with Logger to capture steps
                        logger = PrakriyaLogger()
                        SubantaProcessor.derive_pada(stem, vib, vac, logger)
                        
                        # Get Pratyaya Name (e.g., Su, Au, Jas)
                        sup_raw, _ = KnowledgeBase.get_sup(vib, vac)
                        
                        match_data = {
                            "stem": stem,
                            "vibhakti": vib,
                            "vacana": vac,
                            "pratyaya": sup_raw,
                            "history": logger.get_history() # Forward history
                        }
                        matches.append(match_data)
        
        return matches
