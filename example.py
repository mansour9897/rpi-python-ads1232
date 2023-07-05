from time import sleep
from ads1232 import ADS1232
from rtd import RTD
import RPi._GPIO as GPIO

# ads = ADS1232(22, 23, 4, 18, 17, 27, 24)
ads = ADS1232(7,11,10,25,9,8,5)
ads.SetGain(128)
ads.SetSpeed(10)

pt100 = RTD(100, 66000, 5.0, ads)


print("Welcome to Arianam MFI")
while (True):
    # print(pt100.ReadTemperature())
    print(ads.ReadRawValue(0))
    print("\t")
    print(ads.ReadRawValue(0))
    print("\n")
    sleep(1)

GPIO.cleanup()
