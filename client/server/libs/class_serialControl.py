from threading import Thread, Timer
import random
import time
import serial

class serialControl:
    def __init__(self, serialPort):   
        self.tcontroller = Thread(target=self.controller)
        self.tcontroller_running = True
        self.serialPort = serialPort
        self.serialHandler = None
        self._reset()
        self._open_serial_port()
    
    def _reset(self):
        self.distance = 0.0
        self.speed = 0.0
        self.speed_prom = 0.0
        self.speed_max = 0.0
        self.cycle = 0
        
    def controller(self):
        self._reset()
        while (self.tcontroller_running):
            self.distance += random.uniform(0.001, .01)
            self.speed = random.uniform(10, 50)
            if(self.cycle > 0):
                self.speed_prom = self.speed / self.cycle
            if(self.speed > self.speed_max):
                self.speed_max = self.speed
            self.cycle += 1
            print('alive')
            time.sleep(0.1)
                
    def __del__(self):
        self._close_serial_port()
    
    def _open_serial_port(self):
        if self.serialHandler == None:
            #self.serialHandler = serial.Serial(self.serialPort, 9600)
            #self.serialHandler.open()
            pass
    
    def _close_serial_port(self):
        #self.serialHandler.close()
        pass
    def start(self):
        self.tcontroller_running = True
        self.tcontroller.start()
        
    def stop(self):
        self.tcontroller_running = False
    
    def get_data(self):
        return (self.distance, self.speed, self.speed_prom, self.speed_max, self.cycle)