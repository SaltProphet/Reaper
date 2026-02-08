"""
Tests for REAPER core models.

Validates Pydantic v2 models for the pipeline.
"""
from datetime import datetime

import pytest

from reaper.models import ActionResult, ScoredSignal, SenseType, Signal


class TestSignal:
    """Test Signal model validation."""

    def test_signal_creation(self):
        """Test creating a valid signal."""
        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test-source",
            raw_data={"key": "value"},
        )
        assert signal.sense_type == SenseType.SIGHT
        assert signal.source == "test-source"
        assert signal.raw_data == {"key": "value"}
        assert isinstance(signal.timestamp, datetime)

    def test_signal_requires_sense_and_source(self):
        """Test that sense_type and source are required."""
        with pytest.raises(Exception):
            Signal(raw_data={})

    def test_all_sense_types(self):
        """Test all sense types are valid."""
        for sense in SenseType:
            signal = Signal(sense_type=sense, source="test")
            assert signal.sense_type == sense


class TestScoredSignal:
    """Test ScoredSignal model validation."""

    def test_scored_signal_creation(self):
        """Test creating a valid scored signal."""
        signal = Signal(
            sense_type=SenseType.HEARING,
            source="test-source",
        )
        scored = ScoredSignal(
            signal=signal,
            score=0.75,
            analysis={"result": "good"},
            tags=["test", "valid"],
        )
        assert scored.signal == signal
        assert scored.score == 0.75
        assert scored.tags == ["test", "valid"]

    def test_score_validation_range(self):
        """Test that score must be between 0 and 1."""
        signal = Signal(sense_type=SenseType.TOUCH, source="test")

        # Valid scores
        ScoredSignal(signal=signal, score=0.0)
        ScoredSignal(signal=signal, score=0.5)
        ScoredSignal(signal=signal, score=1.0)

        # Invalid scores
        with pytest.raises(Exception):
            ScoredSignal(signal=signal, score=-0.1)
        with pytest.raises(Exception):
            ScoredSignal(signal=signal, score=1.1)


class TestActionResult:
    """Test ActionResult model validation."""

    def test_action_result_success(self):
        """Test creating a successful action result."""
        signal = Signal(sense_type=SenseType.SMELL, source="test")
        scored = ScoredSignal(signal=signal, score=0.8)
        result = ActionResult(
            signal=scored,
            action_type="test_action",
            success=True,
            result_data={"status": "completed"},
        )
        assert result.success is True
        assert result.error is None

    def test_action_result_failure(self):
        """Test creating a failed action result."""
        signal = Signal(sense_type=SenseType.TASTE, source="test")
        scored = ScoredSignal(signal=signal, score=0.3)
        result = ActionResult(
            signal=scored,
            action_type="test_action",
            success=False,
            error="Something went wrong",
        )
        assert result.success is False
        assert result.error == "Something went wrong"
