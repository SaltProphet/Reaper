"""
Tests for pipeline stub plugins.

Validates that stub plugins implement hooks correctly.
"""
from pipeline.action import ActionPlugin
from pipeline.hearing import HearingPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.sight import SightPlugin
from pipeline.smell import SmellPlugin
from pipeline.taste import TastePlugin
from pipeline.touch import TouchPlugin
from reaper.models import ScoredSignal, SenseType, Signal


class TestPipelineStubs:
    """Test stub plugin implementations."""

    def test_sight_plugin(self):
        """Test SightPlugin stub."""
        plugin = SightPlugin()
        signals = plugin.reaper_sight_detect(source="test-source")
        assert len(signals) > 0
        assert signals[0].sense_type == SenseType.SIGHT
        assert signals[0].source == "test-source"

    def test_hearing_plugin(self):
        """Test HearingPlugin stub."""
        plugin = HearingPlugin()
        signals = plugin.reaper_hearing_detect(source="test-source")
        assert len(signals) > 0
        assert signals[0].sense_type == SenseType.HEARING
        assert signals[0].source == "test-source"

    def test_touch_plugin(self):
        """Test TouchPlugin stub."""
        plugin = TouchPlugin()
        signals = plugin.reaper_touch_detect(source="test-source")
        assert len(signals) > 0
        assert signals[0].sense_type == SenseType.TOUCH
        assert signals[0].source == "test-source"

    def test_taste_plugin(self):
        """Test TastePlugin stub."""
        plugin = TastePlugin()
        signals = plugin.reaper_taste_detect(source="test-source")
        assert len(signals) > 0
        assert signals[0].sense_type == SenseType.TASTE
        assert signals[0].source == "test-source"

    def test_smell_plugin(self):
        """Test SmellPlugin stub."""
        plugin = SmellPlugin()
        signals = plugin.reaper_smell_detect(source="test-source")
        assert len(signals) > 0
        assert signals[0].sense_type == SenseType.SMELL
        assert signals[0].source == "test-source"

    def test_scoring_plugin(self):
        """Test ScoringPlugin stub."""
        plugin = ScoringPlugin()
        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = plugin.reaper_score_signal(signal=signal)
        assert isinstance(scored, ScoredSignal)
        assert 0.0 <= scored.score <= 1.0

    def test_action_plugin(self):
        """Test ActionPlugin stub."""
        plugin = ActionPlugin()
        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = ScoredSignal(signal=signal, score=0.7)
        result = plugin.reaper_action_execute(scored_signal=scored)
        assert result.success is True
        assert result.signal == scored

    def test_plugins_never_hardcode_sources(self):
        """Verify plugins accept source parameter, not hard-coded."""
        # Test with different sources to ensure no hard-coding
        sources = ["source-1", "source-2", "custom-source"]

        sight = SightPlugin()
        for src in sources:
            signals = sight.reaper_sight_detect(source=src)
            assert signals[0].source == src, "Source must not be hard-coded"

        hearing = HearingPlugin()
        for src in sources:
            signals = hearing.reaper_hearing_detect(source=src)
            assert signals[0].source == src, "Source must not be hard-coded"
