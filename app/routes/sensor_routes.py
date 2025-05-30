from flask import Blueprint, request, jsonify
from app.services.db_services import get_sensors, save_sensors, check_threshold, save_log_per_hour


bp = Blueprint('sensor', __name__, url_prefix='/aquarium/')

@bp.route('<aquarium_id>/sensor', methods=['POST'])
def sensor_post(aquarium_id):
    data = request.json
    print(data)

    ph = data.get('ph')
    temp = data.get('temperature')
    turbidity = data.get('turbidity')

    sensor_data = {
        "ph": ph,
        "temperature": temp,
        "turbidity": turbidity
    }

    save_sensors(aquarium_id, sensor_data)
    check_threshold(aquarium_id, sensor_data)


    return jsonify({"message": "Sensor data received and saved"}), 200

@bp.route('<aquarium_id>/log_per_hour', methods=['POST'])
def log_per_hour(aquarium_id):
    data = request.json
    save_log_per_hour(aquarium_id, data)

    return jsonify({"message": "Log per hour data received and saved"}), 200


