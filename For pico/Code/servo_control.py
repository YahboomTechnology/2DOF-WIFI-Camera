import time
from machine import Pin, I2C, PWM, Timer, UART, ADC
from pico_car import pico_car

Motor = pico_car()
Servo = pico_car()
Motor.Car_Stop()
# set buzzer pin
BZ = PWM(Pin(22))
BZ.freq(1000)

#UART
uart = UART(0, 9600, bits=8, parity=None, stop=1, tx=Pin(16), rx=Pin(17))
dat = 0
pos=90

def servo_pos(value):
    global pos
    if value == 0:
        Servo.servo180(1, pos)
    if value == 1:
        pos = pos + 5
        if (pos >= 180):
            pos = 180
        Servo.servo180(1, pos)
    if value == 2:
        pos = pos - 5
        if (pos <= 0):
            pos = 0
        Servo.servo180(1, pos)

while True:
    #receive data
    while uart.any() > 0:
        dat = uart.read(9)
        #OLED display
        if dat == b'$Servo,LR':
            Servo_RL = uart.read(2)
            if Servo_RL == b'S#':
                servo_pos(0)
                print(Servo_RL)
            if Servo_RL == b'L#':
                servo_pos(1)
                print(Servo_RL)
            if Servo_RL == b'R#':
                servo_pos(2)
                print(Servo_RL)
        #car control
        elif dat == b'$1,0,0,0#':
            Motor.Car_Run(255,255)
        elif dat == b'$2,0,0,0#':
            Motor.Car_Back(255,255)
        elif dat == b'$3,0,0,0#':
            Motor.Car_Run(0,255)
        elif dat == b'$4,0,0,0#':
            Motor.Car_Run(255,0)
        elif dat == b'$0,0,0,0#':
            Motor.Car_Stop()
        elif dat == b'$Servo,UD':
            Servo_UD = uart.read(3)
            terminator = uart.read(1)
            Servo_UD_I = int(Servo_UD)
            Servo.servo180(2, Servo_UD_I)
            
