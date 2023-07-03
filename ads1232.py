from time import sleep
class ADS1232:
    def __init__(self, pinData, pinSck, pinGain0, pinGain1, pinSpeed, pinPowerDown):
        self.__pinData = pinData
        self.__pinSck = pinSck
        self.__pinGain0 = pinGain0
        self.__pinGain1 = pinGain1
        self.__pinSpeed = pinSpeed
        self.__pinPowerDown = pinPowerDown
        
        self.PowerReset()

    def PowerReset(self):
        sleep(1)

    def ReadVoltage(self, channel):
        raw = self.ReadRawValue(channel)

    def ReadRawValue(self, channel):
    