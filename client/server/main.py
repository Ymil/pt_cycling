from flask import Flask
from flask import render_template, json, jsonify, send_file, request
import os
from flask.helpers import make_response
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<path:template>.html')
def send_template(template):
    template_file = '{}.html'.format(os.path.join('templates',template))
    return send_file(template_file)

@app.route('/get_settings')
def get_user_config():
    return jsonify(json.load(open('user_config.json')))

@app.route('/set_settings', methods=["PUT"])
def set_settings():
    if request.method == "PUT":
        with open('user_config.json', 'w') as outf:
            json.dump(request.json, outf)
        return make_response('', 201)
    return make_response('', 400)

@app.route('/create_game', methods=['PUT'])
def create_game():
    data = request.json
    if(data['number_of_players'] == '1'):
        response = {
            'id': 0, 
            'number_of_players': 1, 
            'players':{
                    '1':{
                        'player_name': 'player',
                        'speed': 0,
                        'speed_max': 0,
                        'distance': 0
                        }
                }
            }
        return jsonify(response)
    return make_response('', 400)

sim_game_status = 2
@app.route('/status_game/<int:game_id>')
def get_status_game(game_id):
    global sim_game_status
    if(game_id == 0):
        response = {
            'status': sim_game_status,             
            'players':{
                    '1':{
                        'player_name': 'player',
                        'speed': 0,
                        'speed_max': 0,
                        'distance': 0
                        }
                }
            }
        sim_game_status = 2
        return jsonify(response)
    return make_response('', 400)

@app.route('/start_game/<int:game_id>')
def start_game(game_id):
    global sim_game_status
    if(game_id == 0):
        sim_game_status = 4
        return make_response('', 201)
    return make_response('', 400)

@app.route('/get_serial_ports')
def get_setting_serial_ports():
    import serial.tools.list_ports
    ports = []
    for port in list(serial.tools.list_ports.comports()):
        ports.append(str(port).split(" ")[0])
    return jsonify(ports)

if __name__ == "__main__":
    app.run()