"""
Integration Tests for Pipeline

Tests end-to-end pipeline behavior with mock plugins:
- MockIngestor (detection) -> KeywordScorer (scoring) -> MockAction (action)

Validates that plugins can be registered, called, and work together.
"""

import pluggy

from reaper import PluginManager
from reaper.models import ActionResult, ScoredSignal, SenseType, Signal
from reaper.plugins.keyword_scorer import KeywordScorerPlugin

hookimpl = pluggy.HookimplMarker("reaper")


class MockIngestorPlugin:
    """Mock detection plugin for integration testing."""

    def __init__(self, signals_to_return: list[Signal] | None = None):
        """
        Initialize mock ingestor.

        Args:
            signals_to_return: Signals to return on detection (default: generates mock signals)
        """
        self.signals_to_return = signals_to_return or []
        self.detect_called = False
        self.last_source = None

    @hookimpl
    def reaper_sight_detect(self, source: str) -> list[Signal]:
        """Mock sight detection."""
        self.detect_called = True
        self.last_source = source

        # Return pre-configured signals or generate defaults
        if self.signals_to_return:
            return self.signals_to_return

        return [
            Signal(
                sense_type=SenseType.SIGHT,
                source=source,
                raw_data={"text": "urgent critical issue"},
            ),
            Signal(
                sense_type=SenseType.SIGHT,
                source=source,
                raw_data={"text": "minor todo item"},
            ),
            Signal(
                sense_type=SenseType.SIGHT,
                source=source,
                raw_data={"text": "normal data with no keywords"},
            ),
        ]


class MockActionPlugin:
    """Mock action plugin for integration testing."""

    def __init__(self):
        """Initialize mock action plugin."""
        self.actions_executed = []

    @hookimpl
    def reaper_action_execute(self, scored_signal: ScoredSignal) -> ActionResult:
        """Mock action execution."""
        self.actions_executed.append(scored_signal)

        return ActionResult(
            signal=scored_signal,
            action_type="mock_notification",
            success=True,
            result_data={
                "notified": True,
                "score": scored_signal.score,
                "tags": scored_signal.tags,
            },
        )


class TestPipelineIntegration:
    """Integration tests for complete pipeline."""

    def test_basic_pipeline_flow(self):
        """Test basic flow: detect -> score -> action."""
        # Setup plugins
        ingestor = MockIngestorPlugin()
        scorer = KeywordScorerPlugin()
        action = MockActionPlugin()

        # Register plugins
        pm = PluginManager()
        pm.register_plugin(ingestor, name="mock_ingestor")
        pm.register_plugin(scorer, name="keyword_scorer")
        pm.register_plugin(action, name="mock_action")

        assert pm.plugin_count() == 3

        # Step 1: Detect signals
        signals = pm.detect_sight(source="test-source")

        assert len(signals) == 3
        assert ingestor.detect_called
        assert ingestor.last_source == "test-source"

        # Step 2: Score signals
        scored_signals = []
        for signal in signals:
            scored_list = pm.score_signal(signal)
            assert len(scored_list) == 1  # One scorer registered
            scored_signals.append(scored_list[0])

        assert len(scored_signals) == 3

        # Verify scores
        # First signal has "urgent critical issue" -> high score
        assert scored_signals[0].score >= 0.7
        # Second signal has "minor todo" -> low score
        assert scored_signals[1].score <= 0.3
        # Third signal has no keywords -> zero score
        assert scored_signals[2].score == 0.0

        # Step 3: Execute actions
        for scored in scored_signals:
            results = pm.execute_action(scored)
            assert len(results) == 1  # One action plugin registered
            assert results[0].success

        # Verify action was called for all signals
        assert len(action.actions_executed) == 3

    def test_pipeline_with_high_priority_signals(self):
        """Test pipeline filters and acts on high-priority signals only."""
        # Create signals with known content
        signals = [
            Signal(
                sense_type=SenseType.SIGHT,
                source="test",
                raw_data={"text": "critical emergency broken"},
            ),
            Signal(
                sense_type=SenseType.SIGHT,
                source="test",
                raw_data={"text": "normal message"},
            ),
        ]

        # Setup
        ingestor = MockIngestorPlugin(signals_to_return=signals)
        scorer = KeywordScorerPlugin()
        action = MockActionPlugin()

        pm = PluginManager()
        pm.register_plugin(ingestor, name="mock_ingestor")
        pm.register_plugin(scorer, name="keyword_scorer")
        pm.register_plugin(action, name="mock_action")

        # Detect
        detected = pm.detect_sight(source="test")
        assert len(detected) == 2

        # Score
        high_priority_scored = []
        for signal in detected:
            scored_list = pm.score_signal(signal)
            scored = scored_list[0]

            # Only act on high priority (score >= 0.7)
            if scored.score >= 0.7:
                high_priority_scored.append(scored)

        assert len(high_priority_scored) == 1
        assert "high_priority" in high_priority_scored[0].tags

        # Act only on high priority
        for scored in high_priority_scored:
            results = pm.execute_action(scored)
            assert results[0].success

        assert len(action.actions_executed) == 1

    def test_multiple_scorers(self):
        """Test pipeline with multiple scoring plugins."""
        # Create second scorer with different weights
        scorer1 = KeywordScorerPlugin()
        scorer2 = KeywordScorerPlugin(
            high_priority=["custom"],
            medium_priority=[],
            low_priority=[],
        )

        ingestor = MockIngestorPlugin(
            signals_to_return=[
                Signal(
                    sense_type=SenseType.SIGHT,
                    source="test",
                    raw_data={"text": "custom urgent message"},
                )
            ]
        )

        pm = PluginManager()
        pm.register_plugin(ingestor, name="mock_ingestor")
        pm.register_plugin(scorer1, name="scorer1")
        pm.register_plugin(scorer2, name="scorer2")

        signals = pm.detect_sight(source="test")
        assert len(signals) == 1

        # Should get scores from both scorers
        scored_list = pm.score_signal(signals[0])
        assert len(scored_list) == 2

        # scorer1 sees "urgent" (0.3)
        # scorer2 sees "custom" (0.3)
        scores = [s.score for s in scored_list]
        assert 0.3 in scores

    def test_plugin_registration_and_unregistration(self):
        """Test dynamic plugin registration/unregistration."""
        pm = PluginManager()

        ingestor = MockIngestorPlugin()
        pm.register_plugin(ingestor, name="ingestor")
        assert pm.plugin_count() == 1

        # Detect works
        signals = pm.detect_sight(source="test")
        assert len(signals) > 0

        # Unregister
        pm.unregister_plugin(ingestor)
        assert pm.plugin_count() == 0

        # Detect returns empty (no plugins)
        signals = pm.detect_sight(source="test")
        assert len(signals) == 0

    def test_action_result_contains_score_info(self):
        """Test that action results include scoring information."""
        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={"text": "urgent bug"},
        )

        scorer = KeywordScorerPlugin()
        action = MockActionPlugin()

        pm = PluginManager()
        pm.register_plugin(scorer, name="scorer")
        pm.register_plugin(action, name="action")

        # Score
        scored_list = pm.score_signal(signal)
        scored = scored_list[0]

        # Execute action
        results = pm.execute_action(scored)
        result = results[0]

        assert result.success
        assert result.result_data["score"] == scored.score
        assert result.result_data["tags"] == scored.tags
        assert (
            "high_priority" in result.result_data["tags"]
            or "medium_priority" in result.result_data["tags"]
        )

    def test_end_to_end_with_mock_data_generator(self):
        """Test pipeline using mock data generator."""
        from tests.mock_data.mock_generator import MockDataGenerator

        gen = MockDataGenerator()

        # Generate signals with known keywords
        signals = [
            gen.signal_with_keywords(["urgent", "critical"]),
            gen.signal_with_keywords(["bug"]),
            gen.signal_with_keywords([]),
        ]

        ingestor = MockIngestorPlugin(signals_to_return=signals)
        scorer = KeywordScorerPlugin()
        action = MockActionPlugin()

        pm = PluginManager()
        pm.register_plugin(ingestor, name="ingestor")
        pm.register_plugin(scorer, name="scorer")
        pm.register_plugin(action, name="action")

        # Run pipeline
        detected = pm.detect_sight(source="test")
        assert len(detected) == 3

        scored_signals = []
        for signal in detected:
            scored_list = pm.score_signal(signal)
            scored_signals.append(scored_list[0])

        # Verify scores match expected keywords
        assert scored_signals[0].score >= 0.6  # urgent + critical
        assert scored_signals[1].score == 0.2  # bug
        assert scored_signals[2].score == 0.0  # no keywords

        # Execute actions
        for scored in scored_signals:
            pm.execute_action(scored)

        assert len(action.actions_executed) == 3

    def test_pipeline_preserves_signal_data(self):
        """Test that signal data is preserved through the pipeline."""
        original_raw_data = {
            "text": "urgent issue",
            "metadata": {"user": "test_user"},
            "timestamp": "2024-01-01T00:00:00Z",
        }

        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test-source",
            raw_data=original_raw_data,
        )

        scorer = KeywordScorerPlugin()
        action = MockActionPlugin()

        pm = PluginManager()
        pm.register_plugin(scorer, name="scorer")
        pm.register_plugin(action, name="action")

        # Score
        scored_list = pm.score_signal(signal)
        scored = scored_list[0]

        # Verify original signal is preserved
        assert scored.signal == signal
        assert scored.signal.raw_data == original_raw_data

        # Execute action
        results = pm.execute_action(scored)
        result = results[0]

        # Verify signal still preserved in action result
        assert result.signal.signal == signal
        assert result.signal.signal.raw_data == original_raw_data

    def test_error_handling_in_pipeline(self):
        """Test pipeline handles errors gracefully."""

        class FailingActionPlugin:
            """Action plugin that always fails."""

            @hookimpl
            def reaper_action_execute(self, scored_signal: ScoredSignal) -> ActionResult:
                """Action that always fails."""
                return ActionResult(
                    signal=scored_signal,
                    action_type="failing_action",
                    success=False,
                    result_data={},
                    error="Simulated failure for testing",
                )

        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={"text": "urgent"},
        )

        scorer = KeywordScorerPlugin()
        failing_action = FailingActionPlugin()

        pm = PluginManager()
        pm.register_plugin(scorer, name="scorer")
        pm.register_plugin(failing_action, name="failing")

        # Score
        scored_list = pm.score_signal(signal)
        scored = scored_list[0]

        # Execute action (should return failure result, not raise exception)
        results = pm.execute_action(scored)
        result = results[0]

        assert not result.success
        assert result.error == "Simulated failure for testing"
        assert result.action_type == "failing_action"
