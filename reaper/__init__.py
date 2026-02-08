"""
REAPER - Modular, biological pipeline for harvesting problem friction signals.

Plugin-driven and operator-ready system using Pluggy and Pydantic v2.
"""
from reaper.models import ActionResult, ScoredSignal, SenseType, Signal
from reaper.plugin_manager import PluginManager

__version__ = "0.1.0"
__all__ = [
    "Signal",
    "ScoredSignal",
    "ActionResult",
    "SenseType",
    "PluginManager",
]
