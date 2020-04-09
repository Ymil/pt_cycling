from threading import Thread, Timer
import random
import time
import serial
bike_shot_perimeters = {
    29: 2.07973433668,
    28: 2.03261044687,
    27.5: 1.8346901097,
    26: 1.75615029336
}
class serialControl:
    def __init__(self, serialPort, bikeShot):   
        self.tcontroller = Thread(target=self.controller)
        self.tcontroller_running = True
        self.serialPort = serialPort
        self.bikeShot = bikeShot
        self.bikeShotPerimeter = bike_shot_perimeters[self.bikeShot]
        self.serialHandler = None        
        self._reset()
        self._open_serial_port()
        self._last_valid_data = 0
    
    def _reset(self):
        self.data = []
        self.get_counts = 0
        self.distance = 0.0
        self.speed = 0.0
        self.speed_prom = 0.0
        self.speed_max = 0.0
        
    def controller(self):
        self._reset()
        while (self.tcontroller_running):
            try:
                value = self.serialHandler.readline()
                if(not len(value) > 2):
                    continue            
                value = int(value) 
                self.data.append(value)
            except:
                print("Error read value")
                
    def __del__(self):
        self._close_serial_port()
    
    def _open_serial_port(self):
        if self.serialHandler == None:
            self.serialHandler = serial.Serial(self.serialPort, 9600)
    
    def _close_serial_port(self):
        if self.serialHandler:
            self.serialHandler.close()
        
    def start(self):
        self.tcontroller_running = True
        self.tcontroller.start()
        
    def stop(self):
        self.tcontroller_running = False
    
    def processor(self):
        if(len(self.data) > 1):
            print("Valid data")
            data_copy = self.data[:]
            self.data = []
            i = 0
            speed = []
            
            for value in data_copy[1:]:
                tmp_speed = self.bikeShotPerimeter/(value - data_copy[i])*3600
                speed.append(tmp_speed)
                i += 1
            self.distance += (len(data_copy)*self.bikeShotPerimeter)/1000 
            speed_prom = sum(speed)/len(speed)
            self.speed = speed_prom
            self._last_valid_data = time.time()            
        elif( time.time() - self._last_valid_data > 5):
            print("No data")
            self.speed = 0.0
        if(self.get_counts > 0):
            self.speed_prom = (self.speed_prom + self.speed) / self.get_counts
        if(self.speed > self.speed_max):
            self.speed_max = self.speed
            
    def get_data(self):
        self.processor()
        self.get_counts += 1
        rtr = (self.distance, self.speed, self.speed_prom, self.speed_max)
        print(rtr)
        return rtr