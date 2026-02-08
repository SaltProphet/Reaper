"""
Parametrized Tests for REAPER Pipeline

Tests all sense types systematically using pytest parametrization.
"""

import pytest

from pipeline.action import ActionPlugin
from pipeline.hearing import HearingPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.sight import SightPlugin
from pipeline.smell import SmellPlugin
from pipeline.taste import TastePlugin
from pipeline.touch import TouchPlugin
from reaper import PluginManager
from reaper.models import ScoredSignal, SenseType, Signal


class TestParametrizedSenses:
    """Parametrized tests for all sense types."""

    @pytest.fixture
    def plugin_manager(self):
        """Create a fully configured PluginManager."""
        pm = PluginManager()
        pm.register_plugin(SightPlugin(), name="sight")
        pm.register_plugin(HearingPlugin(), name="hearing")
        pm.register_plugin(TouchPlugin(), name="touch")
        pm.register_plugin(TastePlugin(), name="taste")
        pm.register_plugin(SmellPlugin(), name="smell")
        pm.register_plugin(ScoringPlugin(), name="scoring")
        pm.register_plugin(ActionPlugin(), name="action")
        return pm

    @pytest.mark.parametrize(
        "sense_type,detect_method,source",
        [
            (SenseType.SIGHT, "detect_sight", "visual-source"),
            (SenseType.HEARING, "detect_hearing", "audio-source"),
            (SenseType.TOUCH, "detect_touch", "sensor-source"),
            (SenseType.TASTE, "detect_taste", "quality-source"),
            (SenseType.SMELL, "detect_smell", "pattern-source"),
        ],
    )
    def test_sense_detection_parametrized(self, plugin_manager, sense_type, detect_method, source):
        """Test detection for all sense types parametrically."""
        detect_func = getattr(plugin_manager, detect_method)
        signals = detect_func(source=source)

        assert len(signals) > 0
        assert all(s.sense_type == sense_type for s in signals)
        assert all(s.source == source for s in signals)

    @pytest.mark.parametrize(
        "sense_type",
        [
            SenseType.SIGHT,
            SenseType.HEARING,
            SenseType.TOUCH,
            SenseType.TASTE,
            SenseType.SMELL,
        ],
    )
    def test_signal_creation_all_types(self, sense_type):
        """Test creating signals for all sense types."""
        signal = Signal(sense_type=sense_type, source="test-source")

        assert signal.sense_type == sense_type
        assert signal.source == "test-source"
        assert isinstance(signal.raw_data, dict)
        assert isinstance(signal.metadata, dict)

    @pytest.mark.parametrize(
        "score",
        [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0],
    )
    def test_scoring_with_various_scores(self, score):
        """Test scoring with various valid score values."""
        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = ScoredSignal(signal=signal, score=score)

        assert scored.score == score
        assert 0.0 <= scored.score <= 1.0

    @pytest.mark.parametrize(
        "invalid_score",
        [-1.0, -0.1, 1.1, 2.0, 10.0],
    )
    def test_invalid_scores_rejected(self, invalid_score):
        """Test that invalid scores are rejected."""
        signal = Signal(sense_type=SenseType.SIGHT, source="test")

        with pytest.raises(Exception):  # Pydantic ValidationError
            ScoredSignal(signal=signal, score=invalid_score)

    @pytest.mark.parametrize(
        "source",
        [
            "simple-source",
            "source-with-dashes",
            "source_with_underscores",
            "source123",
            "https://example.com/source",
            "file:///path/to/source",
            "",  # Empty source
        ],
    )
    def test_various_source_formats(self, plugin_manager, source):
        """Test detection works with various source formats."""
        signals = plugin_manager.detect_sight(source=source)

        assert isinstance(signals, list)
        if len(signals) > 0:
            assert signals[0].source == source

    @pytest.mark.parametrize(
        "detect_method",
        [
            "detect_sight",
            "detect_hearing",
            "detect_touch",
            "detect_taste",
            "detect_smell",
        ],
    )
    def test_all_detection_methods_return_lists(self, plugin_manager, detect_method):
        """Test all detection methods return lists."""
        detect_func = getattr(plugin_manager, detect_method)
        result = detect_func(source="test")

        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.parametrize(
        "sense_type,raw_data",
        [
            (SenseType.SIGHT, {"image": "data", "confidence": 0.95}),
            (SenseType.HEARING, {"text": "hello", "language": "en"}),
            (SenseType.TOUCH, {"pressure": 10, "duration": 2.5}),
            (SenseType.TASTE, {"quality": "good", "score": 8}),
            (SenseType.SMELL, {"pattern": "anomaly", "severity": "high"}),
        ],
    )
    def test_signals_with_sense_specific_data(self, sense_type, raw_data):
        """Test signals can carry sense-specific raw data."""
        signal = Signal(sense_type=sense_type, source="test", raw_data=raw_data)

        assert signal.sense_type == sense_type
        assert signal.raw_data == raw_data

    @pytest.mark.parametrize(
        "tags",
        [
            ["tag1"],
            ["tag1", "tag2"],
            ["critical", "urgent", "high-priority"],
            [],  # Empty tags
        ],
    )
    def test_scored_signals_with_various_tags(self, tags):
        """Test ScoredSignal with various tag configurations."""
        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = ScoredSignal(signal=signal, score=0.5, tags=tags)

        assert scored.tags == tags

    @pytest.mark.parametrize(
        "action_type",
        [
            "notification",
            "log_entry",
            "ticket_creation",
            "alert",
            "automation_trigger",
        ],
    )
    def test_action_results_with_various_types(self, action_type, plugin_manager):
        """Test actions can be executed with various action types."""
        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = ScoredSignal(signal=signal, score=0.8)

        # ActionPlugin returns stub_action, so we're just validating
        # that the ActionResult model accepts various action_type values
        results = plugin_manager.execute_action(scored)
        assert len(results) > 0
        assert isinstance(results[0].action_type, str)

    @pytest.mark.parametrize(
        "sense_type,plugin_class",
        [
            (SenseType.SIGHT, SightPlugin),
            (SenseType.HEARING, HearingPlugin),
            (SenseType.TOUCH, TouchPlugin),
            (SenseType.TASTE, TastePlugin),
            (SenseType.SMELL, SmellPlugin),
        ],
    )
    def test_plugin_instances_for_all_senses(self, sense_type, plugin_class):
        """Test that all sense plugin classes can be instantiated."""
        plugin = plugin_class()
        assert plugin is not None

    @pytest.mark.parametrize(
        "batch_size",
        [1, 5, 10, 50, 100],
    )
    def test_batch_signal_creation(self, batch_size):
        """Test batch signal creation with various sizes."""
        signals_data = [
            {"sense_type": SenseType.SIGHT, "source": f"source-{i}"} for i in range(batch_size)
        ]
        signals = Signal.create_batch(signals_data)

        assert len(signals) == batch_size
        assert all(isinstance(s, Signal) for s in signals)
        # All should share same timestamp
        timestamps = [s.timestamp for s in signals]
        assert len(set(timestamps)) == 1  # All same


class TestParametrizedPipeline:
    """Parametrized tests for complete pipeline flows."""

    @pytest.fixture
    def plugin_manager(self):
        """Create a fully configured PluginManager."""
        pm = PluginManager()
        pm.register_plugin(SightPlugin(), name="sight")
        pm.register_plugin(HearingPlugin(), name="hearing")
        pm.register_plugin(TouchPlugin(), name="touch")
        pm.register_plugin(TastePlugin(), name="taste")
        pm.register_plugin(SmellPlugin(), name="smell")
        pm.register_plugin(ScoringPlugin(), name="scoring")
        pm.register_plugin(ActionPlugin(), name="action")
        return pm

    @pytest.mark.parametrize(
        "detect_method,sense_type",
        [
            ("detect_sight", SenseType.SIGHT),
            ("detect_hearing", SenseType.HEARING),
            ("detect_touch", SenseType.TOUCH),
            ("detect_taste", SenseType.TASTE),
            ("detect_smell", SenseType.SMELL),
        ],
    )
    def test_full_pipeline_all_senses(self, plugin_manager, detect_method, sense_type):
        """Test complete pipeline (detect → score → act) for all senses."""
        # Detection
        detect_func = getattr(plugin_manager, detect_method)
        signals = detect_func(source=f"test-{sense_type.value}")

        assert len(signals) > 0
        assert all(s.sense_type == sense_type for s in signals)

        # Scoring
        scored_signals = [plugin_manager.score_signal(s)[0] for s in signals]
        assert len(scored_signals) == len(signals)
        assert all(0.0 <= s.score <= 1.0 for s in scored_signals)

        # Action
        results = [plugin_manager.execute_action(s)[0] for s in scored_signals]
        assert len(results) == len(scored_signals)
        assert all(r.success for r in results)
