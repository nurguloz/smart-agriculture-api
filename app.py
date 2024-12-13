from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database to store sensor data (can be replaced with a real database later)
sensors = [
    {"id": 1, "type": "Temperature", "location": "Field A", "status": "active"},
    {"id": 2, "type": "Moisture", "location": "Field B", "status": "active"},
]

# Routes

# Home route (Ensure this is included)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Smart Agriculture API!"}), 200

# 1. Get all sensors
@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    return jsonify(sensors), 200

# 2. Get a specific sensor by ID
@app.route('/api/sensors/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    sensor = next((s for s in sensors if s["id"] == sensor_id), None)
    if sensor:
        return jsonify(sensor), 200
    return jsonify({"error": "Sensor not found"}), 404

# 3. Add a new sensor
@app.route('/api/sensors', methods=['POST'])
def add_sensor():
    # Check if the request contains valid JSON
    if not request.is_json:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    new_sensor = request.json
    # Ensure all required fields are in the request
    if "type" not in new_sensor or "location" not in new_sensor or "status" not in new_sensor:
        return jsonify({"error": "Missing required fields"}), 400
    
    new_sensor["id"] = max(s["id"] for s in sensors) + 1 if sensors else 1
    sensors.append(new_sensor)
    return jsonify(new_sensor), 201

# 4. Update an existing sensor
@app.route('/api/sensors/<int:sensor_id>', methods=['PUT'])
def update_sensor(sensor_id):
    sensor = next((s for s in sensors if s["id"] == sensor_id), None)
    if sensor:
        sensor_data = request.json
        # Update only the fields provided in the request
        if "type" in sensor_data: sensor["type"] = sensor_data["type"]
        if "location" in sensor_data: sensor["location"] = sensor_data["location"]
        if "status" in sensor_data: sensor["status"] = sensor_data["status"]
        return jsonify(sensor), 200
    return jsonify({"error": "Sensor not found"}), 404

# 5. Delete a sensor
@app.route('/api/sensors/<int:sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    global sensors
    sensors = [s for s in sensors if s["id"] != sensor_id]
    return jsonify({"message": "Sensor deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)

