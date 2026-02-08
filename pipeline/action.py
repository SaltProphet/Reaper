"""
Action Sense Pipeline Stub

Execute actions based on scored signals.
Each sense = one job. Never mix pipeline roles.
"""
import pluggy

from reaper.models import ActionResult, ScoredSignal

hookimpl = pluggy.HookimplMarker("reaper")


class ActionPlugin:
    """
    Stub plugin for Action sense (execute actions on signals).

    This is a reference implementation. Real plugins should:
    - Never hard-code actions in core
    - Take appropriate actions based on scored signals
    - Return properly validated ActionResult objects
    """

    @hookimpl
    def reaper_action_execute(self, scored_signal: ScoredSignal) -> ActionResult:
        """
        Execute action based on scored signal.

        Args:
            scored_signal: Signal with score to act upon

        Returns:
            Result of the action taken
        """
        # Stub implementation - real plugin would execute meaningful actions
        return ActionResult(
            signal=scored_signal,
            action_type="stub_action",
            success=True,
            result_data={
                "description": "Stub action executed successfully",
                "stub": True,
            },
        )
