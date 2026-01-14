# Sample Agriculture Sensor Dataset

This directory contains sample datasets for testing and validation.

## Dataset Structure

### Sensor Readings Format

```json
{
  "timestamp": 1703857200.0,
  "location": {
    "latitude": -15.7801,
    "longitude": -47.9292,
    "zone_id": "zone_1"
  },
  "soil_moisture": 65.3,
  "soil_temperature": 23.5,
  "air_temperature": 28.2,
  "humidity": 72.1,
  "light_intensity": 45000.0,
  "ph_level": 6.5,
  "nitrogen_level": 150.2,
  "phosphorus_level": 28.9,
  "potassium_level": 205.7
}
```

### Crop Data Format

```json
{
  "crop_type": "corn",
  "growth_stage": "harvest_ready",
  "planting_date": 1693857200.0,
  "expected_harvest_date": 1704057200.0,
  "health_score": 92.5,
  "yield_estimate": 9500.0
}
```

## Generating Sample Data

Use the data generator to create realistic datasets:

```python
from agro.data_generator import AgroDataGenerator, CropType

gen = AgroDataGenerator(seed=42)

# Generate sensor readings
location = gen.locations[0]
reading = gen.generate_sensor_reading(location)

# Generate crop data
crop = gen.generate_crop_data(CropType.CORN, days_since_planting=115)
```

## Dataset Characteristics

### Sensor Ranges

- **Soil Moisture**: 20-90% (optimal: 50-70%)
- **Temperature**: 5-45°C (optimal: 20-30°C)
- **Humidity**: 30-95% (optimal: 60-80%)
- **Light**: 0-80,000 lux (varies by time of day)
- **pH**: 5.5-7.5 (optimal: 6.0-7.0)
- **Nitrogen**: 100-200 mg/kg
- **Phosphorus**: 20-40 mg/kg
- **Potassium**: 150-250 mg/kg

### Temporal Patterns

- **Daily Cycle**: Temperature and light vary by hour
- **Weekly Cycle**: Irrigation affects soil moisture
- **Seasonal**: Growth stages progress over months

### Realistic Variations

- Random noise (±5%)
- Weather events (±20%)
- Equipment calibration drift (±2%)

## Use Cases

1. **System Testing**: Validate data pipeline
2. **Algorithm Training**: ML model development
3. **Performance Testing**: Load testing with realistic data
4. **Visualization**: Dashboard development
5. **Documentation**: Example data for guides

## Data Quality

All generated data passes validation:
- Value ranges checked
- Type consistency verified
- Timestamp validity confirmed
- Correlation patterns maintained
