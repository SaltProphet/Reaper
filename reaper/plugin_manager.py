"""
REAPER Plugin Manager

Manages plugin registration and discovery via Pluggy.
Ensures no hard-coded sources or pipeline role mixing.
"""

from typing import List, Optional

import pluggy

from reaper.hookspecs import HookSpecs
from reaper.models import ActionResult, ScoredSignal, Signal


class PluginManager:
    """
    Central plugin manager for REAPER.

    All plugins register via Pluggy. No hard-coding of sources allowed.
    """

    def __init__(self):
        self.pm = pluggy.PluginManager("reaper")
        self.pm.add_hookspecs(HookSpecs)
        self._registered_plugins = []

    def register_plugin(self, plugin: object, name: Optional[str] = None) -> None:
        """
        Register a plugin with the manager.

        Args:
            plugin: Plugin instance implementing one or more hookspecs
            name: Optional plugin name for tracking
        """
        self.pm.register(plugin, name=name)
        self._registered_plugins.append((plugin, name))

    def unregister_plugin(self, plugin: object) -> None:
        """Unregister a plugin."""
        self.pm.unregister(plugin)
        self._registered_plugins = [(p, n) for p, n in self._registered_plugins if p != plugin]

    def detect_sight(self, source: str) -> List[Signal]:
        """Detect signals via Sight sense plugins."""
        results = self.pm.hook.reaper_sight_detect(source=source)
        return [signal for result in results for signal in (result or [])]

    def detect_hearing(self, source: str) -> List[Signal]:
        """Detect signals via Hearing sense plugins."""
        results = self.pm.hook.reaper_hearing_detect(source=source)
        return [signal for result in results for signal in (result or [])]

    def detect_touch(self, source: str) -> List[Signal]:
        """Detect signals via Touch sense plugins."""
        results = self.pm.hook.reaper_touch_detect(source=source)
        return [signal for result in results for signal in (result or [])]

    def detect_taste(self, source: str) -> List[Signal]:
        """Detect signals via Taste sense plugins."""
        results = self.pm.hook.reaper_taste_detect(source=source)
        return [signal for result in results for signal in (result or [])]

    def detect_smell(self, source: str) -> List[Signal]:
        """Detect signals via Smell sense plugins."""
        results = self.pm.hook.reaper_smell_detect(source=source)
        return [signal for result in results for signal in (result or [])]

    def score_signal(self, signal: Signal) -> List[ScoredSignal]:
        """Score a signal via scoring plugins."""
        results = self.pm.hook.reaper_score_signal(signal=signal)
        return [r for r in results if r is not None]

    def execute_action(self, scored_signal: ScoredSignal) -> List[ActionResult]:
        """Execute actions via Action sense plugins."""
        results = self.pm.hook.reaper_action_execute(scored_signal=scored_signal)
        return [r for r in results if r is not None]

    def list_plugins(self) -> List[tuple]:
        """List all registered plugins."""
        return self._registered_plugins.copy()
