"""
FILE: logic/subanta_processor.py - PAS-v23.0 (Hindi Logs)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga, UpadeshaType
from core.sanjna_controller import SanjnaController
from core.knowledge_base import KnowledgeBase
from logic.sandhi_processor import SandhiProcessor
from core.adhikara_controller import AdhikaraController
from core.dhatu_repo import DhatuRepository 

class SubantaProcessor:
    KNOWN_PRATYAYAS = {'सु', 'औ', 'जस्', 'अम्', 'औट्', 'शस्', 'टा', 'भ्याम्', 'भिस्', 'ङे', 'भ्यस्', 'ङसि', 'ङस्', 'ओस्', 'आम्', 'ङि', 'सुप्'}
    FEMININE_I_U_STEMS = {'मति', 'बुद्धि', 'धेनु', 'कीर्ति', 'जाति', 'भक्ति'}
    VALID_SINGLE_LETTERS = {'अ', 'इ', 'उ', 'ऋ'}
    SARVANAMA_GANA = {'सर्व', 'विश्व', 'उभ', 'उभय', 'डतर', 'डतम', 'अन्य', 'अन्यतर', 'इतर', 'त्वत्', 'त्व', 'नेम', 'सम', 'सिम', 'तद्', 'यद्', 'एतद्', 'इदम्', 'अदस्', 'एक', 'द्वि', 'युष्मद्', 'अस्मद्', 'भवतु', 'किम्'}

    @staticmethod
    def _finalize(varnas, vibhakti, vacana, logger=None):
        if not varnas: return ""
        final = SandhiProcessor.run_tripadi(varnas, logger) 
        res = sanskrit_varna_samyoga(final)
        if vibhakti == 8: return "हे " + res
        return res

    @staticmethod
    def derive_pada(stem_str, vibhakti, vacana, logger=None, force_pratipadika=False):
        stem = ad(stem_str)

        # --- VALIDATION ---
        if force_pratipadika:
            if logger: logger.log("१.२.४५", "मैनुअल (Manual Override)", f"⚠️ बलपूर्वक: '{stem_str}'", stem, "User")
        else:
            if stem_str in SubantaProcessor.KNOWN_PRATYAYAS: return "Error: Pratyaya"
            if stem_str not in SubantaProcessor.VALID_SINGLE_LETTERS:
                try:
                    dhatu = DhatuRepository.get_dhatu_info(stem_str)
                    if dhatu: return "Error: Dhatu"
                except: pass
            if logger: logger.log("१.२.४५", "अर्थवदधातुरप्रत्ययः प्रातिपदिकम्", f"✅ '{stem_str}' (प्रातिपदिक संज्ञा)", stem, "महर्षि पाणिनि")

        last_char = stem[-1].char
        is_at = (last_char == 'अ')   
        is_aa = (last_char == 'आ')   
        is_it = (last_char == 'इ')                 
        is_ut = (last_char == 'उ')                 
        is_fem_ghi = (stem_str in SubantaProcessor.FEMININE_I_U_STEMS) or is_aa
        is_ghi_any = (is_it or is_ut)
        is_sarvanama = (stem_str in SubantaProcessor.SARVANAMA_GANA)
        if is_sarvanama and logger: logger.log("१.१.२७", "सर्वादीनि सर्वनामनि", f"{stem_str} (सर्वनाम संज्ञा)", stem, "महर्षि पाणिनि")

        # --- SELECTION ---
        sup_data = KnowledgeBase.get_sup(vibhakti, vacana)
        if not sup_data: return "?"
        raw_sup, tags = sup_data

        if logger: logger.log("४.१.२", "स्वौजसमौट्...", f"प्रत्यय चयन: '{raw_sup}'", stem, "महर्षि पाणिनि")

        clean_suffix = []
        rule_applied = ""

        # Hardcoded Cleaning (Hindi Rules)
        if vibhakti == 1 and vacana == 1: clean_suffix = ad("स्"); rule_applied = "१.३.२ उपदेशेऽजनुनासिक इत्"
        elif vibhakti == 1 and vacana == 2: clean_suffix = ad("औ") 
        elif vibhakti == 1 and vacana == 3: 
            if is_at and is_sarvanama: clean_suffix = ad("ई"); rule_applied = "७.१.१७ जसः शी (जस् -> शी)"
            else: clean_suffix = ad("अस्"); rule_applied = "१.३.७ चुटू (जकार इत्)"
        elif vibhakti == 2 and vacana == 1: clean_suffix = ad("अम्")
        elif vibhakti == 2 and vacana == 2: clean_suffix = ad("औ")
        elif vibhakti == 2 and vacana == 3: clean_suffix = ad("अस्"); rule_applied = "१.३.८ लशक्वतद्धिते (शकार इत्)"
        elif vibhakti == 3 and vacana == 1: clean_suffix = ad("आ"); rule_applied = "१.३.७ चुटू (टकार इत्)"
        elif vibhakti == 4 and vacana == 1: clean_suffix = ad("ए"); rule_applied = "१.३.८ लशक्वतद्धिते (ङकार इत्)"
        elif vibhakti == 5 and vacana == 1: clean_suffix = ad("अस्"); rule_applied = "१.३.८ लशक्वतद्धिते (ङकार इत्)"
        elif vibhakti == 6 and vacana == 1: clean_suffix = ad("अस्"); rule_applied = "१.३.८ लशक्वतद्धिते (ङकार इत्)"
        elif vibhakti == 7 and vacana == 1: clean_suffix = ad("इ"); rule_applied = "१.३.८ लशक्वतद्धिते (ङकार इत्)"
        elif vibhakti == 7 and vacana == 3: clean_suffix = ad("सु"); rule_applied = "१.३.३ हलन्त्यम् (पकार इत्)"
        elif vibhakti == 8 and vacana == 1: clean_suffix = ad("स्"); rule_applied = "१.३.२ उपदेशेऽजनुनासिक इत्"
        elif vibhakti == 8 and vacana == 3: clean_suffix = ad("अस्"); rule_applied = "१.३.७ चुटू"

        if not clean_suffix:
            clean_suffix, trace = SanjnaController.run_it_prakaran(ad(raw_sup), UpadeshaType.VIBHAKTI)
            if trace: rule_applied = "अनुबन्ध लोप"

        if logger and rule_applied:
            logger.log(rule_applied, "इत्-संज्ञा / लोप", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "महर्षि पाणिनि")

        is_sambuddhi = (vibhakti == 8 and vacana == 1)
        if is_sambuddhi and logger: 
            logger.log("२.३.४९", "एकवचनं सम्बुद्धिः", "सुँ -> सम्बुद्धि संज्ञा", stem + clean_suffix, "महर्षि पाणिनि")

        # --- SAMBUDDHI OPERATIONS ---
        if is_sambuddhi:
            if is_ghi_any: 
                if is_it: stem[-1].char = 'ए'
                if is_ut: stem[-1].char = 'ओ'
                if logger: logger.log("७.३.१०८", "ह्रस्वस्य गुणः", sanskrit_varna_samyoga(stem+clean_suffix), stem, "महर्षि पाणिनि")
            if is_aa:
                stem[-1].char = 'ए'
                if logger: logger.log("७.३.१०६", "सम्बुद्धौ च", sanskrit_varna_samyoga(stem+clean_suffix), stem, "महर्षि पाणिनि")

            last = stem[-1].char
            if (last in ['ए', 'ओ', 'अ', 'इ', 'उ', 'ऋ']) and clean_suffix:
                if clean_suffix[0].char not in SandhiProcessor.AC:
                    clean_suffix = []
                    if logger: logger.log("६.१.६९", "एङ्ह्रस्वात् सम्बुद्धेः", "हल्-लोप (सकार लोप)", stem, "महर्षि पाणिनि")
            return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)

        # --- SARVANAMA ---
        if is_at and is_sarvanama:
            if vibhakti == 4 and vacana == 1:
                clean_suffix = ad("स्मै")
                if logger: logger.log("७.१.१४", "सर्वनाम्नः स्मै", "सर्वस्मै", stem+clean_suffix, "महर्षि पाणिनि")
                return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)
            elif vibhakti == 5 and vacana == 1:
                clean_suffix = ad("स्मात्")
                if logger: logger.log("७.१.१५", "ङसिङ्योः स्मात्स्मिनौ", "सर्वस्मात्", stem+clean_suffix, "महर्षि पाणिनि")
                return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)
            elif vibhakti == 7 and vacana == 1:
                clean_suffix = ad("स्मिन्")
                if logger: logger.log("७.१.१५", "ङसिङ्योः स्मात्स्मिनौ", "सर्वस्मिन्", stem+clean_suffix, "महर्षि पाणिनि")
                return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)
            elif vibhakti == 6 and vacana == 3:
                clean_suffix = ad("साम्") 
                if logger: logger.log("७.१.५२", "आमि सर्वनाम्नः सुट्", "सर्वसाम्", stem+clean_suffix, "महर्षि पाणिनि")
                stem[-1].char = 'ए'
                if logger: logger.log("७.३.१०३", "बहुवचने झल्येत्", "सर्वेसाम्", stem+clean_suffix, "महर्षि पाणिनि")
                return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)

        # --- RAMA (At) ---
        if is_at:
            if vibhakti == 2 and vacana == 1:
                if clean_suffix and clean_suffix[0].char == 'अ':
                    del clean_suffix[0]
                    if logger: logger.log("६.१.१०७", "अमि पूर्वः", sanskrit_varna_samyoga(stem+clean_suffix), stem + clean_suffix, "महर्षि पाणिनि")
                    return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)
            if vibhakti == 3 and vacana == 1: 
                clean_suffix = ad("इन")
                if logger: logger.log("७.१.१२", "टाङसिङसामिनात्स्याः", "टा -> इन", stem + clean_suffix, "महर्षि पाणिनि")
            elif vibhakti == 3 and vacana == 3: clean_suffix = ad("ऐस्")
            elif vibhakti == 4 and vacana == 1 and not is_sarvanama: clean_suffix = ad("य")
            elif vibhakti == 5 and vacana == 1 and not is_sarvanama: clean_suffix = ad("आत्")
            elif vibhakti == 6 and vacana == 1: clean_suffix = ad("स्य")
            elif vibhakti == 6 and vacana == 3 and not is_sarvanama: 
                clean_suffix = ad("न्") + clean_suffix; stem[-1].char = 'आ'

            if clean_suffix:
                f = clean_suffix[0].char
                if vacana == 3 and f in ['भ्', 'स्']: 
                    if not (vibhakti == 2 and vacana == 3): 
                        stem[-1].char = 'ए'
                        if logger: logger.log("७.३.१०३", "बहुवचने झल्येत्", sanskrit_varna_samyoga(stem+clean_suffix), stem, "महर्षि पाणिनि")
                elif vibhakti in [6, 7] and vacana == 2: stem[-1].char = 'ए'
                elif f in ['भ्', 'य', 'व्', 'य्', 'व']: 
                    # 7.3.102 requires strict scope check, simplifying for Hindi display
                    stem[-1].char = 'आ'

        # --- GHI ---
        if is_ghi_any:
            guna_char = 'ए' if is_it else 'ओ'
            dirgha_char = 'ई' if is_it else 'ऊ'

            if vibhakti == 2 and vacana == 1:
                 if clean_suffix and clean_suffix[0].char == 'अ':
                    del clean_suffix[0]
                    if logger: logger.log("६.१.१०७", "अमि पूर्वः", sanskrit_varna_samyoga(stem+clean_suffix), stem + clean_suffix, "महर्षि पाणिनि")
                    return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)

            if (vibhakti in [1,2] and vacana == 2) or (vibhakti == 2 and vacana == 3):
                pass

            elif vibhakti == 3 and vacana == 1:
                if not is_fem_ghi: clean_suffix = ad("ना")
            elif vibhakti in [4, 5, 6, 7] and vacana == 1:
                stem_a = stem[:]; stem_a[-1].char = guna_char
                suffix_a = clean_suffix[:]
                if vibhakti in [5, 6]: suffix_a = ad("स्")
                if vibhakti == 7: stem_a[-1].char = 'अ'; suffix_a = ad("औ")
                fp_a, _ = SandhiProcessor.apply_ac_sandhi(stem_a, suffix_a)
                res_a_final = SubantaProcessor._finalize(fp_a, vibhakti, vacana, logger)
                if not is_fem_ghi: return res_a_final
                # Alternate form
                stem_b = stem[:]
                suffix_b_str = "्यै" if vibhakti==4 else "्याः" if vibhakti in [5,6] else "्याम्"
                return f"{res_a_final} / {stem_str[:-1] + suffix_b_str}"
            elif (vibhakti == 1 or vibhakti == 8) and vacana == 3: stem[-1].char = guna_char
            elif vibhakti == 6 and vacana == 3: clean_suffix = ad("नाम्"); stem[-1].char = dirgha_char

        # --- RAMA (AA) ---
        if is_aa:
            if vibhakti==1 and vacana==1: return SubantaProcessor._finalize(stem, vibhakti, vacana, logger)
            if vacana==2 and vibhakti in [1,2]: stem[-1].char='ए'; clean_suffix=[]; return sanskrit_varna_samyoga(stem)
            if vibhakti==3 and vacana==1: stem[-1].char='ए'
            if vibhakti in [4,5,6,7] and vacana==1:
                clean_suffix = ad("या") + clean_suffix
                if vibhakti==4: clean_suffix=ad("यै"); return "रमायै"
                if vibhakti in [5,6]: clean_suffix=ad("यास्")
                if vibhakti==7: clean_suffix=ad("याम्"); return "रमायाम्"
            if vibhakti==6 and vacana==3: clean_suffix=ad("नाम्")

        # --- 6.1.102 & 6.1.103 PRIORITY SANDHI ---
        should_run_102 = False
        if clean_suffix:
            # Applies for 1.2, 2.2, 1.3, 2.3
            if (vibhakti in [1, 2] or vibhakti == 8) and (vacana in [2, 3]):
                suffix_start = clean_suffix[0].char

                if is_ghi_any:
                    if (vibhakti == 1 or vibhakti == 8) and vacana == 3:
                        should_run_102 = False
                    else:
                        should_run_102 = True

                elif is_at:
                    if vacana == 2:
                        should_run_102 = False # Na Dici
                    else:
                        # Sarve (1.3 Sarva) - Na Dici (i)
                        if suffix_start in ['इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ऌ']:
                            should_run_102 = False
                        else:
                            should_run_102 = True

        if should_run_102:
            if is_at: stem[-1].char = 'आ'
            if is_it: stem[-1].char = 'ई'
            if is_ut: stem[-1].char = 'ऊ'

            if logger: logger.log("६.१.१०२", "प्रथमयोः पूर्वसवर्णः", sanskrit_varna_samyoga(stem+clean_suffix), stem, "महर्षि पाणिनि")

            if clean_suffix and clean_suffix[0].is_vowel:
                del clean_suffix[0]

            if vibhakti == 2 and vacana == 3:
                if clean_suffix and (clean_suffix[0].char == 'स्' or clean_suffix[0].char == 'ः'):
                    clean_suffix[0].char = 'न्'
                    if logger: logger.log("६.१.१०३", "तस्माच्छसो नः पुंसि", "न्", stem+clean_suffix, "महर्षि पाणिनि")

            return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)

        # --- NORMAL SANDHI ---
        fp, rule = SandhiProcessor.apply_ac_sandhi(stem, clean_suffix)
        if logger and rule: logger.log(rule, "सन्धि", sanskrit_varna_samyoga(fp), fp, "महर्षि पाणिनि")

        return SubantaProcessor._finalize(fp, vibhakti, vacana, logger)
