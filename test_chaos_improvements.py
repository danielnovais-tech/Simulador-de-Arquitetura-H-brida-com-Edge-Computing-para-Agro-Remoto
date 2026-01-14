#!/usr/bin/env python3
"""
Test chaos engineering improvements
"""
import time
from unittest.mock import patch, MagicMock
from io import StringIO

from simulador_agro_edge import AgroEdgeSimulator, LinkStatus, NodeRole


def test_link_failure_recovery():
    """Test link_failure chaos test with active recovery monitoring"""
    print("Testing link_failure chaos test...")
    
    simulator = AgroEdgeSimulator("Test Farm")
    
    # Track that simulate_sd_wan_orchestration is called
    original_orchestration = simulator.simulate_sd_wan_orchestration
    call_count = [0]
    
    def mock_orchestration():
        call_count[0] += 1
        # Force failover to happen
        if simulator.network_links['starlink'].status == LinkStatus.OFFLINE:
            if simulator.network_links['4g_backup'].status == LinkStatus.ONLINE:
                simulator.sd_wan_policy = "4g_failover"
    
    simulator.simulate_sd_wan_orchestration = mock_orchestration
    
    # Mock time.sleep to speed up test
    with patch('time.sleep'):
        result = simulator.run_chaos_test("link_failure")
    
    assert call_count[0] > 0, "simulate_sd_wan_orchestration should be called during recovery"
    print(f"  ✅ link_failure test called simulate_sd_wan_orchestration {call_count[0]} times")
    print("  ✅ Recovery monitoring is active (orchestration invoked in recovery loop)")


def test_node_failure_recovery():
    """Test node_failure chaos test with active recovery monitoring"""
    print("\nTesting node_failure chaos test...")
    
    simulator = AgroEdgeSimulator("Test Farm")
    
    # Track that simulate_edge_heartbeat is called
    original_heartbeat = simulator.simulate_edge_heartbeat
    call_count = [0]
    
    def mock_heartbeat():
        call_count[0] += 1
        # Don't interfere with actual heartbeat logic
    
    simulator.simulate_edge_heartbeat = mock_heartbeat
    
    # Mock time.sleep to speed up test
    with patch('time.sleep'):
        result = simulator.run_chaos_test("node_failure")
    
    assert call_count[0] > 0, "simulate_edge_heartbeat should be called during recovery"
    print(f"  ✅ node_failure test called simulate_edge_heartbeat {call_count[0]} times")
    print("  ✅ Recovery monitoring is active (heartbeat invoked in recovery loop)")


def test_traffic_spike_immediate_completion():
    """Test traffic_spike completes immediately without recovery loop"""
    print("\nTesting traffic_spike immediate completion...")
    
    simulator = AgroEdgeSimulator("Test Farm")
    
    # Track if time.sleep is called (it shouldn't be for traffic_spike)
    sleep_called = [False]
    
    def mock_sleep(duration):
        sleep_called[0] = True
    
    with patch('time.sleep', mock_sleep):
        start_time = time.time()
        result = simulator.run_chaos_test("traffic_spike")
        elapsed = time.time() - start_time
    
    assert result is True, "traffic_spike should return True"
    assert not sleep_called[0], "traffic_spike should NOT call time.sleep (no recovery loop)"
    assert elapsed < 1.0, f"Should complete immediately, took {elapsed}s"
    print("  ✅ traffic_spike completed immediately without recovery loop")
    print(f"  ✅ Completed in {elapsed:.3f}s (no sleep calls)")


if __name__ == "__main__":
    print("="*60)
    print("TESTING CHAOS TEST IMPROVEMENTS")
    print("="*60 + "\n")
    
    try:
        test_link_failure_recovery()
        test_node_failure_recovery()
        test_traffic_spike_immediate_completion()
        
        print("\n" + "="*60)
        print("✅ ALL CHAOS TEST IMPROVEMENTS VERIFIED!")
        print("="*60)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
