"""
FILE: logic/vidhi/guna_misc.py
PAS-v2.0: 5.2 (Siddha) | PILLAR: Misc Guṇa (7.3 & 7.4)
"""
from core.phonology import Varna


class GunaMisc:

    @staticmethod
    def apply_jasi_ca_7_3_109(anga, suffix):
        """[७.३.१०९]: जसि च।"""
        if not anga: return anga, None
        last = anga[-1]
        if last.char in ['इ', 'उ']:
            last.char = 'ए' if last.char == 'इ' else 'ओ'
            last.trace.append("७.३.१०९")
            return anga, "७.३.१०९"
        return anga, None

    @staticmethod
    def apply_rto_ngi_sarvanamasthanayoh_7_3_110(anga, suffix):
        """[७.३.११०]: ऋतो ङिसर्वनामस्थानयोः।"""
        if not anga: return anga, None
        if anga[-1].char == 'ऋ':
            anga.pop()
            anga.append(Varna('अ'))
            anga.append(Varna('र्'))
            anga[-1].trace.append("७.३.११०")
            return anga, "७.३.११०"
        return anga, None

    @staticmethod
    def apply_gher_niti_7_3_111(anga, suffix=None):
        """[७.३.१११]: घेर्ङिति।"""
        if anga and anga[-1].char in ['इ', 'उ']:
            v = anga[-1]
            v.char = 'ए' if v.char == 'इ' else 'ओ'
            v.trace.append("७.३.१११")
            return anga, "७.३.१११"
        return anga, None

    @staticmethod
    def apply_guno_yanlukoh_7_4_82(anga):
        """[७.४.८२]: गुणो यङ्लुकोः।"""
        for v in anga:
            if "abhyasa" in v.sanjnas:
                old = v.char
                if v.char == 'इ':
                    v.char = 'ए'
                elif v.char == 'उ':
                    v.char = 'ओ'
                elif v.char == 'ऋ':
                    v.char = 'अर्'

                if v.char != old:
                    v.trace.append("७.४.८२")
                    return anga, "७.४.८२"
        return anga, None