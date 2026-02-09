"""
Pipeline Stubs

Stub implementations for the 5-sense pipeline + Action.
Each sense = one job. These are reference implementations.
"""

from pipeline.action import ActionPlugin
from pipeline.hearing import HearingPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.sight import SightPlugin
from pipeline.smell import SmellPlugin
from pipeline.taste import TastePlugin
from pipeline.touch import TouchPlugin

__all__ = [
    "SightPlugin",
    "HearingPlugin",
    "TouchPlugin",
    "TastePlugin",
    "SmellPlugin",
    "ScoringPlugin",
    "ActionPlugin",
]
