from flask import Flask, jsonify, request
from flask_cors import CORS
from HardwareController import HardwareController
from ActionType import ActionType
import threading
import time


app = Flask(__name__)
CORS(app)
iot_device = HardwareController()

def check_temperature() -> None:
    while True:
        iot_device.check_temperature()
        time.sleep(10)


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
            data = {'success': True, 'message': 'Successfully opened door'}, 200

        case ActionType.CLOSE_DOOR:
            iot_device.close_door()
            data = {'success': True, 'message': 'Successfully closed door'}, 200

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
            iot_device.open_door()
            data = {'success': True, 'message': 'Successfully activated the led'}, 200

        case ActionType.LOWER_TEMP:
            iot_device.close_door()
            data = {'success': True, 'message': 'Successfully deactivated the led'}, 200

        case _:
            data = {'success': False, 'error': 'Invalid action type'}, 400

    return jsonify(data)


@app.route('/actions/alarm', methods=['POST'])
def handle_alarm_action(action: ActionType):
    action_data = request.get_json()
    action_str = action_data.get('action')
    data = {}

    action = ActionType.convert_str_action_to_enum(action_str)
    if not action:
        data = {'error': 'Invalid action type'}, 400

    match action:
        case ActionType.ACTIVATE_ALARM:
            iot_device.open_door()
            data = {'success': True, 'message': 'Successfully activated the alarm'}, 200

        case ActionType.DEACTIVATE_ALARM:
            iot_device.close_door()
            data = {'success': True, 'message': 'Successfully deactivated the alarm'}, 200

        case _:
            data = {'success': False, 'error': 'Invalid action type'}, 400

    return jsonify(data)


@app.route('/settings/test-mode', methods=['POST'])
def handle_test_mode_action():
    action_data = request.get_json()
    test_mode = action_data.get('test_value')
    data = {}

    if test_mode not in [True, False]:
        data = {'error': 'Invalid test mode value'}, 400

    # Change test mode value here

    data = {'success': True, 'message': f"Test mode is now: {test_mode}"}, 200

    return jsonify(data)


if __name__ == '__main__':
    iot_thread = threading.Thread(target=check_temperature)
    iot_thread.daemon = True
    iot_thread.start()

    app.run(host='10.166.30.126', port=5000, debug=True)