"""
FILE: logic/subanta/s_1_1.py
TIMESTAMP: 2026-01-31 01:10:00 (IST)
PILLAR: Subanta Strategy (Prathama Ekavachana)
DESCRIPTION: Specialized engine for Case 1, Singular (Su~).
             Updated to handle separate stem/suffix arguments for VidhiEngine.
"""
from core.phonology import ad, sanskrit_varna_samyoga, Varna
from core.upadesha_registry import UpadeshaType
from logic.it_engine import ItEngine
from logic.vidhi.vidhi_engine import VidhiEngine

class SubantaEngine11:
    """
    STRATEGY: Prathama Vibhakti, Ekavachana (1.1)
    Suffix: Su~ (becomes 's', 'am', or deleted)
    """

    @staticmethod
    def derive(stem_str, anga_varnas, logger):
        """
        Derives 1.1 form.
        stem_str: String representation (e.g. "राम")
        anga_varnas: List of Varna objects (The Anga/Stem)
        logger: The PrakriyaLogger instance
        """

        # 1. Add Suffix 'Su~' (4.1.2)
        suffix = ad("सुँ")
        if logger:
            logger.add_step(anga_varnas + suffix, "4.1.2", description="Su-Pratyaya")

        # 2. It-Prakaran on Suffix (Clean Su -> s)
        clean_suffix, _ = ItEngine.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)

        if logger:
            logger.add_step(anga_varnas + clean_suffix, "1.3.2", description="It-Prakaranam (u removed)")

        # Analysis of the Anga
        antya_char = anga_varnas[-1].char if anga_varnas else ""

        # =========================================================
        # BRANCHING LOGIC
        # =========================================================

        # A. Irregular Bases (Apavada: Kroṣṭu)
        if "क्रोष्टु" in stem_str:
            # We combine for stubs that only take one argument
            curr_varnas = anga_varnas + clean_suffix
            curr_varnas, rule = VidhiEngine.apply_trijvadbhava_7_1_95(curr_varnas)
            if rule and logger: logger.add_step(curr_varnas, rule)
            # ... (Remaining irregular logic uses curr_varnas)
            return curr_varnas

        # B. Kinship Terms (Pitr, Matr etc.)
        elif any(x in stem_str for x in ["जामातृ", "पितृ", "भ्रातृ", "नृ", "मातृ", "स्वसृ", "धातृ", "कर्तृ"]):
            curr_varnas = anga_varnas + clean_suffix
            curr_varnas, rule = VidhiEngine.apply_anang_7_1_94(curr_varnas)
            # ... (Remaining kinship logic uses curr_varnas)
            return curr_varnas

        # F. General Cases (Rama, Jnana, etc.)
        else:
            # 1. Neuter A-ending (Jñānam)
            if antya_char == 'अ' and stem_str in ["ज्ञान", "फल", "वन", "पुष्प"]:
                # Apply 7.1.24: Su -> Am
                anga_varnas, clean_suffix, rule = VidhiEngine.apply_ato_am_7_1_24(anga_varnas, clean_suffix)
                if rule and logger:
                    # We pass empty description so logger fetches the full Sanskrit from SutraManager
                    logger.add_step(anga_varnas + clean_suffix, rule, description="")

                # Apply 6.1.107: a + am -> am
                curr_varnas, rule = VidhiEngine.apply_ami_purvah_6_1_107(anga_varnas, clean_suffix)
                if rule and logger:
                    logger.add_step(curr_varnas, rule, description="")

                return curr_varnas

            # 2. Standard Visarga Path (Rama -> Ramah)
            curr_varnas = anga_varnas + clean_suffix
            return SubantaEngine11._apply_visarga_finish(curr_varnas, logger)

    @staticmethod
    def _apply_visarga_finish(varnas, logger):
        """Standard sequence for non-neuter/non-lopa stems."""
        if varnas and varnas[-1].char == 'स्':
            varnas, rule = VidhiEngine.apply_rutva_8_2_66(varnas)
            if rule and logger: logger.add_step(varnas, rule)

            # Clean 'u' from 'Ru~'
            varnas, _ = ItEngine.run_it_prakaran(varnas, UpadeshaType.VIBHAKTI)
            if logger: logger.add_step(varnas, "1.3.2")

            varnas, rule = VidhiEngine.apply_visarga_8_3_15(varnas)
            if rule and logger: logger.add_step(varnas, rule)
        return varnas