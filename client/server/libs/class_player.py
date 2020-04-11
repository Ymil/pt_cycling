from libs.class_remoteServerController import remoteServerController
from libs.class_serialControl import serialControl
from threading import Thread
from datetime import datetime
import random
import json

class Player(remoteServerController):
    def __init__(self, settings_file="user_config.json"):
        self._master = False
        self._status = 0
        self.server = ''
        self._t_update_data = None
        self.settings_file = settings_file
        self._serial_control = None
        self._game_id = None
        self._settings = {}
        self.get_settings()
        self._reset()
    
    def _reset(self):
        if(not self._t_update_data == None):
            self.stop()
        if(self._status == 1):
            self._serial_control.stop()
        self._distance = 0.0
        self._speed = 0.0
        self._speed_prom = 0.0
        self._speed_max = 0.0
        self._status = 0
    
    def set_game_id(self, game_id):
        self._game_id = game_id
    
    def get_game_id(self):
        return self._game_id
    
    def remote_add_data(self):
        #/add_data_player/{game_id}/{player_name}/{player_datatime_sync}/{player_distance}/{player_speed_max}/{player_speed_prom}
        self.put('add_data_player/{}/{}/{}/{}/{}/{}/{}'.format(
            self.get_game_id(), self.get_name(), str(datetime.now()),
            self._distance, self._speed, self._speed_prom, self._speed_max))
    
    def configure(self):
        if(self._status == 1):
            self._reset()
        if self._serial_control == None:
            self._serial_control = serialControl(self._settings['serial_port'], self._settings['bike_shot'])     
    
    def start(self):    
        self._serial_control.start()
        self._status = 1       
        #self.update_data()
    
    def stop(self):        
        #self._t_update_data.cancel()
        self._status = 0
        self._serial_control.stop()
        
    def set_master(self):
        self._master = True
        
    def get_name(self):
        return self._settings['player_name']
    
    def get_data(self):     
        if self._status:
            if(not self._game_id == None or not self._game_id == 0):
                Thread(target=self.remote_add_data).start()
            data = self._serial_control.get_data()
            self._distance = data[0]
            self._speed = data[1]
            self._speed_prom = data[2]
            self._speed_max = data[3]
        return {
             'player_name': self.get_name(), 'player_distance': self._distance,
             'player_speed': self._speed, 'player_speed_prom': self._speed_prom, 
             'player_speed_max': self._speed_max
        }
    
    def update_data(self):
        print('Updating data')
        
        self._t_update_data = Timer(0.5, self.update_data)
        self._t_update_data.start()
    
    def get_server(self):
        return self.server
        
    
    def get_settings(self):
        self._settings = json.load(open(self.settings_file))
        self.server = self._settings['ip_server']
        return self._settings
    
    def set_settings(self, data):
        with open(self.settings_file, 'w') as outf:
            json.dump(data, outf)
        self.get_settings()