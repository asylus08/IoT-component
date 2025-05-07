from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from HardwareController import HardwareController
from ActionType import ActionType
from firedatabase import Database
import threading
import time


app = Flask(__name__)
CORS(app)
iot_device = HardwareController()
db = Database()

def check_temperature() -> None:
    while True:
        iot_device.check_temperature()
        temp = iot_device.current_temp
        db.write_local_data(temp, iot_device.is_test_mode)
        db.write_cloud_data(temp, iot_device.is_test_mode)
        time.sleep(15)

@app.route('/test-connection', methods=['GET'])
def test_connection():
    data = {'success': True}, 200
    return jsonify(data)


@app.route('/actions/door', methods=['POST'])
def handle_door_action():
    action_data = request.get_json()
    action_str = action_data.get('action')
    data = {}

    action = ActionType.convert_str_action_to_enum(action_str)
    if not action:
        data = {'error': 'Invalid action type'}, 400

    match action:
        case ActionType.OPEN_DOOR:
            iot_device.open_door()
            data = {'success': True, 'message': 'Successfully opened door', 'is_door_open': iot_device.is_door_open}, 200

        case ActionType.CLOSE_DOOR:
            iot_device.close_door()
            data = {'success': True, 'message': 'Successfully closed door', 'is_door_open': iot_device.is_door_open}, 200

        case _:
            data = {'success': False, 'error': 'Invalid action type'}, 400

    return jsonify(data)


@app.route('/actions/temperature', methods=['POST'])
def handle_led_action():
    action_data = request.get_json()
    action_str = action_data.get('action')
    data = {}

    action = ActionType.convert_str_action_to_enum(action_str)
    if not action:
        data = {'error': 'Invalid action type'}, 400

    match action:
        case ActionType.RISE_TEMP:
            iot_device.increase_temp()
            temp = iot_device.current_temp
            db.write_local_data(temp, iot_device.is_test_mode)
            db.write_cloud_data(temp, iot_device.is_test_mode)
            data = {'success': True, 'message': 'Successfully activated the led', 'temp': iot_device.current_temp}, 200

        case ActionType.LOWER_TEMP:
            iot_device.decrease_temp()
            temp = iot_device.current_temp
            db.write_local_data(temp, iot_device.is_test_mode)
            db.write_cloud_data(temp, iot_device.is_test_mode)
            data = {'success': True, 'message': 'Successfully deactivated the led', 'temp': iot_device.current_temp}, 200

        case _:
            data = {'success': False, 'error': 'Invalid action type'}, 400

    return jsonify(data)


@app.route('/actions/alarm', methods=['POST'])
#@cross_origin()
def handle_alarm_action():
    action_data = request.get_json()
    action_str = action_data.get('action')
    data = {}

    action = ActionType.convert_str_action_to_enum(action_str)
    if not action:
        data = {'error': 'Invalid action type'}, 400

    match action:
        case ActionType.ACTIVATE_ALARM:
            iot_device.activate_alarm()
            data = {'success': True, 'message': 'Successfully activated the alarm'}, 200

        case ActionType.DEACTIVATE_ALARM:
            iot_device.deactivate_alarm()
            data = {'success': True, 'message': 'Successfully deactivated the alarm'}, 200

        case _:
            data = {'success': False, 'error': 'Invalid action type'}, 400

    return jsonify(data)


@app.route('/settings/test-mode', methods=['POST'])
def handle_test_mode_action():
    data = {}

    if iot_device.is_test_mode:
        iot_device.deactivate_test_mode()
    else:
        iot_device.activate_test_mode()

    data = {'success': True, 'message': f"Test mode is now: {iot_device.is_test_mode}", 'test_mode' : iot_device.is_test_mode}, 200

    return jsonify(data)


if __name__ == '__main__':
    iot_thread = threading.Thread(target=check_temperature)
    iot_thread.daemon = True
    iot_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=False)