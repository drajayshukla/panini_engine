"""
FILE: logic/anga_processor.py - PAS-v8.3
PILLAR: Anga-Adhikara (6.4 - 7.4) & Functional Standardization
"""
from core.core_foundation import Varna, ad

class AngaProcessor:
    @staticmethod
    def is_blocked_kniti(suffix, context=None):
        if not suffix: return False
        # 1.1.5: Kniti Ca - Blocking Guna/Vriddhi
        tags = getattr(suffix[0], 'sanjnas', set())
        return any(t in tags for t in ['kit', 'ngit', 'gnit'])

    @staticmethod
    def apply_guna_7_3_84(anga, suffix, context=None):
        """7.3.84: सार्वधातुकार्धधातुकयोः - Guna of final Ik-varna."""
        if AngaProcessor.is_blocked_kniti(suffix): return anga, "Blocked by 1.1.5"
        if not anga: return anga, None
        
        last = anga[-1]
        guna_map = {'इ': 'ए', 'ई': 'ए', 'उ': 'ओ', 'ऊ': 'ओ', 'ऋ': 'अर्', 'ॠ': 'अर्', 'ऌ': 'अल्'}
        
        if last.char in guna_map:
            sub = guna_map[last.char]
            anga.pop()
            # Replace with new Varnas (handling multi-char like 'ar')
            for char in sub:
                v = Varna(char)
                v.trace.append("7.3.84")
                anga.append(v)
            return anga, "7.3.84"
        return anga, None

    @staticmethod
    def apply_6_1_64_shatva(varnas):
        """6.1.64: धात्वादेः षः सः - Initial sh -> s."""
        if varnas and varnas[0].char.startswith('ष्'):
            varnas[0].char = 'स्'
            return True
        return False

    @staticmethod
    def apply_6_1_65_natva(varnas):
        """6.1.65: णो नः - Initial nna -> n."""
        if varnas and varnas[0].char.startswith('ण्'):
            varnas[0].char = 'न्'
            return True
        return False

    @staticmethod
    def apply_aco_niti_7_2_115(anga, suffix):
        """7.2.115: अचो ञ्णिति - Vriddhi of final vowel before Ñit/Nit."""
        if not suffix: return anga, None
        tags = getattr(suffix[0], 'sanjnas', set())
        if not ({'ñit', 'ṇit'} & tags): return anga, None
        
        last = anga[-1]
        vriddhi_map = {'अ': 'आ', 'इ': 'ऐ', 'ई': 'ऐ', 'उ': 'औ', 'ऊ': 'औ', 'ऋ': 'आर्'}
        
        if last.char in vriddhi_map:
            sub = vriddhi_map[last.char]
            anga.pop()
            for char in sub:
                v = Varna(char); v.trace.append("7.2.115")
                anga.append(v)
            return anga, "7.2.115"
        return anga, None
