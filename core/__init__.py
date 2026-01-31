"""
FILE: core/__init__.py
TIMESTAMP: 2026-01-30 23:10:00 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta) | PILLAR: Package Initialization & System Logging
DESCRIPTION: Initializes the logging system and exports foundational types.
"""
import logging
import os

# =============================================================================
# 1. SYSTEM LOGGING SETUP
# =============================================================================
LOG_FILE = "panini_engine.log"

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        # 'w' mode overwrites the log file on every run (clean start).
        # Change to 'a' if you want to keep history across runs.
        logging.FileHandler(LOG_FILE, mode='w'),

        # Uncomment the next line to see internal logs in the terminal (Debug Mode)
        # logging.StreamHandler()
    ]
)

# Initialize the global core logger
sys_logger = logging.getLogger("PaniniCore")
sys_logger.info("--------------------------------------------------")
sys_logger.info("   PANINI ENGINE v6.0 INITIALIZED")
sys_logger.info("   (System logs redirected to panini_engine.log)")
sys_logger.info("--------------------------------------------------")

# =============================================================================
# 2. MODULE EXPORTS
# =============================================================================

# Type Definitions & Registries
from .upadesha_registry import UpadeshaType
from .sup_registry import SupRegistry

# The New Librarian (Replaces old SutraRegistry)
from .sutra_manager import SutraManager

# Context & History Tracking
from .prakriya_context import PrakriyaContext
from .prakriya_logger import PrakriyaLogger

# Phonology Utilities
# (Exported here for easy access via 'from core import ad, Varna')
from .phonology import ad, Varna, sanskrit_varna_samyoga