"""
FILE: core/prakriya_stack.py
PURPOSE: The "State Persistence" Object (Render Fix)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class Term:
    """Represents a component: e.g., 'Rama' (Anga) or 'Su' (Pratyaya)"""
    def __init__(self, text, tags=None):
        self.varnas = ad(text) # List of Varna objects
        self.tags = tags if tags else set() 

    def get_text(self):
        return sanskrit_varna_samyoga(self.varnas)

    def add_tag(self, tag):
        self.tags.add(tag)

class PrakriyaState:
    """The Immutable Context passed through the Engine."""
    def __init__(self):
        self.terms = [] 
        self.history = [] 
        self.meta_flags = {} 

    def add_term(self, text, tags=None):
        self.terms.append(Term(text, tags))

    def step(self, rule_id, rule_name, operation_desc, result_snapshot):
        entry = {
            "rule": rule_id,
            "name": rule_name,
            "desc": operation_desc,
            "result": result_snapshot
        }
        self.history.append(entry)

    def render(self):
        """Returns the joined string representation."""
        # Flatten all varnas from all terms into one list
        all_varnas = []
        for t in self.terms:
            all_varnas.extend(t.varnas)

        # Apply Samyoga (Phonetic Join) on the whole sequence
        return sanskrit_varna_samyoga(all_varnas)

    def get_index_of_tag(self, tag_name):
        for i, term in enumerate(self.terms):
            if tag_name in term.tags: return i
        return -1
