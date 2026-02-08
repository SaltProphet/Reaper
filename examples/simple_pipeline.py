"""
Simple Pipeline Example

This example demonstrates the basic REAPER pipeline:
1. Detection - Detect signals from a source
2. Scoring - Evaluate signal priority
3. Action - Execute actions on high-priority signals

Run from repository root:
    python examples/simple_pipeline.py
"""

from reaper import PluginManager
from pipeline.sight import SightPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.action import ActionPlugin


def main():
    print("=" * 60)
    print("REAPER Simple Pipeline Example")
    print("=" * 60)
    
    # Step 1: Initialize Plugin Manager
    print("\n[1] Initializing Plugin Manager...")
    pm = PluginManager()
    
    # Step 2: Register Plugins
    print("[2] Registering plugins...")
    pm.register_plugin(SightPlugin(), name="sight")
    pm.register_plugin(ScoringPlugin(), name="scoring")
    pm.register_plugin(ActionPlugin(), name="action")
    print("    ✓ Sight plugin registered")
    print("    ✓ Scoring plugin registered")
    print("    ✓ Action plugin registered")
    
    # Step 3: Detect Signals
    print("\n[3] Detecting signals from source...")
    source = "example-visual-feed"
    signals = pm.detect_sight(source=source)
    print(f"    ✓ Detected {len(signals)} signals from '{source}'")
    
    if not signals:
        print("    ⚠ No signals detected. Exiting.")
        return
    
    # Step 4: Score Signals
    print("\n[4] Scoring signals...")
    scored_signals = []
    for i, signal in enumerate(signals):
        scored = pm.score_signal(signal)[0]
        scored_signals.append(scored)
        print(f"    Signal {i+1}: score={scored.score:.2f}, tags={scored.tags}")
    
    # Step 5: Filter High-Priority Signals
    print("\n[5] Filtering high-priority signals...")
    threshold = 0.5
    high_priority = [s for s in scored_signals if s.score >= threshold]
    print(f"    ✓ {len(high_priority)}/{len(scored_signals)} signals above threshold {threshold}")
    
    if not high_priority:
        print("    ⚠ No high-priority signals. Exiting.")
        return
    
    # Step 6: Execute Actions
    print("\n[6] Executing actions on high-priority signals...")
    success_count = 0
    for i, scored_signal in enumerate(high_priority):
        result = pm.execute_action(scored_signal)[0]
        if result.success:
            success_count += 1
            print(f"    ✓ Action {i+1}: {result.action_type} - {result.details}")
        else:
            print(f"    ✗ Action {i+1} failed: {result.details}")
    
    # Step 7: Summary
    print("\n" + "=" * 60)
    print("Pipeline Summary")
    print("=" * 60)
    print(f"Total signals detected:    {len(signals)}")
    print(f"High-priority signals:     {len(high_priority)}")
    print(f"Successful actions:        {success_count}")
    print(f"Failed actions:            {len(high_priority) - success_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
