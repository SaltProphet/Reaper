"""
REAPER Core Models

Pydantic v2 models for data validation across the 5-sense pipeline.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class SenseType(str, Enum):
    """The five senses plus Action in the REAPER pipeline."""
    SIGHT = "sight"
    HEARING = "hearing"
    TOUCH = "touch"
    TASTE = "taste"
    SMELL = "smell"
    ACTION = "action"


class Signal(BaseModel):
    """
    Base signal model representing raw input from any sense.
    
    All plugins must accept and return Signal-compatible data.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    sense_type: SenseType = Field(..., description="Which sense detected this signal")
    source: str = Field(..., description="Plugin source identifier (never hard-coded)")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_data: Dict[str, Any] = Field(default_factory=dict, description="Raw signal data")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ScoredSignal(BaseModel):
    """
    Signal after scoring/analysis.
    
    Extends Signal with score and analysis results.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    signal: Signal
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized score 0-1")
    analysis: Dict[str, Any] = Field(default_factory=dict, description="Analysis results")
    tags: list[str] = Field(default_factory=list, description="Classification tags")


class ActionResult(BaseModel):
    """
    Result of an action taken on a signal.
    
    Used by Action sense plugins to report what they did.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    signal: ScoredSignal
    action_type: str = Field(..., description="Type of action taken")
    success: bool = Field(..., description="Whether action succeeded")
    result_data: Dict[str, Any] = Field(default_factory=dict, description="Action result data")
    error: Optional[str] = Field(None, description="Error message if failed")
