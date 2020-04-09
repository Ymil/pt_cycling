import argparse
import serial
import time
import random
import math
import signal
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-speedMode', default='random', help='Indica el modo para establecer la velocidad [stable|random]')
parser.add_argument('-speed', default=10, type=float, help='Modo estable: Establece la velocidad km/h')
parser.add_argument('-speedMin', default=0, type=float, help='Modo random: Establece la velocidad minima')
parser.add_argument('-speedMax', default=100, type=float, help='Modo random: Establece la velocidad maxima')
parser.add_argument('-shotBike', default='29', type=str, help='Indica el rodado de la bici [26/27.5/25.29]')
args = parser.parse_args()

print(args)
bike_shot_perimeters = {
    '29': 2.07973433668,
    '28': 2.03261044687,
    '27.5': 1.8346901097,
    '26': 1.75615029336
}

bike_shot_perimeter = bike_shot_perimeters[args.shotBike]
cycle_mode = 'speed_stable'
if(args.speedMode == 'stable'):
    velocity_stabe = args.speed
    print("Datos de interes")
    print("Velocidad: {} KM/H".format(velocity_stabe))
    print("\t1h -> {} KM".format(velocity_stabe))
    for minutos in [45, 30, 15, 10, 5, 1]:
        print("\t{} Minutos -> {} KM".format(minutos, velocity_stabe/(60/minutos)))
    print("Tiempo:".format())
    
    print("\t{} KM -> 60 Minutos".format(velocity_stabe))
    for distance in [10,5,3,1,0.5,0.1]:
        print("\t{} KM -> {} Minutos".format(distance, distance*60/velocity_stabe))
    
elif(args.speedMode == 'random'):
    velocity_min = args.speedMin
    velocity_max = args.speedMax  



  
    
s2 = serial.Serial('COM2', 9600, timeout=1)
time_last = 0
time_start = 0
millis = 0
def signal_handler(sig, frame):
    if(s2.is_open):
        s2.close()
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

while True:            
    if(time_start == 0):
        time_start = time.time()
        continue
    time_last = int((time.time()-time_start)*1000)    
    s2.write(str(time_last).encode('utf-8'))
    s2.write(b'\n')
    if(args.speedMode == 'stable'):
        sleep = (bike_shot_perimeter*3600)/(velocity_stabe*1000)
    elif(args.speedMode == 'random'):
        sleep = (bike_shot_perimeter*3600)/(random.randint(velocity_min, velocity_max)*1000)
    time.sleep(sleep)
    