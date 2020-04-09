from flask import Flask
from flask import render_template, json, jsonify, send_file, request
from libs.class_player import Player
from libs.class_game import Game
import os
from flask.helpers import make_response
app = Flask(__name__, root_path='../cli')

player = Player()
game = Game(player)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<path:template>.html')
def send_template(template):
    #Fix AngularJS
    template_file = '{}.html'.format(os.path.join('templates',template))
    return send_file(template_file)

@app.route('/get_settings')
def get_settings():
    return jsonify(player.get_settings())

@app.route('/set_settings', methods=["PUT"])
def set_settings():
    if request.method == "PUT":
        player.set_settings(request.json)
        return make_response('', 201)
    return make_response('', 400)

@app.route('/create_game', methods=['PUT'])
def create_game():
    data = request.json
    if(game.create(data)):        
        return jsonify(game.get_serializate_data())
    return make_response('', 400)


@app.route('/join_game/<int:game_id>')
def join_game(game_id):
    response = game.join_player(game_id)
    return jsonify(response)
    

@app.route('/status_game')
def get_status_game():
    status = game.get_status_game()
    return jsonify(status)
    

@app.route('/start_game')
def start_game():
    if(game.start()):
        return make_response('', 201)
    return make_response('', 400)

@app.route('/start_game_player')
def start_game_player():
    if(game.start_player()):
        return make_response('', 201)
    return make_response('', 400)

@app.route('/end_game_player')
def end_game_player():
    if(game.end_player()):
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