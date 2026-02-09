#!/usr/bin/env python3
"""
Plugin Template Generator CLI

Minimal scaffolding tool to create new REAPER plugins under reaper/plugins/.
Generates a plugin directory with __init__.py and template code.

Usage:
    python scripts/new_plugin.py my_plugin
    python scripts/new_plugin.py my_plugin --hook reaper_score_signal
"""

import argparse
import sys
from pathlib import Path

PLUGIN_TEMPLATE = '''"""
{plugin_name} Plugin

Auto-generated plugin scaffold. Implement your hook logic below.
"""

import pluggy

from reaper.models import Signal, ScoredSignal, SenseType

hookimpl = pluggy.HookimplMarker("reaper")


class {class_name}:
    """
    {plugin_name} plugin implementation.

    TODO: Add plugin description and configuration details.
    """

    @hookimpl
    def {hook_name}(self, {hook_params}):
        """
        {hook_docstring}

        Args:
            {hook_args_doc}

        Returns:
            {hook_return_doc}
        """
        # TODO: Implement plugin logic
        {hook_return_example}
'''


HOOK_CONFIGS = {
    "reaper_sight_detect": {
        "params": "source: str",
        "args_doc": "source: Source identifier for detection",
        "return_doc": "List[Signal]: Detected signals with sense_type=SIGHT",
        "return_example": 'return [Signal(sense_type=SenseType.SIGHT, source=source)]',
        "docstring": "Detect visual signals from source.",
    },
    "reaper_hearing_detect": {
        "params": "source: str",
        "args_doc": "source: Source identifier for detection",
        "return_doc": "List[Signal]: Detected signals with sense_type=HEARING",
        "return_example": 'return [Signal(sense_type=SenseType.HEARING, source=source)]',
        "docstring": "Detect audio/text signals from source.",
    },
    "reaper_touch_detect": {
        "params": "source: str",
        "args_doc": "source: Source identifier for detection",
        "return_doc": "List[Signal]: Detected signals with sense_type=TOUCH",
        "return_example": 'return [Signal(sense_type=SenseType.TOUCH, source=source)]',
        "docstring": "Detect interaction signals from source.",
    },
    "reaper_taste_detect": {
        "params": "source: str",
        "args_doc": "source: Source identifier for detection",
        "return_doc": "List[Signal]: Detected signals with sense_type=TASTE",
        "return_example": 'return [Signal(sense_type=SenseType.TASTE, source=source)]',
        "docstring": "Detect quality/sampling signals from source.",
    },
    "reaper_smell_detect": {
        "params": "source: str",
        "args_doc": "source: Source identifier for detection",
        "return_doc": "List[Signal]: Detected signals with sense_type=SMELL",
        "return_example": 'return [Signal(sense_type=SenseType.SMELL, source=source)]',
        "docstring": "Detect pattern/anomaly signals from source.",
    },
    "reaper_score_signal": {
        "params": "signal: Signal",
        "args_doc": "signal: Signal to score",
        "return_doc": "ScoredSignal: Signal with score and analysis",
        "return_example": (
            "return ScoredSignal(\n            signal=signal,\n            score=0.5,\n"
            '            analysis={"method": "TODO"},\n            tags=["todo"]\n        )'
        ),
        "docstring": "Score a detected signal.",
    },
    "reaper_action_execute": {
        "params": "scored_signal: ScoredSignal",
        "args_doc": "scored_signal: Scored signal to act upon",
        "return_doc": "ActionResult: Result of action execution",
        "return_example": """from reaper.models import ActionResult
        return ActionResult(
            signal=scored_signal,
            action_type="TODO",
            success=True,
            result_data={"status": "completed"}
        )""",
        "docstring": "Execute action on scored signal.",
    },
}


def snake_to_pascal(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(word.capitalize() for word in snake_str.split("_"))


def create_plugin(plugin_name: str, hook_name: str = "reaper_score_signal") -> None:
    """
    Create a new plugin directory with template code.

    Args:
        plugin_name: Name of the plugin (snake_case)
        hook_name: Hook to implement (default: reaper_score_signal)
    """
    # Validate hook name
    if hook_name not in HOOK_CONFIGS:
        print(f"Error: Unknown hook '{hook_name}'")
        print(f"Available hooks: {', '.join(HOOK_CONFIGS.keys())}")
        sys.exit(1)

    # Setup paths
    repo_root = Path(__file__).parent.parent
    plugin_dir = repo_root / "reaper" / "plugins" / plugin_name

    # Check if plugin already exists
    if plugin_dir.exists():
        print(f"Error: Plugin directory already exists: {plugin_dir}")
        sys.exit(1)

    # Create plugin directory
    plugin_dir.mkdir(parents=True, exist_ok=True)

    # Get hook configuration
    hook_config = HOOK_CONFIGS[hook_name]

    # Generate plugin code
    class_name = snake_to_pascal(plugin_name) + "Plugin"
    plugin_code = PLUGIN_TEMPLATE.format(
        plugin_name=plugin_name.replace("_", " ").title(),
        class_name=class_name,
        hook_name=hook_name,
        hook_params=hook_config["params"],
        hook_args_doc=hook_config["args_doc"],
        hook_return_doc=hook_config["return_doc"],
        hook_return_example=hook_config["return_example"],
        hook_docstring=hook_config["docstring"],
    )

    # Write __init__.py
    init_file = plugin_dir / "__init__.py"
    init_file.write_text(plugin_code)

    print(f"✓ Created plugin: {plugin_dir}")
    print(f"✓ Implemented hook: {hook_name}")
    print("\nNext steps:")
    print(f"  1. Edit {init_file}")
    print("  2. Implement your plugin logic")
    print(
        f"  3. Register with PluginManager: "
        f"pm.register_plugin({class_name}(), name='{plugin_name}')"
    )
    print(f"  4. Add tests in tests/unit/test_{plugin_name}.py")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a new REAPER plugin scaffold",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "plugin_name",
        help="Plugin name in snake_case (e.g., my_plugin)",
    )
    parser.add_argument(
        "--hook",
        default="reaper_score_signal",
        choices=list(HOOK_CONFIGS.keys()),
        help="Hook to implement (default: reaper_score_signal)",
    )

    args = parser.parse_args()
    create_plugin(args.plugin_name, args.hook)


if __name__ == "__main__":
    main()
