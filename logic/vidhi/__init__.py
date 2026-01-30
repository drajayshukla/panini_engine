"""
FILE: logic/vidhi/__init__.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Vidhi-Orchestrator
"""
from .meta_rules import MetaRules
from .sandhi_engine import SandhiEngine
from .guna_vriddhi import GunaVriddhi
from .anga_transform import AngaTransform
from .tripadi import Tripadi

class VidhiEngine(MetaRules, SandhiEngine, GunaVriddhi, AngaTransform, Tripadi):
    """Universal Pāṇinian Rule Executor."""
    pass

# ALIASES: Defined outside the class to ensure parents are fully initialized
VidhiEngine.apply_vṛddhi_7_2_115 = VidhiEngine.apply_aco_niti_7_2_115
VidhiEngine.apply_vṛddhi_7_2_117 = VidhiEngine.apply_taddhiteshu_acam_ade_7_2_117