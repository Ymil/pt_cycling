import serial
import time
import random
import math
execution = False
s1 = serial.Serial()
s1.port = 'COM3'

s2 = serial.Serial('COM2', 9600, timeout=1)
execution = True
time_delta = 0
time_last = 0
time_start = 0
millis = 0
while True:            
    if(time_start == 0):
        time_start = time.time()
        continue
    print("Write data")
    time_last = int((time.time()-time_start)*1000)    
    s2.write(str(time_last).encode('utf-8'))
    s2.write(b'\n')
    #s2.flush()
    #sleep = random.uniform(0.1, 2)
    sleep = random.randint(10, 100)/100
    print(sleep)
    time.sleep(sleep)
    