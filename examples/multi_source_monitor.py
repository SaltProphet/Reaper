"""
Multi-Source Monitor Example

This example demonstrates monitoring multiple sources across different senses.

Run from repository root:
    python examples/multi_source_monitor.py
"""

from pipeline.action import ActionPlugin
from pipeline.hearing import HearingPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.sight import SightPlugin
from pipeline.smell import SmellPlugin
from pipeline.taste import TastePlugin
from pipeline.touch import TouchPlugin
from reaper import PluginManager


def main():
    print("=" * 70)
    print("REAPER Multi-Source Monitor Example")
    print("=" * 70)

    # Initialize
    pm = PluginManager()

    # Register all plugins
    print("\n[1] Registering all sense plugins...")
    pm.register_plugin(SightPlugin(), name="sight")
    pm.register_plugin(HearingPlugin(), name="hearing")
    pm.register_plugin(TouchPlugin(), name="touch")
    pm.register_plugin(TastePlugin(), name="taste")
    pm.register_plugin(SmellPlugin(), name="smell")
    pm.register_plugin(ScoringPlugin(), name="scoring")
    pm.register_plugin(ActionPlugin(), name="action")
    print("    ✓ All plugins registered")

    # Define sources to monitor
    sources = [
        ("sight", "visual-feed-production", "high"),
        ("sight", "visual-feed-staging", "medium"),
        ("hearing", "slack-messages", "high"),
        ("hearing", "log-stream", "medium"),
        ("touch", "api-events", "high"),
        ("taste", "performance-metrics", "high"),
        ("smell", "anomaly-detector", "medium"),
    ]

    print(f"\n[2] Monitoring {len(sources)} sources...")
    all_signals = []

    # Collect signals from all sources
    for sense_type, source, priority in sources:
        print(f"\n    [{sense_type.upper()}] {source} (priority: {priority})")

        try:
            if sense_type == "sight":
                signals = pm.detect_sight(source=source)
            elif sense_type == "hearing":
                signals = pm.detect_hearing(source=source)
            elif sense_type == "touch":
                signals = pm.detect_touch(source=source)
            elif sense_type == "taste":
                signals = pm.detect_taste(source=source)
            elif sense_type == "smell":
                signals = pm.detect_smell(source=source)
            else:
                signals = []

            print(f"        → Detected {len(signals)} signals")

            # Tag signals with priority
            for signal in signals:
                signal.raw_data["source_priority"] = priority

            all_signals.extend(signals)

        except Exception as e:
            print(f"        ✗ Error: {e}")

    print(f"\n[3] Total signals collected: {len(all_signals)}")

    # Score all signals
    print("\n[4] Scoring signals...")
    scored_signals = []
    for signal in all_signals:
        scored = pm.score_signal(signal)[0]
        scored_signals.append(scored)

    # Group by priority
    high_priority = [s for s in scored_signals if s.score >= 0.7]
    medium_priority = [s for s in scored_signals if 0.4 <= s.score < 0.7]
    low_priority = [s for s in scored_signals if s.score < 0.4]

    print(f"    High priority (≥0.7):   {len(high_priority)}")
    print(f"    Medium priority (≥0.4): {len(medium_priority)}")
    print(f"    Low priority (<0.4):    {len(low_priority)}")

    # Execute actions on high-priority signals
    print("\n[5] Executing actions on high-priority signals...")
    success_count = 0
    for scored in high_priority:
        result = pm.execute_action(scored)[0]
        if result.success:
            success_count += 1

    print(f"    ✓ {success_count}/{len(high_priority)} actions succeeded")

    # Summary by sense
    print("\n" + "=" * 70)
    print("Signal Distribution by Sense")
    print("=" * 70)

    from collections import Counter

    sense_counts = Counter(s.signal.sense_type.value for s in scored_signals)
    for sense, count in sorted(sense_counts.items()):
        print(f"  {sense:12s}: {count:3d} signals")

    print("=" * 70)


if __name__ == "__main__":
    main()
