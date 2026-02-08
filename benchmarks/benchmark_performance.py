"""
Performance Benchmarks for REAPER

Measures performance of optimized code paths.
Run with: python benchmarks/benchmark_performance.py
"""

import time
from datetime import datetime

from pipeline.action import ActionPlugin
from pipeline.hearing import HearingPlugin
from pipeline.scoring import ScoringPlugin
from pipeline.sight import SightPlugin
from pipeline.smell import SmellPlugin
from pipeline.taste import TastePlugin
from pipeline.touch import TouchPlugin
from reaper import PluginManager, SenseType, Signal


def benchmark_detection(num_iterations=1000):
    """Benchmark signal detection performance."""
    pm = PluginManager()
    pm.register_plugin(SightPlugin())

    start = time.perf_counter()
    for _ in range(num_iterations):
        signals = pm.detect_sight(source="benchmark-source")
    end = time.perf_counter()

    elapsed = end - start
    throughput = num_iterations / elapsed

    print(f"\n📊 Detection Benchmark:")
    print(f"   Iterations: {num_iterations:,}")
    print(f"   Time: {elapsed:.3f}s")
    print(f"   Throughput: {throughput:.0f} ops/sec")


def benchmark_full_pipeline(num_iterations=100):
    """Benchmark complete pipeline processing."""
    pm = PluginManager()
    pm.register_plugin(SightPlugin())
    pm.register_plugin(ScoringPlugin())
    pm.register_plugin(ActionPlugin())

    start = time.perf_counter()
    for _ in range(num_iterations):
        # Detect
        signals = pm.detect_sight(source="benchmark")
        # Score
        for signal in signals:
            scored = pm.score_signal(signal)
            # Act
            if scored:
                pm.execute_action(scored[0])
    end = time.perf_counter()

    elapsed = end - start
    throughput = num_iterations / elapsed

    print(f"\n📊 Full Pipeline Benchmark:")
    print(f"   Iterations: {num_iterations:,}")
    print(f"   Time: {elapsed:.3f}s")
    print(f"   Throughput: {throughput:.0f} ops/sec")


def benchmark_batch_creation(num_signals=1000):
    """Benchmark batch signal creation vs individual creation."""
    # Individual creation
    start = time.perf_counter()
    for i in range(num_signals):
        Signal(sense_type=SenseType.SIGHT, source=f"source-{i}")
    individual_time = time.perf_counter() - start

    # Batch creation
    signals_data = [
        {"sense_type": SenseType.SIGHT, "source": f"source-{i}"} for i in range(num_signals)
    ]
    start = time.perf_counter()
    Signal.create_batch(signals_data)
    batch_time = time.perf_counter() - start

    improvement = ((individual_time - batch_time) / individual_time) * 100

    print(f"\n📊 Batch Creation Benchmark:")
    print(f"   Signals: {num_signals:,}")
    print(f"   Individual: {individual_time:.4f}s")
    print(f"   Batch: {batch_time:.4f}s")
    print(f"   Improvement: {improvement:.1f}%")


def benchmark_plugin_count(num_iterations=100000):
    """Benchmark plugin_count vs len(list_plugins())."""
    pm = PluginManager()
    pm.register_plugin(SightPlugin())
    pm.register_plugin(HearingPlugin())
    pm.register_plugin(TouchPlugin())
    pm.register_plugin(TastePlugin())
    pm.register_plugin(SmellPlugin())

    # Using plugin_count()
    start = time.perf_counter()
    for _ in range(num_iterations):
        count = pm.plugin_count()
    count_time = time.perf_counter() - start

    # Using len(list_plugins())
    start = time.perf_counter()
    for _ in range(num_iterations):
        count = len(pm.list_plugins())
    list_time = time.perf_counter() - start

    improvement = ((list_time - count_time) / list_time) * 100

    print(f"\n📊 Plugin Count Benchmark:")
    print(f"   Iterations: {num_iterations:,}")
    print(f"   plugin_count(): {count_time:.4f}s")
    print(f"   len(list_plugins()): {list_time:.4f}s")
    print(f"   Improvement: {improvement:.1f}%")


def benchmark_multi_sense_detection(num_iterations=100):
    """Benchmark detection across all five senses."""
    pm = PluginManager()
    pm.register_plugin(SightPlugin())
    pm.register_plugin(HearingPlugin())
    pm.register_plugin(TouchPlugin())
    pm.register_plugin(TastePlugin())
    pm.register_plugin(SmellPlugin())

    start = time.perf_counter()
    for _ in range(num_iterations):
        pm.detect_sight(source="test")
        pm.detect_hearing(source="test")
        pm.detect_touch(source="test")
        pm.detect_taste(source="test")
        pm.detect_smell(source="test")
    end = time.perf_counter()

    elapsed = end - start
    throughput = (num_iterations * 5) / elapsed  # 5 senses per iteration

    print(f"\n📊 Multi-Sense Detection Benchmark:")
    print(f"   Iterations: {num_iterations:,} (x5 senses)")
    print(f"   Time: {elapsed:.3f}s")
    print(f"   Throughput: {throughput:.0f} detections/sec")


def main():
    """Run all performance benchmarks."""
    print("=" * 60)
    print("REAPER Performance Benchmarks")
    print("=" * 60)
    print("\nRunning benchmarks... (this may take a minute)\n")

    benchmark_detection(num_iterations=1000)
    benchmark_full_pipeline(num_iterations=100)
    benchmark_batch_creation(num_signals=1000)
    benchmark_plugin_count(num_iterations=100000)
    benchmark_multi_sense_detection(num_iterations=100)

    print("\n" + "=" * 60)
    print("✅ All benchmarks complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
