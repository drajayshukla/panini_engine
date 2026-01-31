"""
FILE: core/prakriya_context.py
PAS-v2.0: 5.0 (Siddha) | PILLAR: Prakriya-Vatavaranam (Context)
TIMESTAMP: 2026-01-30 15:00:00
"""
from dataclasses import dataclass, field
from typing import Set, Dict, Optional

@dataclass
class PrakriyaContext:
    """
    [VṚTTI]: प्रक्रिया-वातावरणम्।
    Holds the environmental metadata required for rule application.
    This acts as the 'Sabhā' (assembly) that sūtras consult to check
    if conditions like Ārdhadhātuka or Dhātulopa are met.
    """

    # --- Core Status Flags ---
    is_ardhadhatuka: bool = False
    is_sarvadhatuka: bool = False
    is_intensive: bool = False  # Handles Yaṅ/Yaṅ-luk contexts (e.g., मरीमृज)

    # --- Lopa (Elision) Tracking (Critical for 1.1.4, 1.1.5) ---
    dhatulopa: bool = False
    dhatulopa_caused_by_suffix: bool = False
    pratyayalopa: bool = False

    # --- Rule Identification ---
    rule_trigger: Optional[str] = None  # e.g., "2.4.74"

    # --- Designation and Metadata Storage ---
    sanjnas: Set[str] = field(default_factory=set)
    metadata: Dict = field(default_factory=dict)

    def has_sanjna(self, name: str) -> bool:
        """Checks if a specific technical designation is active in this context."""
        return name in self.sanjnas

    def add_sanjna(self, name: str):
        """Adds a technical designation to the current context."""
        self.sanjnas.add(name)