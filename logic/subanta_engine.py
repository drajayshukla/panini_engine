"""
FILE: logic/subanta_engine.py
TIMESTAMP: 2026-01-30 23:59:00 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta) | PILLAR: Engine (Detailed Jas Handling + Sarvanama + Conflict Logic)
"""
from core.phonology import ad, sanskrit_varna_samyoga, Varna
from core.sup_registry import SupRegistry
from core.prakriya_logger import PrakriyaLogger
from logic.it_engine import ItEngine
from logic.vidhi import VidhiEngine
from logic.vidhi.subanta_vidhi import SubantaVidhi
from logic.vidhi.sarvanama_vidhi import SarvanamaVidhi
from logic.vidhi.sandhi_engine import SandhiEngine


class SubantaEngine:

    def generate_table(self, pratipadika_str):
        """Fast Mode: Generates 7x3 Table."""
        table = {}
        stem_template = ad(pratipadika_str)
        print(f"\n🌊 Generating Subanta Table for: {pratipadika_str}")

        for case in range(1, 8):
            forms = []
            for num in range(1, 4):
                res = self.derive_pada(stem_template[:], case, num, log=False)
                forms.append(res)
            table[case] = forms
            print(f"   Case {case}: {forms}")
        return table

    def derive_detailed(self, pratipadika_str, case, num):
        """Guru Mode: Returns the Logger."""
        stem = ad(pratipadika_str)
        logger = PrakriyaLogger()
        self.derive_pada(stem, case, num, log=True, logger=logger)
        return logger

    def derive_pada(self, stem, vibhakti, vacana, log=False, logger=None):
        """Core Derivation Logic."""

        # 1. Suffix Selection (4.1.2)
        data = SupRegistry.get_suffix(vibhakti, vacana)
        if not data: return "?"
        raw_sup, tags = data  # e.g., "जस्"
        suffix = ad(raw_sup)

        if log: logger.add_step(stem + suffix, "4.1.2")
        if log: logger.add_step(stem + suffix, "1.4.14")

        # 2. It-Prakaranam (Detailed Logic)
        suffix_str = sanskrit_varna_samyoga(suffix)

        # [SPECIAL HANDLING FOR JAS (1.3)]
        # We explicitly handle Jas to show 1.3.7 and 1.3.4 logs clearly
        if raw_sup == "जस्":
            # A. Apply Cutu (1.3.7) manually to show the step
            if suffix[0].char == 'ज्':
                suffix.pop(0)  # Remove J
                if log: logger.add_step(stem + suffix, "1.3.7")

            # B. Log 1.3.4 (The Prohibition of 1.3.3)
            # We don't change the suffix here, just log that 's' was saved
            if log: logger.add_step(stem + suffix, "1.3.4")

            clean_suffix = suffix

        # [STANDARD HANDLING]
        else:
            # Check protected list for other suffixes like Bhis, Shas, etc.
            protected_suffixes = ["भिस्", "शस्", "ङस्", "सुप्", "ओस्", "भ्यस्"]

            if suffix_str in protected_suffixes:
                clean_suffix = suffix
            else:
                clean_suffix, _ = ItEngine.run_it_prakaran(suffix, "VIBHAKTI")

        if clean_suffix: clean_suffix[0].sanjnas.update(tags)

        # Log generic change if not already logged above
        if raw_sup != "जस्" and log and suffix_str != sanskrit_varna_samyoga(clean_suffix):
            logger.add_step(stem + clean_suffix, "1.3.2")

        # --- 3. SARVANAMA & SPECIFIC VIDHIS ---
        stem_str = sanskrit_varna_samyoga(stem)
        is_sarva = SarvanamaVidhi.is_sarvanama(stem_str)

        rule_applied = None

        # [7.1.17] Jas -> Shi
        if is_sarva and vibhakti == 1 and vacana == 3:
            stem, clean_suffix, rule_applied = SarvanamaVidhi.apply_jasah_shi_7_1_17(stem, clean_suffix)

        # [7.1.14] Ne -> Smai
        elif is_sarva and vibhakti == 4 and vacana == 1:
            stem, clean_suffix, rule_applied = SarvanamaVidhi.apply_sarvanamnah_smai_7_1_14(stem, clean_suffix)

        # [7.1.15] Nasi -> Smat / Ni -> Smin
        elif is_sarva and vibhakti == 5 and vacana == 1:
            stem, clean_suffix, rule_applied = SarvanamaVidhi.apply_nasinyoh_smatsminau_7_1_15(stem, clean_suffix, True)
        elif is_sarva and vibhakti == 7 and vacana == 1:
            stem, clean_suffix, rule_applied = SarvanamaVidhi.apply_nasinyoh_smatsminau_7_1_15(stem, clean_suffix,
                                                                                               False)

        # [7.1.52] Am -> Sut
        elif is_sarva and vibhakti == 6 and vacana == 3:
            stem, clean_suffix, rule_applied = SarvanamaVidhi.apply_ami_sarvanamnah_sut_7_1_52(stem, clean_suffix)

        # Log if a specific Sarvanama rule fired
        if log and rule_applied:
            logger.add_step(stem + clean_suffix, rule_applied)

        # --- STANDARD RAMA RULES (If no Sarvanama override) ---
        if not rule_applied:
            # [7.1.9] Ato Bhisa Ais
            stem, clean_suffix, rule = SubantaVidhi.apply_ato_bhisa_ais_7_1_9(stem, clean_suffix)
            if log and rule: logger.add_step(stem + clean_suffix, rule)

        # --- 4. SANDHI SELECTION ---
        suffix_first = clean_suffix[0].char if clean_suffix else ""
        rule_sandhi = None

        # [NEW]: Case 1.3 (Rama + As) -> Uses 6.1.102 (Prathamayoh Purvasavarnah)
        # This handles Rāmāḥ explicitly
        if not rule_applied and vibhakti in [1, 2] and suffix_first == 'अ':
            stem, rule_sandhi = VidhiEngine.apply_aka_savarne_dirgha_6_1_101(stem, clean_suffix)
            rule_sandhi = "6.1.102"  # Override code to show Purvasavarna explicitly

        # [NEW LOGIC] Case 1.2: Rama + Au (Conflict Handling)
        elif stem[-1].char == 'अ' and suffix_first == 'औ':
            if log:
                logger.add_step(stem + clean_suffix, "6.1.102",
                                description="प्रथमयोः पूर्वसवर्णः इति पूर्वसवर्णदीर्घे प्राप्ते")
                logger.add_step(stem + clean_suffix, "6.1.104",
                                description="नादिचि इति निषेधः")
            stem, rule_sandhi = SandhiEngine.apply_vriddhi_rechi_6_1_88(stem, clean_suffix)

        # Standard Ai (Rāmaiḥ) -> Vriddhi
        elif suffix_first == 'ऐ':
            stem, rule_sandhi = SandhiEngine.apply_vriddhi_rechi_6_1_88(stem, clean_suffix)

        # Standard Savarna (Generic fallback)
        elif not rule_applied:
            stem, rule_sandhi = VidhiEngine.apply_aka_savarne_dirgha_6_1_101(stem, clean_suffix)

        if log and rule_sandhi: logger.add_step(stem + clean_suffix, rule_sandhi)

        # 5. Tripadi (Final Polish)
        full = stem + clean_suffix

        # Rutva (s -> r)
        full, rule_rutva = VidhiEngine.apply_rutva_8_2_66(full)
        if log and rule_rutva:
            code = "8.2.66" if "8.2.66" in rule_rutva else rule_rutva

            # Simulate intermediate Ru~ state
            temp_ru = full[:-1] + [Varna("र्"), Varna("उ"), Varna("ँ")]
            logger.add_step(temp_ru, code)
            logger.add_step(full, "1.3.2")

        # Visarga (r -> h)
        full, rule_visarga = VidhiEngine.apply_visarga_8_3_15(full)
        if log and rule_visarga:
            code = "8.3.15" if "8.3.15" in rule_visarga else rule_visarga
            logger.add_step(full, code)

        return sanskrit_varna_samyoga(full)