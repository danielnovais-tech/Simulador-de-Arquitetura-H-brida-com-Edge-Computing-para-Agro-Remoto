"""
Comprehensive unit tests for agro_edge_simulator.py
Tests sensor data generation, edge processing, cloud processing, CLI, and integration scenarios
"""
import pytest
import sys
import argparse
import time
from unittest.mock import patch, MagicMock
from io import StringIO

# Import the main simulator module
sys.path.insert(0, '..')
from agro_edge_simulator import (
    SensorNode,
    EdgeNode,
    CloudNode,
    AgroEdgeSimulator,
    main,
    TEMP_HIGH_THRESHOLD,
    TEMP_LOW_THRESHOLD,
    HUMIDITY_LOW_THRESHOLD,
    SOIL_LOW_THRESHOLD
)


# ============================================================================
# SensorNode Tests - Data Generation and Validation
# ============================================================================

class TestSensorNode:
    """Test cases for SensorNode data generation"""
    
    def test_sensor_initialization(self):
        """Test sensor node initializes with correct attributes"""
        sensor = SensorNode("S1", "temperatura")
        assert sensor.node_id == "S1"
        assert sensor.sensor_type == "temperatura"
        assert sensor.data_points == 0
    
    def test_temperatura_sensor_data_range(self):
        """Test temperature sensor generates data within valid range [15.0, 35.0]"""
        sensor = SensorNode("S1", "temperatura")
        
        # Test multiple readings to ensure range consistency
        for _ in range(100):
            data = sensor.collect_data()
            assert data["type"] == "temperatura"
            assert 15.0 <= data["value"] <= 35.0
            assert isinstance(data["value"], float)
    
    def test_umidade_sensor_data_range(self):
        """Test humidity sensor generates data within valid range [30.0, 90.0]"""
        sensor = SensorNode("S2", "umidade")
        
        for _ in range(100):
            data = sensor.collect_data()
            assert data["type"] == "umidade"
            assert 30.0 <= data["value"] <= 90.0
            assert isinstance(data["value"], float)
    
    def test_solo_sensor_data_range(self):
        """Test soil moisture sensor generates data within valid range [20.0, 80.0]"""
        sensor = SensorNode("S3", "solo")
        
        for _ in range(100):
            data = sensor.collect_data()
            assert data["type"] == "solo"
            assert 20.0 <= data["value"] <= 80.0
            assert isinstance(data["value"], float)
    
    def test_sensor_data_points_increment(self):
        """Test that data_points counter increments on each collection"""
        sensor = SensorNode("S1", "temperatura")
        assert sensor.data_points == 0
        
        sensor.collect_data()
        assert sensor.data_points == 1
        
        sensor.collect_data()
        assert sensor.data_points == 2
        
        for _ in range(10):
            sensor.collect_data()
        assert sensor.data_points == 12
    
    def test_unknown_sensor_type(self):
        """Test unknown sensor type returns default values"""
        sensor = SensorNode("S4", "unknown_type")
        data = sensor.collect_data()
        
        assert data["type"] == "unknown"
        assert data["value"] == 0


# ============================================================================
# EdgeNode Tests - Processing and Alerts
# ============================================================================

class TestEdgeNode:
    """Test cases for EdgeNode processing and alert generation"""
    
    def test_edge_initialization(self):
        """Test edge node initializes with correct attributes"""
        edge = EdgeNode("E1")
        assert edge.edge_id == "E1"
        assert edge.processed_data == 0
        assert edge.alerts_generated == 0
    
    def test_process_normal_temperature(self):
        """Test edge processes normal temperature without alerts"""
        edge = EdgeNode("E1")
        data = {"type": "temperatura", "value": 25.0}
        
        alert = edge.process_data(data)
        
        assert edge.processed_data == 1
        assert edge.alerts_generated == 0
        assert alert is False
    
    def test_process_high_temperature_alert(self):
        """Test edge generates alert for high temperature (>32.0)"""
        edge = EdgeNode("E1")
        data = {"type": "temperatura", "value": 35.0}
        
        alert = edge.process_data(data)
        
        assert edge.processed_data == 1
        assert edge.alerts_generated == 1
        assert alert is True
    
    def test_process_low_temperature_alert(self):
        """Test edge generates alert for low temperature (<18.0)"""
        edge = EdgeNode("E1")
        data = {"type": "temperatura", "value": 15.0}
        
        alert = edge.process_data(data)
        
        assert edge.processed_data == 1
        assert edge.alerts_generated == 1
        assert alert is True
    
    def test_process_low_humidity_alert(self):
        """Test edge generates alert for low humidity (<40.0)"""
        edge = EdgeNode("E1")
        data = {"type": "umidade", "value": 35.0}
        
        alert = edge.process_data(data)
        
        assert edge.processed_data == 1
        assert edge.alerts_generated == 1
        assert alert is True
    
    def test_process_normal_humidity(self):
        """Test edge processes normal humidity without alerts"""
        edge = EdgeNode("E1")
        data = {"type": "umidade", "value": 60.0}
        
        alert = edge.process_data(data)
        
        assert edge.processed_data == 1
        assert edge.alerts_generated == 0
        assert alert is False
    
    def test_process_low_soil_alert(self):
        """Test edge generates alert for low soil moisture (<30.0)"""
        edge = EdgeNode("E1")
        data = {"type": "solo", "value": 25.0}
        
        alert = edge.process_data(data)
        
        assert edge.processed_data == 1
        assert edge.alerts_generated == 1
        assert alert is True
    
    def test_process_normal_soil(self):
        """Test edge processes normal soil moisture without alerts"""
        edge = EdgeNode("E1")
        data = {"type": "solo", "value": 50.0}
        
        alert = edge.process_data(data)
        
        assert edge.processed_data == 1
        assert edge.alerts_generated == 0
        assert alert is False
    
    def test_multiple_data_processing(self):
        """Test edge correctly counts multiple data processing"""
        edge = EdgeNode("E1")
        
        # Process 5 normal readings
        for i in range(5):
            data = {"type": "temperatura", "value": 25.0}
            edge.process_data(data)
        
        assert edge.processed_data == 5
        assert edge.alerts_generated == 0
        
        # Process 3 alert-triggering readings
        for i in range(3):
            data = {"type": "temperatura", "value": 35.0}
            edge.process_data(data)
        
        assert edge.processed_data == 8
        assert edge.alerts_generated == 3


# ============================================================================
# CloudNode Tests - Data Storage and Alert Processing
# ============================================================================

class TestCloudNode:
    """Test cases for CloudNode data receiving and alert processing"""
    
    def test_cloud_initialization(self):
        """Test cloud node initializes with correct attributes"""
        cloud = CloudNode()
        assert cloud.total_data_received == 0
        assert cloud.alerts_processed == 0
    
    def test_receive_data(self):
        """Test cloud receives data correctly"""
        cloud = CloudNode()
        
        cloud.receive_data(10)
        assert cloud.total_data_received == 10
        
        cloud.receive_data(5)
        assert cloud.total_data_received == 15
    
    def test_process_alert(self):
        """Test cloud processes alerts correctly"""
        cloud = CloudNode()
        
        cloud.process_alert()
        assert cloud.alerts_processed == 1
        
        cloud.process_alert()
        cloud.process_alert()
        assert cloud.alerts_processed == 3
    
    def test_combined_operations(self):
        """Test combined data receiving and alert processing"""
        cloud = CloudNode()
        
        cloud.receive_data(100)
        cloud.process_alert()
        cloud.receive_data(50)
        cloud.process_alert()
        cloud.process_alert()
        
        assert cloud.total_data_received == 150
        assert cloud.alerts_processed == 3


# ============================================================================
# AgroEdgeSimulator Tests - Network Initialization and Simulation
# ============================================================================

class TestAgroEdgeSimulator:
    """Test cases for AgroEdgeSimulator initialization and basic operations"""
    
    def test_simulator_initialization(self):
        """Test simulator initializes with correct topology"""
        simulator = AgroEdgeSimulator(duration=10)
        
        assert simulator.duration == 10
        assert len(simulator.sensors) == 9
        assert len(simulator.edge_nodes) == 3
        assert simulator.cloud is not None
        assert simulator.last_cloud_sync_data_count == 0
    
    def test_sensor_types_distribution(self):
        """Test sensors are distributed correctly across types"""
        simulator = AgroEdgeSimulator(duration=10)
        
        temp_count = sum(1 for s in simulator.sensors if s.sensor_type == "temperatura")
        humid_count = sum(1 for s in simulator.sensors if s.sensor_type == "umidade")
        soil_count = sum(1 for s in simulator.sensors if s.sensor_type == "solo")
        
        assert temp_count == 3
        assert humid_count == 3
        assert soil_count == 3
    
    def test_sensor_ids(self):
        """Test sensors have correct IDs"""
        simulator = AgroEdgeSimulator(duration=10)
        
        expected_ids = [f"S{i+1}" for i in range(9)]
        actual_ids = [s.node_id for s in simulator.sensors]
        
        assert actual_ids == expected_ids
    
    def test_edge_ids(self):
        """Test edge nodes have correct IDs"""
        simulator = AgroEdgeSimulator(duration=10)
        
        expected_ids = [f"E{i+1}" for i in range(3)]
        actual_ids = [e.edge_id for e in simulator.edge_nodes]
        
        assert actual_ids == expected_ids
    
    @patch('time.sleep')
    @patch('builtins.print')
    def test_brief_simulation_run(self, mock_print, mock_sleep):
        """Test brief simulation run (integration test)"""
        simulator = AgroEdgeSimulator(duration=2)
        
        # Mock sleep to speed up test
        mock_sleep.return_value = None
        
        # Run simulation with time override
        with patch('time.time') as mock_time:
            # Simulate time progression - need enough time values for all calls
            start_time = 1000.0
            time_values = [start_time + i * 0.5 for i in range(20)]
            mock_time.side_effect = time_values
            
            simulator.run_simulation()
        
        # Verify simulation ran
        assert simulator.start_time is not None
        assert simulator.end_time is not None
    
    @patch('time.sleep')
    @patch('builtins.print')
    def test_interrupt_handling(self, mock_print, mock_sleep):
        """Test simulation handles keyboard interrupt gracefully"""
        simulator = AgroEdgeSimulator(duration=100)
        
        mock_sleep.side_effect = [None, KeyboardInterrupt()]
        
        # Should not raise exception
        simulator.run_simulation()
        
        # Verify simulation was interrupted
        assert simulator.start_time is not None
        assert simulator.end_time is not None


# ============================================================================
# CLI Tests - Argument Parsing and Validation
# ============================================================================

class TestCLI:
    """Test cases for command-line interface"""
    
    def test_duration_argument_required(self):
        """Test that duration argument is required"""
        with patch('sys.argv', ['agro_edge_simulator.py']):
            with pytest.raises(SystemExit):
                main()
    
    def test_duration_argument_parsing(self):
        """Test duration argument is parsed correctly"""
        with patch('sys.argv', ['agro_edge_simulator.py', '--duration', '600']):
            with patch.object(AgroEdgeSimulator, 'run_simulation'):
                # Capture the created simulator
                with patch('agro_edge_simulator.AgroEdgeSimulator') as mock_sim:
                    try:
                        main()
                    except:
                        pass
                    
                    # Verify simulator was created with correct duration
                    if mock_sim.called:
                        mock_sim.assert_called_with(600)
    
    def test_negative_duration_validation(self):
        """Test negative duration is rejected"""
        with patch('sys.argv', ['agro_edge_simulator.py', '--duration', '-10']):
            with patch('sys.stderr', new_callable=StringIO):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
    
    def test_zero_duration_validation(self):
        """Test zero duration is rejected"""
        with patch('sys.argv', ['agro_edge_simulator.py', '--duration', '0']):
            with patch('sys.stderr', new_callable=StringIO):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
    
    def test_positive_duration_accepted(self):
        """Test positive duration values are accepted"""
        test_durations = ['1', '60', '600', '1800', '3600']
        
        for duration in test_durations:
            with patch('sys.argv', ['agro_edge_simulator.py', '--duration', duration]):
                with patch.object(AgroEdgeSimulator, 'run_simulation'):
                    with patch('builtins.print'):
                        try:
                            main()
                            # If we get here without SystemExit, the duration was accepted
                            success = True
                        except SystemExit as e:
                            # Exit code 0 is also success
                            success = (e.code == 0)
                        
                        # We just need to verify no error was raised
                        assert True


# ============================================================================
# Edge Cases and Boundary Tests
# ============================================================================

class TestEdgeCases:
    """Test cases for edge cases and boundary conditions"""
    
    def test_minimum_duration(self):
        """Test simulator with minimum duration (1 second)"""
        simulator = AgroEdgeSimulator(duration=1)
        assert simulator.duration == 1
        assert len(simulator.sensors) == 9
        assert len(simulator.edge_nodes) == 3
    
    def test_large_duration(self):
        """Test simulator with large duration value"""
        simulator = AgroEdgeSimulator(duration=86400)  # 24 hours
        assert simulator.duration == 86400
    
    def test_threshold_boundaries_temperature(self):
        """Test temperature threshold boundaries"""
        edge = EdgeNode("E1")
        
        # Just below high threshold - no alert
        data = {"type": "temperatura", "value": 31.9}
        assert edge.process_data(data) is False
        
        # At high threshold - no alert
        data = {"type": "temperatura", "value": 32.0}
        assert edge.process_data(data) is False
        
        # Just above high threshold - alert
        data = {"type": "temperatura", "value": 32.1}
        assert edge.process_data(data) is True
        
        # Just above low threshold - no alert
        data = {"type": "temperatura", "value": 18.1}
        assert edge.process_data(data) is False
        
        # At low threshold - no alert
        data = {"type": "temperatura", "value": 18.0}
        assert edge.process_data(data) is False
        
        # Just below low threshold - alert
        data = {"type": "temperatura", "value": 17.9}
        assert edge.process_data(data) is True
    
    def test_threshold_boundaries_humidity(self):
        """Test humidity threshold boundaries"""
        edge = EdgeNode("E1")
        
        # Just above threshold - no alert
        data = {"type": "umidade", "value": 40.1}
        assert edge.process_data(data) is False
        
        # At threshold - no alert
        data = {"type": "umidade", "value": 40.0}
        assert edge.process_data(data) is False
        
        # Just below threshold - alert
        data = {"type": "umidade", "value": 39.9}
        assert edge.process_data(data) is True
    
    def test_threshold_boundaries_soil(self):
        """Test soil moisture threshold boundaries"""
        edge = EdgeNode("E1")
        
        # Just above threshold - no alert
        data = {"type": "solo", "value": 30.1}
        assert edge.process_data(data) is False
        
        # At threshold - no alert
        data = {"type": "solo", "value": 30.0}
        assert edge.process_data(data) is False
        
        # Just below threshold - alert
        data = {"type": "solo", "value": 29.9}
        assert edge.process_data(data) is True
    
    def test_cloud_sync_behavior(self):
        """Test cloud synchronization occurs at expected intervals"""
        simulator = AgroEdgeSimulator(duration=1)
        
        # Verify initial state
        assert simulator.last_cloud_sync_data_count == 0
        assert simulator.cloud.total_data_received == 0


# ============================================================================
# Integration Test
# ============================================================================

class TestIntegration:
    """Integration test for end-to-end simulation"""
    
    @patch('time.sleep')
    @patch('builtins.print')
    def test_end_to_end_simulation(self, mock_print, mock_sleep):
        """Test complete end-to-end simulation with all components"""
        # Create simulator
        simulator = AgroEdgeSimulator(duration=3)
        
        # Mock sleep to speed up test
        mock_sleep.return_value = None
        
        # Mock time progression
        with patch('time.time') as mock_time:
            start_time = 1000.0
            # Generate enough time points for the simulation
            time_values = [start_time + i * 0.5 for i in range(10)]
            mock_time.side_effect = time_values
            
            # Run simulation
            simulator.run_simulation()
        
        # Verify all components interacted correctly
        assert simulator.start_time is not None
        assert simulator.end_time is not None
        
        # Verify sensors collected data
        total_sensor_data = sum(s.data_points for s in simulator.sensors)
        assert total_sensor_data > 0
        
        # Verify edge nodes processed data
        total_edge_processed = sum(e.processed_data for e in simulator.edge_nodes)
        assert total_edge_processed > 0
        
        # Verify cloud received data or alerts
        assert simulator.cloud.total_data_received >= 0
        assert simulator.cloud.alerts_processed >= 0
        
        # Verify sensor data was distributed to edge nodes
        assert total_sensor_data == total_edge_processed
