"""
FILE: logic/dhatu_processor.py - PAS-v14.0 (Num-Agama + Internal Sandhi)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class DhatuDiagnostic:
    def __init__(self, raw_upadesha, is_subdhatu=False):
        self.raw = raw_upadesha
        self.is_subdhatu = is_subdhatu
        self.varnas = ad(raw_upadesha)

        # Snapshot
        self.originally_halanta = False
        if self.varnas and self.varnas[-1].is_consonant:
            self.originally_halanta = True

        self.it_tags = set()
        self.history = []
        self.pada = "Unknown"

        self.process()
        self.pada = self.determine_pada()

    def log(self, rule, desc):
        self.history.append(f"{rule}: {desc}")

    def process(self):
        # Phase 1: Cleaning (It-Karya)
        ir_it_processed = self._apply_ir_it_vartika()
        self._apply_1_3_5_adir_nit_tu_du()
        self._apply_1_3_2_upadeshe_aj_it()

        text = sanskrit_varna_samyoga(self.varnas)
        is_vartika_exception = any(text.startswith(x) for x in ["ष्वष्क्", "ष्ठिव्"])

        if self.originally_halanta and not ir_it_processed and not is_vartika_exception:
            self._apply_1_3_3_halantyam()

        # Phase 2: Root Phonology
        self._apply_6_1_64_shatva_vidhi()
        self._apply_6_1_65_natva_vidhi()

        # Phase 3: Augmentation (Num)
        # 1.1.47: Midaco'ntyāt paraḥ (Place after last vowel)
        self._apply_7_1_58_num_agama()

        # Phase 4: Internal Sandhi (Processing the inserted Num)
        self._apply_internal_sandhi()

    def _apply_7_1_58_num_agama(self):
        """
        7.1.58: Idito num dhātoḥ (Insert 'n')
        1.1.47: Midaco'ntyāt paraḥ (Insert after last vowel)
        """
        if "ir-It (Vartika)" in self.it_tags: return

        # STRICT Check: Only Short 'इँ-It' triggers Num.
        if any("इँ-It" in t for t in self.it_tags):
            # Algorithm for 1.1.47
            v_indices = [i for i, v in enumerate(self.varnas) if v.is_vowel]
            if v_indices:
                idx = v_indices[-1] + 1
                self.varnas.insert(idx, Varna("न्"))
                self.log("7.1.58", "Added Num (n) after last vowel (1.1.47)")

    def _apply_internal_sandhi(self):
        """
        Handles 8.3.24 (Naśchāpadāntasya jhali) -> Anusvara
        Handles 8.4.58 (Anusvārasya yayi parasavarṇaḥ) -> Class Nasal
        """
        # Scan for the inserted 'n' (Num)
        for i in range(len(self.varnas) - 1):
            curr = self.varnas[i].char
            if curr != 'न्': continue

            # Look ahead
            nxt = self.varnas[i+1].char

            # 1. Check for Parasavarna (Matching Class Nasal)
            # Kavarga -> ṅ
            if any(k in nxt for k in ['क', 'ख', 'ग', 'घ']):
                self.varnas[i].char = 'ङ्'
                self.log("8.4.58", f"n -> ṅ (before {nxt})")

            # Cavarga -> ñ (e.g., Bhaji -> Bhañj)
            elif any(c in nxt for c in ['च', 'छ', 'ज', 'झ']):
                self.varnas[i].char = 'ञ्'
                self.log("8.4.58", f"n -> ñ (before {nxt})")

            # Ṭavarga -> ṇ (e.g., Kuṭhi -> Kuṇṭh)
            elif any(t in nxt for t in ['ट', 'ठ', 'ड', 'ढ']):
                self.varnas[i].char = 'ण्'
                self.log("8.4.58", f"n -> ṇ (before {nxt})")

            # Tavarga -> n (e.g., Citi -> Cint) - No change needed physically

            # Pavarga -> m (e.g., Jabhi -> Jambh)
            elif any(p in nxt for p in ['प', 'फ', 'ब', 'भ']):
                self.varnas[i].char = 'म्'
                self.log("8.4.58", f"n -> m (before {nxt})")

            # 2. Check for Anusvara (before Śal/Sibilants)
            # e.g., Trasi -> Traṃs
            elif any(s in nxt for s in ['श', 'ष', 'स', 'ह']):
                self.varnas[i].char = 'ं'
                self.log("8.3.24", f"n -> ṃ (before Jhal {nxt})")

            # 3. Exception: 'v' is NOT Jhal in internal context for this purpose usually,
            # but strictly, if not Stop and not Sibilant, it might remain 'n' 
            # (e.g. Ivi -> Inv). Code does nothing, preserving 'n'.

    # --- Standard Helpers (Unchanged) ---
    def determine_pada(self):
        raw_tags = [t.split('-')[0] for t in self.it_tags]
        if any(x in raw_tags for x in ['ङ', 'ङि', 'अँ']): return "Ātmanepada (1.3.12)"
        if any(x in raw_tags for x in ['ञ', 'ञि']): return "Ubhayapada (1.3.72)"
        return "Parasmaipada (1.3.78)"

    def _apply_ir_it_vartika(self):
        if len(self.varnas) >= 2:
            last = self.varnas[-1]
            penult = self.varnas[-2]
            if last.char == 'र्' and any(x in penult.char for x in ['इ', 'ि', 'ई', 'ी']):
                self.it_tags.add("ir-It (Vartika)")
                self.varnas = self.varnas[:-2]
                self.log("Vartika", "Removed final 'ir' bundle")
                return True
        return False

    def _apply_1_3_5_adir_nit_tu_du(self):
        if len(self.varnas) >= 2:
            c1 = self.varnas[0].char.replace('्', '')
            c2 = self.varnas[1].char
            marker = None
            if c1 == 'ञ' and any(v in c2 for v in ['इ', 'ि']): marker = "ञि"
            elif c1 == 'ट' and any(v in c2 for v in ['उ', 'ु']): marker = "टु"
            elif c1 == 'ड' and any(v in c2 for v in ['उ', 'ु']): marker = "डु"
            if marker:
                 self.it_tags.add(f"{marker}-It (1.3.5)")
                 self.varnas = self.varnas[2:]
                 self.log("1.3.5", f"Removed initial {marker}")

    def _apply_1_3_2_upadeshe_aj_it(self):
        to_remove = []
        for v in self.varnas:
            if v.is_anunasika:
                tag = "Aj-It" 
                if any(x in v.char for x in ['इ', 'ि']): tag = "इँ-It"
                elif any(x in v.char for x in ['ई', 'ी']): tag = "ईँ-It"
                elif any(x in v.char for x in ['उ', 'ु']): tag = "उँ-It"
                else: tag = "अँ-It"
                self.it_tags.add(f"{tag} (1.3.2)")
                to_remove.append(v)
                self.log("1.3.2", f"Removed nasal {v.char}")
        for v in to_remove: self.varnas.remove(v)

    def _apply_1_3_3_halantyam(self):
        if self.varnas and self.varnas[-1].is_consonant:
            last = self.varnas[-1].char
            self.it_tags.add(f"{last}-It (1.3.3)")
            self.varnas.pop()
            self.log("1.3.3", f"Removed final {last}")

    def _apply_6_1_64_shatva_vidhi(self):
        if not self.varnas: return
        text = sanskrit_varna_samyoga(self.varnas)
        if self.is_subdhatu: return
        exceptions = ["ष्ठिव्", "ष्वष्क्", "ष्ठिवु"]
        if any(text.startswith(ex) for ex in exceptions): return
        if self.varnas[0].char.startswith('ष्'):
            self.varnas[0].char = self.varnas[0].char.replace('ष्', 'स्')
            self.log("6.1.64", "Changed initial ṣ -> s")
            for i in range(1, min(len(self.varnas), 3)):
                char = self.varnas[i].char
                if 'ट' in char: self.varnas[i].char = char.replace('ट', 'त')
                elif 'ठ' in char: self.varnas[i].char = char.replace('ठ', 'थ')
                elif 'ण' in char: self.varnas[i].char = char.replace('ण', 'न')

    def _apply_6_1_65_natva_vidhi(self):
        if self.varnas and self.varnas[0].char.startswith('ण्'):
            self.varnas[0].char = self.varnas[0].char.replace('ण्', 'न्')
            self.log("6.1.65", "Changed initial ṇ -> n")

    def get_final_root(self):
        return sanskrit_varna_samyoga(self.varnas)
