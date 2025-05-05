import RPi.GPIO as GPIO
from gpiozero import Device, Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import Freenove_DHT as DHT
from Status import Status
import time
import os


class HardwareController:
    MAXIMUM_SAFE_TEMP = 25

    def __init__(self, test_mode=False):
        self.is_test_mode = test_mode
        GPIO.setmode(GPIO.BCM)

        # Setup du PiGPIOFactory, empeche le servo de 'jitter' en tout temps
        #os.system("echo sudo pigpiod")
        
        Device.pin_factory = PiGPIOFactory('127.0.0.1')

        self.current_temp = 0

        self.led = 19
        self.buzzer = 17
        self.servo = 18
        self.dht = 24

        self.tones = [440, 1440]
        self.angles = [3, 12]

        GPIO.setup(self.buzzer, GPIO.OUT)
        self.door = Servo(self.servo)
        GPIO.setup(self.led, GPIO.OUT)
        self.door.detach()

        GPIO.output(self.led, GPIO.LOW)

        self.alarm = GPIO.PWM(self.buzzer, 440)

        self.open_door()

        self.status = Status.NONE

    def read_temp(self):
        self.temp_sensor = DHT.DHT(self.dht)
        # On verifie si les donnees du capteur sont valides
        if self.temp_sensor.readDHT11() == 0:
            self.current_temp = self.temp_sensor.getTemperature()
            print(self.temp_sensor.getTemperature())

        return self.current_temp

    def check_temperature(self):
        if not self.is_test_mode:
            self.current_temp = self.read_temp()

        if self.current_temp > self.MAXIMUM_SAFE_TEMP and self.status != Status.ALERT:
            print('Alert temp')
            self.status = Status.ALERT
            self.activate_alarm()
            self.close_door()
            # ui_callback(Status.ALERT)

        elif self.current_temp <= self.MAXIMUM_SAFE_TEMP and self.status != Status.SAFE:
            print('Safe temp')
            self.status = Status.SAFE
            self.deactivate_alarm()
            self.open_door()
            # ui_callback(Status.SAFE)

    def activate_test_mode(self):
        self.is_test_mode = True

    def deactivate_test_mode(self):
        self.is_test_mode = False

    def activate_alarm(self):
        self.alarm.start(50)
        GPIO.output(self.led, GPIO.HIGH)

    def deactivate_alarm(self):
        self.alarm.stop()
        GPIO.output(self.led, GPIO.LOW)

    def close_door(self):
        self.door.min()

    def open_door(self):
        self.door.max()

    def increase_temp(self):
        self.current_temp += 1

    def decrease_temp(self):
        self.current_temp -= 1