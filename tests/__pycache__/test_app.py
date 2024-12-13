import unittest
from app import app

class SensorApiTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup for the entire test class."""
        cls.app = app.test_client()
        cls.app.testing = True
    
    def setUp(self):
        """Setup for each test."""
        # You can add any setup required before each test here, like resetting the database

    def tearDown(self):
        """Tear down for each test."""
        # You can add cleanup steps here, like deleting test data from the database

    def test_create_sensor(self):
        """Test POST /api/sensors"""
        new_sensor = {
            "type": "Temperature",
            "location": "Field A",
            "lastReading": {
                "temperature": 25.5,
                "humidity": 45.2,
                "soilMoisture": 40.5,
                "lightIntensity": 300
            },
            "status": "active"
        }
        response = self.app.post('/api/sensors', json=new_sensor)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)  # Ensure the sensor ID is included
        self.assertEqual(response.json['type'], 'Temperature')

    def test_get_sensors(self):
        """Test GET /api/sensors"""
        response = self.app.get('/api/sensors')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)  # Ensure it returns a list

    def test_get_sensor_by_id(self):
        """Test GET /api/sensors/{id}"""
        # Assuming the sensor with ID 1 exists, adjust based on your API
        response = self.app.get('/api/sensors/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)

    def test_get_sensor_not_found(self):
        """Test GET /api/sensors/{id} when sensor is not found"""
        response = self.app.get('/api/sensors/9999')  # Non-existent ID
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json.get('error'), 'Sensor not found')

    def test_update_sensor(self):
        """Test PUT /api/sensors/{id}"""
        updated_data = {
            "type": "Humidity",
            "location": "Field B",
            "status": "inactive"
        }
        response = self.app.put('/api/sensors/1', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['location'], 'Field B')

    def test_delete_sensor(self):
        """Test DELETE /api/sensors/{id}"""
        # Assuming the sensor with ID 1 exists, adjust based on your API
        response = self.app.delete('/api/sensors/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Sensor deleted')

        # Ensure the sensor is deleted
        response = self.app.get('/api/sensors/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
