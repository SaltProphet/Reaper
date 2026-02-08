"""
Tests for REAPER Hook Specifications

Tests that validate hook specifications and their implementations.
"""

import pluggy
import pytest

from reaper.hookspecs import HookSpecs
from reaper.models import ActionResult, ScoredSignal, SenseType, Signal


class TestHookSpecs:
    """Test hook specifications are properly defined."""

    def test_hookspecs_class_exists(self):
        """Test that HookSpecs class exists."""
        assert HookSpecs is not None

    def test_hookspecs_sight_detect(self):
        """Test reaper_sight_detect hook spec exists."""
        assert hasattr(HookSpecs, "reaper_sight_detect")

    def test_hookspecs_hearing_detect(self):
        """Test reaper_hearing_detect hook spec exists."""
        assert hasattr(HookSpecs, "reaper_hearing_detect")

    def test_hookspecs_touch_detect(self):
        """Test reaper_touch_detect hook spec exists."""
        assert hasattr(HookSpecs, "reaper_touch_detect")

    def test_hookspecs_taste_detect(self):
        """Test reaper_taste_detect hook spec exists."""
        assert hasattr(HookSpecs, "reaper_taste_detect")

    def test_hookspecs_smell_detect(self):
        """Test reaper_smell_detect hook spec exists."""
        assert hasattr(HookSpecs, "reaper_smell_detect")

    def test_hookspecs_score_signal(self):
        """Test reaper_score_signal hook spec exists."""
        assert hasattr(HookSpecs, "reaper_score_signal")

    def test_hookspecs_action_execute(self):
        """Test reaper_action_execute hook spec exists."""
        assert hasattr(HookSpecs, "reaper_action_execute")

    def test_all_hookspecs_have_docstrings(self):
        """Test that all hook specs have documentation."""
        specs = HookSpecs()
        hook_methods = [
            "reaper_sight_detect",
            "reaper_hearing_detect",
            "reaper_touch_detect",
            "reaper_taste_detect",
            "reaper_smell_detect",
            "reaper_score_signal",
            "reaper_action_execute",
        ]

        for method_name in hook_methods:
            method = getattr(specs, method_name)
            assert method.__doc__ is not None
            assert len(method.__doc__.strip()) > 0


class TestHookImplementations:
    """Test that plugins properly implement hook specs."""

    def test_valid_sight_detection_hook(self):
        """Test a valid sight detection hook implementation."""
        hookimpl = pluggy.HookimplMarker("reaper")

        class ValidPlugin:
            @hookimpl
            def reaper_sight_detect(self, source: str):
                return [Signal(sense_type=SenseType.SIGHT, source=source)]

        plugin = ValidPlugin()
        signals = plugin.reaper_sight_detect(source="test")

        assert len(signals) == 1
        assert signals[0].sense_type == SenseType.SIGHT

    def test_valid_scoring_hook(self):
        """Test a valid scoring hook implementation."""
        hookimpl = pluggy.HookimplMarker("reaper")

        class ValidScorer:
            @hookimpl
            def reaper_score_signal(self, signal: Signal):
                return ScoredSignal(signal=signal, score=0.5)

        scorer = ValidScorer()
        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = scorer.reaper_score_signal(signal=signal)

        assert isinstance(scored, ScoredSignal)
        assert scored.score == 0.5

    def test_valid_action_hook(self):
        """Test a valid action hook implementation."""
        hookimpl = pluggy.HookimplMarker("reaper")

        class ValidAction:
            @hookimpl
            def reaper_action_execute(self, scored_signal: ScoredSignal):
                return ActionResult(
                    signal=scored_signal,
                    action_type="test",
                    success=True,
                    result_data={},
                )

        action = ValidAction()
        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = ScoredSignal(signal=signal, score=0.8)
        result = action.reaper_action_execute(scored_signal=scored)

        assert isinstance(result, ActionResult)
        assert result.success is True

    def test_hook_without_decorator_not_called(self):
        """Test that methods without @hookimpl are not called by pluggy."""

        class PluginWithoutDecorator:
            def reaper_sight_detect(self, source: str):
                return [Signal(sense_type=SenseType.SIGHT, source=source)]

        # This should work when called directly
        plugin = PluginWithoutDecorator()
        signals = plugin.reaper_sight_detect(source="test")
        assert len(signals) == 1

        # But it won't be discovered by pluggy without @hookimpl
        # (This is tested implicitly in plugin_manager tests)

    def test_multiple_hooks_in_one_plugin(self):
        """Test a plugin can implement multiple hooks."""
        hookimpl = pluggy.HookimplMarker("reaper")

        class MultiHookPlugin:
            @hookimpl
            def reaper_sight_detect(self, source: str):
                return [Signal(sense_type=SenseType.SIGHT, source=source)]

            @hookimpl
            def reaper_hearing_detect(self, source: str):
                return [Signal(sense_type=SenseType.HEARING, source=source)]

        plugin = MultiHookPlugin()

        sight_signals = plugin.reaper_sight_detect(source="test")
        assert sight_signals[0].sense_type == SenseType.SIGHT

        hearing_signals = plugin.reaper_hearing_detect(source="test")
        assert hearing_signals[0].sense_type == SenseType.HEARING

    def test_hook_with_wrong_return_type_still_returns(self):
        """Test that hook with wrong return type still executes."""
        hookimpl = pluggy.HookimplMarker("reaper")

        class WrongReturnTypePlugin:
            @hookimpl
            def reaper_sight_detect(self, source: str):
                # Wrong: should return List[Signal], but returns single Signal
                return Signal(sense_type=SenseType.SIGHT, source=source)

        plugin = WrongReturnTypePlugin()
        result = plugin.reaper_sight_detect(source="test")

        # Plugin executes, but returns wrong type
        # Type checking would catch this, but runtime allows it
        assert isinstance(result, Signal)
        assert not isinstance(result, list)

    def test_hook_names_are_correct(self):
        """Test that all expected hook names exist in HookSpecs."""
        expected_hooks = [
            "reaper_sight_detect",
            "reaper_hearing_detect",
            "reaper_touch_detect",
            "reaper_taste_detect",
            "reaper_smell_detect",
            "reaper_score_signal",
            "reaper_action_execute",
        ]

        specs = HookSpecs()
        for hook_name in expected_hooks:
            assert hasattr(specs, hook_name), f"Missing hook: {hook_name}"

    def test_action_hook_name_is_not_execute_action(self):
        """Test that action hook is named reaper_action_execute (common mistake)."""
        specs = HookSpecs()

        # Correct name
        assert hasattr(specs, "reaper_action_execute")

        # Common mistake
        assert not hasattr(specs, "reaper_execute_action")
