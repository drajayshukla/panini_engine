"""
FILE: logic/sanjna/vidhi_linker.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Bridge (Vidhi-Sanjñā Linker)
"""

def link_vidhi_rule(rule_name, *args, **kwargs):
    from logic.vidhi import VidhiEngine
    method = getattr(VidhiEngine, rule_name)
    return method(*args, **kwargs)

# Backward compatibility aliases
def apply_vṛddhi_7_2_115(a, s): return link_vidhi_rule('apply_aco_niti_7_2_115', a, s)
def apply_rutva_8_2_66(v): return link_vidhi_rule('apply_rutva_8_2_66', v)
def apply_visarga_8_3_15(v): return link_vidhi_rule('apply_visarga_8_3_15', v)