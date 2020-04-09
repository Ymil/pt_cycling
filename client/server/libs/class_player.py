from libs.class_serialControl import serialControl
from threading import Timer
import random
import json

class Player():
    __settings_file__ = 'user_config.json'
    def __init__(self):
        self._master = False
        self._status = 0
        self._t_update_data = None
        self._reset()
        self._serial_control = None
        
        self._settings = {}
        self.get_settings()
    
    def _reset(self):
        if(not self._t_update_data == None):
            self.stop()
        self._distance = 0.0
        self._speed = 0.0
        self._speed_max = 0.0
    

    def run(self):
        
        self._serial_control = serialControl(self._settings['serial_port'], self._settings['bike_shot'])        
        self._serial_control.start()
        self._reset()
        self._status = 1       
        #self.update_data()
    
    def stop(self):        
        #self._t_update_data.cancel()
        self._status = 0
        self._serial_control.stop()
        del self._serial_control
        
    def set_master(self):
        self._master = True
        
    def get_name(self):
        return self._settings['player_name']
    
    def get_data(self):
        print('Get data')
        if self._status:
            data = self._serial_control.get_data()
            self._distance += data[0]
            self._speed = data[1]
            self._speed_max = data[3]
        return {
             'player_name': self.get_name(), 'player_distance': self._distance,
             'player_speed_prom': self._speed, 'player_speed_max': self._speed_max
        }
    
    def update_data(self):
        print('Updating data')
        
        self._t_update_data = Timer(0.5, self.update_data)
        self._t_update_data.start()
    
    def get_settings(self):
        self._settings = json.load(open(self.__settings_file__))
        return self._settings
    
    def set_settings(self, data):
        with open(self.__settings_file__, 'w') as outf:
            json.dump(data, outf)
        self.get_settings()