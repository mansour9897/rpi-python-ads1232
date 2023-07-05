from time import sleep
from ads1232 import ADS1232
from rtd import RTD
import RPi._GPIO as GPIO

ads = ADS1232(22, 23, 4, 18, 17, 27, 24)
ads.SetGain(128)
ads.SetSpeed(80)

pt100 = RTD(100, 66000, 5.0, ads)
sleep(5)
# ads = ADS1232(7,11,10,25,9,8,5)

print("Welcome to Arianam MFI")
while (True):
    print(pt100.ReadTemperature())
    sleep(1)

GPIO.cleanup()
