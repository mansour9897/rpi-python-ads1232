from ads1232 import ADS1232
import RPi._GPIO as GPIO 

ads = ADS1232(22,23,4,18,17,27,24)
# ads = ADS1232(7,11,10,25,9,8,5)

print("Welcome to Arianam MFI")
while(True):
    print(ads.ReadVoltage(0))

GPIO.cleanup()
