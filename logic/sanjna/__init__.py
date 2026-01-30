"""
FILE: logic/sanjna/__init__.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Sanjñā-Orchestrator
REFERENCE: Combined Aṣṭādhyāyī Definitions
"""
from .definitions_1_1 import FoundationSanjnas
from .it_prakaranam import ItSanjnas
from .morpho_sanjna import MorphoSanjnas

class SanjnaEngine(FoundationSanjnas, ItSanjnas, MorphoSanjnas):
    """
    Universal Sanjñā interface.
    This class binds all Paninian technical definitions (1.1.x, 1.3.x, 1.4.x)
    into a single executable engine.
    """
    pass

# For easier access across the project
sanjna_engine = SanjnaEngine()