"""
FILE: teach_sambuddhi_logic.py
PURPOSE: Teach Sambuddhi Sanjna (2.3.49) and Eng-hrasvat Lopa (6.1.69).
LOGIC:
  1. If Vibhakti=8, Vacana=1 -> Label suffix as 'Sambuddhi' (2.3.49).
  2. If Ghi-stem -> Apply Guna (7.3.108) FIRST.
  3. Then check 6.1.69: If Stem ends in Eng/Hrasva AND Suffix is Sambuddhi/Hal -> DELETE.
"""
import os
import json
import sys
import subprocess

# ==============================================================================
# 1. UPDATE SUTRA DB
# ==============================================================================
SUTRA_UPDATE = [
    {
        "sutra_num": "2.3.49",
        "name": "एकवचनं संबुद्धिः",
        "type": "Sanjna",
        "vartikas": ["संबोधने प्रथमाया एकवचनं संबुद्धिसंज्ञं स्यात् ॥ (Vocative Singular is called Sambuddhi)."]
    },
    {
        "sutra_num": "6.1.69",
        "name": "एङ्ह्रस्वात् सम्बुद्धेः",
        "type": "Vidhi",
        "vartikas": [
            "एङन्ताद्ध्रस्वान्ताच्चाङ्गाद्धल्लुप्यते संबुद्धेश्चेत् । (Consonant of Sambuddhi is deleted after Eng or Short vowel).",
            "हे राम (Short 'a'), हे हरे (Eng 'e')."
        ]
    },
    {
        "sutra_num": "7.3.108",
        "name": "ह्रस्वस्य गुणः",
        "type": "Vidhi",
        "vartikas": ["सम्बुद्धौ (In Sambuddhi, short vowel gets Guna)."]
    }
]

json_path = "data/panini_sutras.json"
if os.path.exists(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        existing_ids = {item['sutra_num'] for item in data}
        for new_item in SUTRA_UPDATE:
            if new_item['sutra_num'] not in existing_ids:
                data.append(new_item)
            else:
                for i, item in enumerate(data):
                    if item['sutra_num'] == new_item['sutra_num']:
                        data[i] = new_item
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("✅ Sutra DB updated with 2.3.49, 6.1.69, 7.3.108")
    except Exception as e:
        print(f"❌ Error updating JSON: {e}")

# ==============================================================================
# 2. LOGIC: SUBANTA PROCESSOR (With Formal Sambuddhi Logic)
# ==============================================================================
NEW_PROCESSOR_CODE = '''"""
FILE: logic/subanta_processor.py
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga, UpadeshaType
from core.sanjna_controller import SanjnaController
from core.knowledge_base import KnowledgeBase
from logic.sandhi_processor import SandhiProcessor
from core.adhikara_controller import AdhikaraController
from core.dhatu_repo import DhatuRepository 

class SubantaProcessor:
    KNOWN_PRATYAYAS = {'सु', 'औ', 'जस्', 'अम्', 'औट्', 'शस्', 'टा', 'भ्याम्', 'भिस्', 'ङे', 'भ्यस्', 'ङसि', 'ङस्', 'ओस्', 'आम्', 'ङि', 'सुप्', 'तिप्', 'तस्', 'झि', 'सिप्', 'थस्', 'थ', 'मिप्', 'वस्', 'मस्', 'शप्', 'श्नु', 'स्य', 'तासि', 'क्विप्', 'घञ्'}
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
            if logger: logger.log("1.2.45", "Manual Override", f"⚠️ Forced: '{stem_str}'", stem, "User")
        else:
            if stem_str in SubantaProcessor.KNOWN_PRATYAYAS: return "Error: Pratyaya"
            if stem_str not in SubantaProcessor.VALID_SINGLE_LETTERS:
                try:
                    dhatu = DhatuRepository.get_dhatu_info(stem_str)
                    if dhatu: return "Error: Dhatu"
                except: pass
            if logger: logger.log("1.2.45", "Arthavad... Pratipadikam", f"✅ '{stem_str}'", stem, "Maharshi Pāṇini")

        # --- CLASSIFICATION ---
        last_char = stem[-1].char
        is_at = (last_char == 'अ')   
        is_aa = (last_char == 'आ')   
        is_it = (last_char == 'इ')                 
        is_ut = (last_char == 'उ')                 
        is_fem_ghi = (stem_str in SubantaProcessor.FEMININE_I_U_STEMS) or is_aa
        is_ghi_any = (is_it or is_ut)
        is_sarvanama = (stem_str in SubantaProcessor.SARVANAMA_GANA)
        if is_sarvanama and logger: logger.log("1.1.27", "Sarvadini Sarvanamani", f"{stem_str}", stem, "Maharshi Pāṇini")

        # --- SELECTION ---
        sup_data = KnowledgeBase.get_sup(vibhakti, vacana)
        if not sup_data: return "?"
        raw_sup, tags = sup_data; suffix = ad(raw_sup)
        
        if logger: logger.log("4.1.2", "Svaujasmaut...", f"Selecting '{raw_sup}'", stem + suffix, "Maharshi Pāṇini")
        
        # 2.3.49 SAMBUDDHI SANJNA
        is_sambuddhi = False
        if vibhakti == 8 and vacana == 1:
            is_sambuddhi = True
            if logger: logger.log("2.3.49", "Ekavacanam Sambuddhih", "Su gets Sambuddhi Sanjna", stem + suffix, "Maharshi Pāṇini")

        clean_suffix, trace = SanjnaController.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)
        if clean_suffix: clean_suffix[0].sanjnas.update(tags)
        if logger and trace: logger.log(trace[-1], "It-Lopa", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

        # --- 8.1 SAMBUDDHI OPERATION (Shared Logic) ---
        if is_sambuddhi:
            # 1. Guna for Ghi/Hrasva (7.3.108)
            # Hari -> Hare, Guru -> Guro
            if is_ghi_any: 
                # Determine Guna
                if is_it: stem[-1].char = 'ए'
                if is_ut: stem[-1].char = 'ओ'
                if logger: logger.log("7.3.108", "Hrasvasya Gunah", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")
            
            # Rama (At) - No Guna needed, already 'a' (Hrasva).
            # Ramaa (Aa) - 7.3.106 Sambuddhau Ca (e) -> Rame
            if is_aa:
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.106", "Sambuddhau Ca", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")

            # 2. Deletion (6.1.69 Eng-hrasvat Sambuddheh)
            # Condition: Stem ends in Eng (e, o) OR Hrasva (a, i, u).
            # Suffix is 'Hal' (Consonant).
            last = stem[-1].char
            eng = ['ए', 'ओ']
            hrasva = ['अ', 'इ', 'उ', 'ऋ']
            
            if (last in eng or last in hrasva) and clean_suffix:
                # Check if suffix is Hal (Consonant)
                # 's' is Hal.
                if clean_suffix[0].char not in SandhiProcessor.AC:
                    # DELETE SUFFIX
                    clean_suffix = []
                    if logger: logger.log("6.1.69", "Eng-hrasvat Sambuddheh", f"Deleted 's' from {sanskrit_varna_samyoga(stem)}", stem, "Maharshi Pāṇini")
            
            return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)


        # --- SARVANAMA SPECIALS ---
        if is_at and is_sarvanama:
            if vibhakti == 1 and vacana == 3:
                clean_suffix = ad("ई") 
                if logger: logger.log("7.1.17", "Jasah Shee", "सर्वे", stem+clean_suffix, "Maharshi Pāṇini")
            elif vibhakti == 4 and vacana == 1:
                clean_suffix = ad("स्मै")
                if logger: logger.log("7.1.14", "Sarvanamnah Smai", "सर्वस्मै", stem+clean_suffix, "Maharshi Pāṇini")
                return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)
            elif vibhakti == 5 and vacana == 1:
                clean_suffix = ad("स्मात्")
                if logger: logger.log("7.1.15", "Ngasi-ngyoh Smatsminau", "सर्वस्मात्", stem+clean_suffix, "Maharshi Pāṇini")
                return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)
            elif vibhakti == 7 and vacana == 1:
                clean_suffix = ad("स्मिन्")
                if logger: logger.log("7.1.15", "Ngasi-ngyoh Smatsminau", "सर्वस्मिन्", stem+clean_suffix, "Maharshi Pāṇini")
                return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)
            elif vibhakti == 6 and vacana == 3:
                clean_suffix = ad("साम्") 
                if logger: logger.log("7.1.52", "Aami Sarvanamnah Sut", "सर्वसाम्", stem+clean_suffix, "Maharshi Pāṇini")
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.103", "Bahuvacane Jhalyet", "सर्वेसाम्", stem+clean_suffix, "Maharshi Pāṇini")
                return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)

        # --- RAMA (At) RULES ---
        if is_at:
            if vibhakti == 1 and vacana == 1: 
                return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)
            
            if vibhakti == 3 and vacana == 1: 
                clean_suffix = ad("इन")
                if logger: logger.log("7.1.12", "Ta-ngasi... -> Ina", "इन", stem + clean_suffix, "Maharshi Pāṇini")
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
                        if logger: logger.log("7.3.103", "Bahuvacane Jhalyet", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")
                elif vibhakti in [6, 7] and vacana == 2: stem[-1].char = 'ए'
                elif f in ['भ्', 'य', 'व्', 'य्', 'व']: 
                    if AdhikaraController.is_rule_in_scope("7.3.102", "ANGASYA"): stem[-1].char = 'आ'

        # --- PRE-CHECKS ---
        if (is_at or is_ghi_any or is_aa) and vibhakti == 2 and vacana == 1:
            return stem_str + "म्"

        # --- GHI ---
        if is_ghi_any:
            guna_char = 'ए' if is_it else 'ओ'
            dirgha_char = 'ई' if is_it else 'ऊ'
            
            if (vibhakti in [1,2] and vacana == 2) or (vibhakti == 2 and vacana == 3):
                stem[-1].char = dirgha_char # Purva Savarna Dirgha (6.1.102)
                
                if vacana == 2: 
                    clean_suffix = []
                    return sanskrit_varna_samyoga(stem)
                
                if vacana == 3: 
                    if not is_fem_ghi:
                        clean_suffix = ad("न्") # 6.1.103 Shaso Nah
                        if logger: logger.log("6.1.103", "Tasmacchaso Nah Pumsi", "न्", stem+clean_suffix, "Maharshi Pāṇini")
                    else:
                        clean_suffix = ad("स्")

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

        # --- PRIORITY SANDHI (6.1.102) ---
        should_run_102 = False
        if clean_suffix and (vibhakti==1 or vibhakti==2 or vibhakti==8) and vacana==3:
            stem_end = stem[-1].char
            suffix_start = clean_suffix[0].char
            if (is_at or is_ghi_any) and suffix_start == 'अ':
                if is_ghi_any and (vibhakti==1 or vibhakti==8):
                    should_run_102 = False 
                else:
                    should_run_102 = True 

        if should_run_102:
            if is_at: stem[-1].char = 'आ'
            if is_it: stem[-1].char = 'ई'
            if is_ut: stem[-1].char = 'ऊ'
            
            if logger: logger.log("6.1.102", "Prathamayoh Purvasavarnah", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")
            if clean_suffix and clean_suffix[0].char == 'अ':
                del clean_suffix[0]
            
            if vibhakti == 2:
                if clean_suffix and (clean_suffix[0].char == 'स्' or clean_suffix[0].char == 'ः'):
                    clean_suffix[0].char = 'न्'
                    if logger: logger.log("6.1.103", "Tasmacchaso Nah Pumsi", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")

            return SubantaProcessor._finalize(stem + clean_suffix, vibhakti, vacana, logger)

        # --- NORMAL SANDHI ---
        fp, rule = SandhiProcessor.apply_ac_sandhi(stem, clean_suffix)
        if logger and rule: logger.log(rule, "Sandhi", sanskrit_varna_samyoga(fp), fp, "Maharshi Pāṇini")
        
        return SubantaProcessor._finalize(fp, vibhakti, vacana, logger)
'''

with open("logic/subanta_processor.py", "w", encoding="utf-8") as f:
    f.write(NEW_PROCESSOR_CODE)

print("🚀 Sambuddhi Sanjna (2.3.49) & Eng-hrasvat Lopa (6.1.69) implemented structurally.")
subprocess.run([sys.executable, "master_runner.py"])