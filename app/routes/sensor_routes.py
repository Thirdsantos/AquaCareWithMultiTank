from flask import Blueprint, request, jsonify


bp = Blueprint('sensor', __name__, url_prefix='/aquarium/')

@bp.route('<aquarium_id>/sensor', methods=['POST'])
def sensor_post(aquarium_id):
    data = request.json
    print(data)

    ph = data.get('ph')
    temp = data.get('temp')
    turbidity = data.get('turbidity')

    sensor_data = {
        "ph": ph,
        "temperature": temp,
        "turbidity": turbidity
    }


    return jsonify({"message": "Sensor data received and saved"}), 200
