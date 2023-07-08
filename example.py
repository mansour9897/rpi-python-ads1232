from time import sleep
from ads1232 import ADS1232
from rtd import RTD
import RPi._GPIO as GPIO
import logging

# logging.basicConfig(level=logging.DEBUG)

# ads = ADS1232(22, 23, 4, 18, 17, 27, 24)
ads = ADS1232(7,11,10,25,9,8,5)
ads.SetGain(128)
ads.SetSpeed(10)

pt100 = RTD(100, 66000, 5.0, ads)


print("Welcome to Arianam MFI")
while (True):
    print('{:.2f}'.format(pt100.ReadTemperature()))
    # print(ads.ReadVoltage(0))
    # print("\t")
    # sleep(1)
    # print(ads.ReadVoltage(1))
    # print("\n")
    sleep(1)

GPIO.cleanup()
