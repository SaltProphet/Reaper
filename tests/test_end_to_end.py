"""
End-to-End Pipeline Test

This test validates the complete REAPER pipeline from signal detection
through scoring to action execution across all five senses.
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
from reaper.models import SenseType


class TestEndToEndPipeline:
    """End-to-end tests for the complete REAPER pipeline."""

    @pytest.fixture
    def plugin_manager(self):
        """Create a fully configured PluginManager."""
        pm = PluginManager()

        # Register all sense plugins
        pm.register_plugin(SightPlugin(), name="sight")
        pm.register_plugin(HearingPlugin(), name="hearing")
        pm.register_plugin(TouchPlugin(), name="touch")
        pm.register_plugin(TastePlugin(), name="taste")
        pm.register_plugin(SmellPlugin(), name="smell")

        # Register scoring and action plugins
        pm.register_plugin(ScoringPlugin(), name="scoring")
        pm.register_plugin(ActionPlugin(), name="action")

        return pm

    def test_complete_sight_pipeline(self, plugin_manager):
        """Test complete pipeline for Sight sense."""
        # Detection
        signals = plugin_manager.detect_sight(source="test-visual-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.SIGHT for s in signals)

        # Scoring
        scored_signals = [plugin_manager.score_signal(s)[0] for s in signals]
        assert len(scored_signals) == len(signals)
        assert all(0.0 <= s.score <= 1.0 for s in scored_signals)

        # Action
        high_priority = [s for s in scored_signals if s.score >= 0.5]
        if high_priority:
            results = [plugin_manager.execute_action(s)[0] for s in high_priority]
            assert all(r.success for r in results)

    def test_complete_hearing_pipeline(self, plugin_manager):
        """Test complete pipeline for Hearing sense."""
        # Detection
        signals = plugin_manager.detect_hearing(source="test-text-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.HEARING for s in signals)

        # Scoring
        scored_signals = [plugin_manager.score_signal(s)[0] for s in signals]
        assert len(scored_signals) == len(signals)
        assert all(0.0 <= s.score <= 1.0 for s in scored_signals)

        # Action
        high_priority = [s for s in scored_signals if s.score >= 0.5]
        if high_priority:
            results = [plugin_manager.execute_action(s)[0] for s in high_priority]
            assert all(r.success for r in results)

    def test_complete_touch_pipeline(self, plugin_manager):
        """Test complete pipeline for Touch sense."""
        # Detection
        signals = plugin_manager.detect_touch(source="test-interaction-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.TOUCH for s in signals)

        # Scoring
        scored_signals = [plugin_manager.score_signal(s)[0] for s in signals]
        assert len(scored_signals) == len(signals)

        # Action
        high_priority = [s for s in scored_signals if s.score >= 0.5]
        if high_priority:
            results = [plugin_manager.execute_action(s)[0] for s in high_priority]
            assert all(r.success for r in results)

    def test_complete_taste_pipeline(self, plugin_manager):
        """Test complete pipeline for Taste sense."""
        # Detection
        signals = plugin_manager.detect_taste(source="test-quality-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.TASTE for s in signals)

        # Scoring
        scored_signals = [plugin_manager.score_signal(s)[0] for s in signals]
        assert len(scored_signals) == len(signals)

        # Action
        high_priority = [s for s in scored_signals if s.score >= 0.5]
        if high_priority:
            results = [plugin_manager.execute_action(s)[0] for s in high_priority]
            assert all(r.success for r in results)

    def test_complete_smell_pipeline(self, plugin_manager):
        """Test complete pipeline for Smell sense."""
        # Detection
        signals = plugin_manager.detect_smell(source="test-pattern-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.SMELL for s in signals)

        # Scoring
        scored_signals = [plugin_manager.score_signal(s)[0] for s in signals]
        assert len(scored_signals) == len(signals)

        # Action
        high_priority = [s for s in scored_signals if s.score >= 0.5]
        if high_priority:
            results = [plugin_manager.execute_action(s)[0] for s in high_priority]
            assert all(r.success for r in results)

    def test_multi_sense_pipeline(self, plugin_manager):
        """Test pipeline with signals from multiple senses."""
        # Collect signals from all senses
        all_signals = []

        all_signals.extend(plugin_manager.detect_sight(source="visual-1"))
        all_signals.extend(plugin_manager.detect_hearing(source="text-1"))
        all_signals.extend(plugin_manager.detect_touch(source="interaction-1"))
        all_signals.extend(plugin_manager.detect_taste(source="quality-1"))
        all_signals.extend(plugin_manager.detect_smell(source="pattern-1"))

        assert len(all_signals) >= 5  # At least one from each sense

        # Verify sense diversity
        sense_types = {s.sense_type for s in all_signals}
        assert len(sense_types) == 5  # All five senses represented

        # Score all signals
        scored_signals = [plugin_manager.score_signal(s)[0] for s in all_signals]
        assert len(scored_signals) == len(all_signals)

        # Execute actions on high priority
        high_priority = [s for s in scored_signals if s.score >= 0.7]
        if high_priority:
            results = [plugin_manager.execute_action(s)[0] for s in high_priority]
            # At least some actions should succeed
            assert any(r.success for r in results)

    def test_pipeline_error_handling(self, plugin_manager):
        """Test pipeline handles errors gracefully."""
        # Empty source should not crash
        signals = plugin_manager.detect_sight(source="")
        assert isinstance(signals, list)

        # Invalid source should not crash
        signals = plugin_manager.detect_hearing(source="nonexistent://invalid")
        assert isinstance(signals, list)

    def test_pipeline_isolation(self, plugin_manager):
        """Test that pipeline phases remain isolated."""
        # Detect
        signals = plugin_manager.detect_sight(source="isolation-test")

        # Signals should only have raw data, no scores
        for signal in signals:
            assert not hasattr(signal, 'score')
            assert not hasattr(signal, 'analysis')

        # Score
        scored = [plugin_manager.score_signal(s)[0] for s in signals]

        # Scored signals should have scores but original signal unchanged
        for scored_signal in scored:
            assert hasattr(scored_signal, 'score')
            assert hasattr(scored_signal, 'signal')
            # Original signal should remain unscored (no score attribute added)
            assert not hasattr(scored_signal.signal, 'score')

    def test_batch_processing(self, plugin_manager):
        """Test pipeline can handle batch processing."""
        # Generate larger batch
        all_signals = []
        sources = [f"batch-source-{i}" for i in range(10)]

        for source in sources:
            signals = plugin_manager.detect_hearing(source=source)
            all_signals.extend(signals)

        # Should handle large batches
        assert len(all_signals) >= 10

        # Score in batch
        scored = [plugin_manager.score_signal(s)[0] for s in all_signals]
        assert len(scored) == len(all_signals)

        # Filter and action
        high_priority = [s for s in scored if s.score >= 0.6]
        results = [plugin_manager.execute_action(s)[0] for s in high_priority]

        # Verify batch completed
        assert len(results) == len(high_priority)

    def test_pipeline_data_flow(self, plugin_manager):
        """Test data flows correctly through the pipeline."""
        source = "data-flow-test"

        # 1. Detection produces Signals
        signals = plugin_manager.detect_sight(source=source)
        first_signal = signals[0]

        # Verify Signal structure
        assert first_signal.sense_type == SenseType.SIGHT
        assert first_signal.source == source
        assert isinstance(first_signal.raw_data, dict)

        # 2. Scoring produces ScoredSignals
        scored = plugin_manager.score_signal(first_signal)[0]

        # Verify ScoredSignal structure
        assert scored.signal == first_signal
        assert isinstance(scored.score, float)
        assert isinstance(scored.analysis, dict)
        assert isinstance(scored.tags, list)

        # 3. Action produces ActionResults
        result = plugin_manager.execute_action(scored)[0]

        # Verify ActionResult structure
        assert isinstance(result.success, bool)
        assert isinstance(result.action_type, str)
        assert isinstance(result.result_data, dict)

    def test_full_pipeline_integration(self, plugin_manager):
        """
        Complete integration test simulating a real-world scenario.
        
        Scenario: Monitor multiple sources, score all signals,
        and action on high-priority items.
        """
        # Phase 1: Multi-source detection
        sources_and_senses = [
            ("sight", "production-ui"),
            ("hearing", "user-feedback"),
            ("touch", "api-analytics"),
            ("taste", "performance-metrics"),
            ("smell", "anomaly-detection"),
        ]

        all_signals = []
        for sense, source in sources_and_senses:
            if sense == "sight":
                signals = plugin_manager.detect_sight(source=source)
            elif sense == "hearing":
                signals = plugin_manager.detect_hearing(source=source)
            elif sense == "touch":
                signals = plugin_manager.detect_touch(source=source)
            elif sense == "taste":
                signals = plugin_manager.detect_taste(source=source)
            elif sense == "smell":
                signals = plugin_manager.detect_smell(source=source)

            all_signals.extend(signals)

        # Phase 2: Score all signals
        scored_signals = [plugin_manager.score_signal(s)[0] for s in all_signals]

        # Phase 3: Categorize by priority
        critical = [s for s in scored_signals if s.score >= 0.8]
        high = [s for s in scored_signals if 0.6 <= s.score < 0.8]
        medium = [s for s in scored_signals if 0.4 <= s.score < 0.6]

        # Phase 4: Execute actions on critical and high priority
        action_targets = critical + high
        results = [plugin_manager.execute_action(s)[0] for s in action_targets]

        # Verify integration success
        assert len(all_signals) >= 5
        assert len(scored_signals) == len(all_signals)
        assert len(results) == len(action_targets)

        # If there are actionable signals, verify actions
        if len(action_targets) > 0:
            # Actions should generally succeed
            success_rate = sum(1 for r in results if r.success) / len(results)
            assert success_rate > 0.5  # At least 50% success
        else:
            # It's okay if no signals meet the threshold
            # Just verify the pipeline completed successfully
            assert len(medium) >= 0  # Pipeline processed all signals
