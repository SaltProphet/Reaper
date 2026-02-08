"""
Edge Case Tests for REAPER Plugin System

Tests plugin loading failures, edge cases, and error handling.
"""

import pytest

from pipeline.action import ActionPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.sight import SightPlugin
from reaper import PluginManager
from reaper.models import ScoredSignal, SenseType, Signal


class FaultyPlugin:
    """Plugin that raises errors for testing isolation."""

    def reaper_sight_detect(self, source: str):
        """Intentionally faulty detection."""
        raise RuntimeError("Faulty plugin error")


class TestPluginEdgeCases:
    """Test edge cases in plugin management."""

    def test_unregister_nonexistent_plugin(self):
        """Test unregistering a plugin that was never registered."""
        pm = PluginManager()
        plugin = SightPlugin()
        # Pluggy raises AssertionError when unregistering non-existent plugin
        with pytest.raises(AssertionError, match="plugin is not registered"):
            pm.unregister_plugin(plugin)
        assert pm.plugin_count() == 0

    def test_register_same_plugin_multiple_times(self):
        """Test registering the same plugin multiple times raises error."""
        pm = PluginManager()
        plugin = SightPlugin()
        pm.register_plugin(plugin, name="sight-1")
        # Pluggy doesn't allow same plugin instance multiple times
        with pytest.raises(ValueError, match="Plugin already registered"):
            pm.register_plugin(plugin, name="sight-2")
        assert pm.plugin_count() == 1

    def test_empty_source_handling(self):
        """Test detection with empty source string."""
        pm = PluginManager()
        pm.register_plugin(SightPlugin())

        # Empty source should not crash
        signals = pm.detect_sight(source="")
        assert isinstance(signals, list)
        # Plugin should still return signals with empty source
        assert len(signals) > 0
        assert signals[0].source == ""

    def test_special_characters_in_source(self):
        """Test detection with special characters in source."""
        pm = PluginManager()
        pm.register_plugin(SightPlugin())

        special_sources = [
            "source://with:special@chars",
            "path/to/resource?param=value",
            "unicode-source-\u2764\ufe0f",
            "spaces in source",
        ]

        for source in special_sources:
            signals = pm.detect_sight(source=source)
            assert len(signals) > 0
            assert signals[0].source == source

    def test_no_plugins_registered(self):
        """Test calling hooks when no plugins are registered."""
        pm = PluginManager()

        # Should return empty lists when no plugins registered
        assert pm.detect_sight(source="test") == []
        assert pm.detect_hearing(source="test") == []
        assert pm.detect_touch(source="test") == []
        assert pm.detect_taste(source="test") == []
        assert pm.detect_smell(source="test") == []

    def test_plugin_isolation_detection_failure(self):
        """Test that faulty plugin registration works."""
        pm = PluginManager()
        # FaultyPlugin doesn't have @hookimpl decorator, so it won't be called
        # This tests that plugins without proper decorators are silently ignored
        pm.register_plugin(FaultyPlugin(), name="faulty")

        # Since FaultyPlugin lacks @hookimpl, it won't be called and returns empty list
        signals = pm.detect_sight(source="test")
        assert isinstance(signals, list)
        assert len(signals) == 0

    def test_multiple_scoring_plugins(self):
        """Test multiple scoring plugins returning different scores."""
        pm = PluginManager()
        pm.register_plugin(ScoringPlugin(), name="scorer-1")
        pm.register_plugin(ScoringPlugin(), name="scorer-2")

        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored_signals = pm.score_signal(signal)

        # Should get results from both scorers
        assert len(scored_signals) == 2
        assert all(isinstance(s, ScoredSignal) for s in scored_signals)

    def test_multiple_action_plugins(self):
        """Test multiple action plugins executing on same signal."""
        pm = PluginManager()
        pm.register_plugin(ActionPlugin(), name="action-1")
        pm.register_plugin(ActionPlugin(), name="action-2")

        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = ScoredSignal(signal=signal, score=0.8)
        results = pm.execute_action(scored)

        # Should get results from both action plugins
        assert len(results) == 2
        assert all(r.success for r in results)

    def test_unregister_plugin_removes_from_list(self):
        """Test that unregistering plugin removes it from list_plugins."""
        pm = PluginManager()
        plugin = SightPlugin()
        pm.register_plugin(plugin, name="sight")

        plugins_before = pm.list_plugins()
        assert len(plugins_before) == 1

        pm.unregister_plugin(plugin)
        plugins_after = pm.list_plugins()
        assert len(plugins_after) == 0

    def test_plugin_list_is_tuple(self):
        """Test that list_plugins returns immutable tuple."""
        pm = PluginManager()
        pm.register_plugin(SightPlugin(), name="sight")

        plugins = pm.list_plugins()
        assert isinstance(plugins, tuple)

        # Tuple should be immutable
        with pytest.raises(TypeError):
            plugins[0] = None  # type: ignore

    def test_signal_with_minimal_data(self):
        """Test signals can be created with minimal required data."""
        signal = Signal(sense_type=SenseType.SIGHT, source="minimal")

        # Should have defaults for optional fields
        assert signal.raw_data == {}
        assert signal.metadata == {}
        assert signal.timestamp is not None

    def test_signal_with_large_raw_data(self):
        """Test signals can handle large raw_data payloads."""
        large_data = {f"key_{i}": f"value_{i}" for i in range(1000)}
        signal = Signal(sense_type=SenseType.HEARING, source="large-data", raw_data=large_data)

        assert len(signal.raw_data) == 1000
        assert signal.raw_data["key_500"] == "value_500"

    def test_scored_signal_boundary_scores(self):
        """Test ScoredSignal with boundary score values."""
        signal = Signal(sense_type=SenseType.TOUCH, source="test")

        # Test minimum valid score
        scored_min = ScoredSignal(signal=signal, score=0.0)
        assert scored_min.score == 0.0

        # Test maximum valid score
        scored_max = ScoredSignal(signal=signal, score=1.0)
        assert scored_max.score == 1.0

    def test_action_result_with_no_error(self):
        """Test ActionResult success case has no error."""
        signal = Signal(sense_type=SenseType.SMELL, source="test")
        scored = ScoredSignal(signal=signal, score=0.9)

        pm = PluginManager()
        pm.register_plugin(ActionPlugin())
        results = pm.execute_action(scored)

        assert results[0].success is True
        assert results[0].error is None

    def test_plugin_count_consistency(self):
        """Test plugin_count matches length of list_plugins."""
        pm = PluginManager()

        assert pm.plugin_count() == len(pm.list_plugins())

        pm.register_plugin(SightPlugin())
        assert pm.plugin_count() == len(pm.list_plugins())

        pm.register_plugin(ScoringPlugin())
        assert pm.plugin_count() == len(pm.list_plugins())
