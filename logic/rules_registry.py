"""
FILE: logic/rules_registry.py
PURPOSE: The "Rule Registry" (Risk #1 Solved)
Defines rules as data objects.
"""
from core.maheshwara_sutras import MaheshwaraSutras
from core.core_foundation import Varna

class PaniniRule:
    def __init__(self, id, name, condition, transformation, type="Vidhi"):
        self.id = id
        self.name = name
        self.condition = condition # Lambda receiving (state)
        self.transformation = transformation # Lambda receiving (state)
        self.type = type # Vidhi, Sanjna, Paribhasha

# --- PRATYAHARA HELPER (Risk #3 Solved) ---
def in_pratyahara(varna_obj, p_name):
    # Dynamic Query to Maheshwara Sutras
    pset = MaheshwaraSutras.get_pratyahara(p_name)
    # Simple char check (ignoring modifiers for basic check)
    return varna_obj.char[0] in pset

# --- RULE DEFINITIONS ---
def define_rules():
    rules = []

    # R1: 6.1.77 Eco Yanaci (Sandhi)
    # Condition: Term[-1] is IK, NextTerm[0] is AC (Dissimilar)
    def check_yan(state):
        if len(state.terms) < 2: return False
        t1 = state.terms[-1]
        t2 = state.terms[-1] # Wait, need adjacent terms. 
        # Simplified: Check last char of Term 0 vs first of Term 1
        # Real engine scans all junctions.
        for i in range(len(state.terms)-1):
            left = state.terms[i].varnas
            right = state.terms[i+1].varnas
            if not left or not right: continue

            last = left[-1]
            first = right[0]

            # Use Pratyahara Logic
            if in_pratyahara(last, "इक्") and in_pratyahara(first, "अच्"):
                return (i, "YAN")
        return False

    def apply_yan(state, context):
        idx, _ = context
        left_term = state.terms[idx]
        last_varna = left_term.varnas.pop()

        yan_map = {'इ': 'य्', 'ई': 'य्', 'उ': 'व्', 'ऊ': 'व्', 'ऋ': 'र्', 'ॠ': 'र्', 'ऌ': 'ल्'}
        sub = yan_map.get(last_varna.char[0], last_varna.char)

        left_term.varnas.append(Varna(sub))
        return f"Replaced {last_varna.char} with {sub}"

    rules.append(PaniniRule("6.1.77", "इको यणचि", check_yan, apply_yan))

    # R2: 8.3.15 Kharavasanayor... (Visarga)
    # Condition: Padanta 's' or 'r'
    def check_visarga(state):
        # Check absolute end of the Prakriya
        if not state.terms: return False
        last_term = state.terms[-1]
        if not last_term.varnas: return False
        last_char = last_term.varnas[-1].char
        if last_char in ['स्', 'र्']: return True
        return False

    def apply_visarga(state, context):
        last_term = state.terms[-1]
        old = last_term.varnas[-1].char
        last_term.varnas[-1] = Varna("ः")
        return f"Changed Padanta {old} -> ः"

    rules.append(PaniniRule("8.3.15", "खरवसानयोर्विसर्जनीयः", check_visarga, apply_visarga))

    return rules
