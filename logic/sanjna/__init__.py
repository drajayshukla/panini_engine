"""
FILE: logic/sanjna/__init__.py
PAS-v2.0: 5.0.1 (Siddha) | TIMESTAMP: 2026-01-30 16:10:00
"""
from .it_prakaranam import ItSanjnas
from .definitions_1_1 import FoundationSanjnas
from .morpho_sanjna import MorphoSanjnas

# Order of inheritance: ItSanjnas must be present for 1.3.x rules
class SanjnaEngine(ItSanjnas, FoundationSanjnas, MorphoSanjnas):
    """
    Universal Sanjñā Interface.
    Inherits all 1.3.x methods from ItSanjnas to resolve Bridge AttributeErrors.
    """
    pass

sanjna_engine = SanjnaEngine()