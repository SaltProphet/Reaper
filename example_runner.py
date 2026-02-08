"""
Example REAPER Pipeline Runner

Demonstrates how to use the plugin-driven system.
Never hard-codes sources - everything is plugin-based.
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
    pm = PluginManager()

    # Register all sense plugins
    print("Registering plugins...")
    pm.register_plugin(SightPlugin(), name="sight")
    pm.register_plugin(HearingPlugin(), name="hearing")
    pm.register_plugin(TouchPlugin(), name="touch")
    pm.register_plugin(TastePlugin(), name="taste")
    pm.register_plugin(SmellPlugin(), name="smell")
    pm.register_plugin(ScoringPlugin(), name="scoring")
    pm.register_plugin(ActionPlugin(), name="action")

    print(f"Registered {pm.plugin_count()} plugins\n")

    # Detect signals from each sense (sources are plugin-specific, not hard-coded)
    print("=== DETECTION PHASE ===")

    print("\n1. SIGHT Detection:")
    sight_signals = pm.detect_sight(source="example-visual-source")
    for signal in sight_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    print("\n2. HEARING Detection:")
    hearing_signals = pm.detect_hearing(source="example-audio-source")
    for signal in hearing_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    print("\n3. TOUCH Detection:")
    touch_signals = pm.detect_touch(source="example-sensor-source")
    for signal in touch_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    print("\n4. TASTE Detection:")
    taste_signals = pm.detect_taste(source="example-quality-source")
    for signal in taste_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    print("\n5. SMELL Detection:")
    smell_signals = pm.detect_smell(source="example-pattern-source")
    for signal in smell_signals:
        print(f"   - Detected: {signal.sense_type.value} from {signal.source}")
        print(f"     Data: {signal.raw_data}")

    # Collect all signals efficiently using itertools.chain
    all_signals = list(
        chain(sight_signals, hearing_signals, touch_signals, taste_signals, smell_signals)
    )

    # Score signals
    print("\n\n=== SCORING PHASE ===")
    scored_signals = []
    for signal in all_signals:
        scored = pm.score_signal(signal)
        if scored:
            scored_signals.append(scored[0])
            print(f"   - Scored {signal.sense_type.value}: {scored[0].score}")
            print(f"     Tags: {scored[0].tags}")

    # Execute actions
    print("\n\n=== ACTION PHASE ===")
    for scored_signal in scored_signals:
        results = pm.execute_action(scored_signal)
        for result in results:
            status = "✓" if result.success else "✗"
            sense_type = scored_signal.signal.sense_type.value
            print(f"   {status} Action '{result.action_type}' on {sense_type}")
            if result.error:
                print(f"     Error: {result.error}")
            else:
                print(f"     Result: {result.result_data}")

    print("\n\n=== PIPELINE COMPLETE ===")
    print(f"Processed {len(all_signals)} signals from {pm.plugin_count()} plugins")


if __name__ == "__main__":
    main()
