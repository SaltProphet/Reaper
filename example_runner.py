"""
Example REAPER Pipeline Runner

Demonstrates the complete end-to-end REAPER pipeline:
1. Detection across 5 senses (Sight, Hearing, Touch, Taste, Smell)
2. Scoring of detected signals
3. Action execution on scored signals

This example showcases the plugin-driven architecture where:
- All functionality is provided by plugins (no hard-coding)
- Sources are plugin-specific (passed as parameters, never hard-coded)
- Pipeline roles remain separated (detect → score → act)
- Type-safe data flows through Pydantic models
"""

from itertools import chain

from pipeline.action import ActionPlugin
from pipeline.hearing import HearingPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.sight import SightPlugin
from pipeline.smell import SmellPlugin
from pipeline.taste import TastePlugin
from pipeline.touch import TouchPlugin
from reaper import PluginManager


def main():
    """Run example pipeline demonstrating all 5 senses + action."""

    # Initialize plugin manager
    # The PluginManager is the core coordinator that:
    # - Registers plugins implementing hook specifications
    # - Routes method calls to registered plugins via Pluggy
    # - Returns aggregated results from all registered plugins
    pm = PluginManager()

    # Register all sense plugins
    # Each plugin implements specific hook specifications from reaper.hookspecs
    # Plugins are modular and can be added/removed without changing core
    print("Registering plugins...")
    pm.register_plugin(SightPlugin(), name="sight")  # Visual detection
    pm.register_plugin(HearingPlugin(), name="hearing")  # Audio/text detection
    pm.register_plugin(TouchPlugin(), name="touch")  # Interaction detection
    pm.register_plugin(TastePlugin(), name="taste")  # Quality/sampling detection
    pm.register_plugin(SmellPlugin(), name="smell")  # Pattern/anomaly detection
    pm.register_plugin(ScoringPlugin(), name="scoring")  # Signal scoring
    pm.register_plugin(ActionPlugin(), name="action")  # Action execution

    print(f"Registered {pm.plugin_count()} plugins\n")
    print("Note: These are stub implementations. In production, you would")
    print("      register real plugins (e.g., GitHubIssueDetector, SlackNotifier)\n")

    # Detection Phase: Each sense detects signals from its domain
    # Sources are plugin-specific identifiers (never hard-coded in core)
    # Each plugin decides how to interpret its source parameter
    print("=== DETECTION PHASE ===")
    print("Collecting signals from all 5 senses...\n")

    print("1. SIGHT Detection (Visual signals):")
    # Example: In production, source might be "github.com/org/repo/issues"
    sight_signals = pm.detect_sight(source="example-visual-source")
    for signal in sight_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    print("\n2. HEARING Detection (Audio/Text signals):")
    # Example: In production, source might be "slack.com/channel/engineering"
    hearing_signals = pm.detect_hearing(source="example-audio-source")
    for signal in hearing_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    print("\n3. TOUCH Detection (Interaction signals):")
    # Example: In production, source might be "api.company.com/analytics"
    touch_signals = pm.detect_touch(source="example-sensor-source")
    for signal in touch_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    print("\n4. TASTE Detection (Quality/Sampling signals):")
    # Example: In production, source might be "monitoring.company.com/metrics"
    taste_signals = pm.detect_taste(source="example-quality-source")
    for signal in taste_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    print("\n5. SMELL Detection (Pattern/Anomaly signals):")
    # Example: In production, source might be "logs.company.com/errors"
    smell_signals = pm.detect_smell(source="example-pattern-source")
    for signal in smell_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    # Aggregate all detected signals
    # Using itertools.chain for efficient concatenation without intermediate lists
    all_signals = list(
        chain(sight_signals, hearing_signals, touch_signals, taste_signals, smell_signals)
    )
    print(f"\nTotal signals detected: {len(all_signals)}")

    # Scoring Phase: Evaluate the importance/priority of each signal
    # Scoring plugins analyze signals and assign scores (0.0-1.0)
    # Higher scores indicate higher priority/urgency
    print("\n\n=== SCORING PHASE ===")
    print("Evaluating signal priorities...\n")
    scored_signals = []
    for signal in all_signals:
        # score_signal returns a list (multiple scorers can provide different scores)
        scored = pm.score_signal(signal)
        if scored:
            scored_signals.append(scored[0])
            print(f"   - Scored {signal.sense_type.value}: {scored[0].score:.2f}")
            print(f"     Tags: {scored[0].tags}")
            print(f"     Analysis: {scored[0].analysis}")

    # Action Phase: Execute actions on high-priority signals
    # Actions are triggered based on scored signals
    # Examples: create tickets, send notifications, trigger automations
    print("\n\n=== ACTION PHASE ===")
    print("Executing actions on scored signals...\n")
    for scored_signal in scored_signals:
        # execute_action returns a list (multiple action plugins can act on same signal)
        results = pm.execute_action(scored_signal)
        for result in results:
            status = "✓" if result.success else "✗"
            sense_type = scored_signal.signal.sense_type.value
            print(f"   {status} Action '{result.action_type}' on {sense_type} signal")
            if result.error:
                print(f"     Error: {result.error}")
            else:
                print(f"     Result: {result.result_data}")

    # Pipeline Summary
    print("\n\n=== PIPELINE COMPLETE ===")
    print(f"✓ Detected {len(all_signals)} signals across 5 senses")
    print(f"✓ Scored {len(scored_signals)} signals")
    print(f"✓ Executed {len(scored_signals)} actions")
    print(f"✓ Using {pm.plugin_count()} registered plugins")
    print("\nNext Steps:")
    print("  1. Create real plugins by implementing hook specifications")
    print("  2. Register your plugins with the PluginManager")
    print("  3. Deploy and monitor your REAPER pipeline")
    print("\nSee CONTRIBUTING.md for plugin development guide.")


if __name__ == "__main__":
    main()
