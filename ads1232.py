from time import sleep
import RPi._GPIO as GPIO
import logging


class ADS1232:
    def __init__(self, pinData, pinSck, pinGain0, pinGain1, pinSpeed, pinPowerDown, pinAddress):
        if (isinstance(pinData, int) and
            isinstance(pinSck, int) and
            isinstance(pinGain0, int) and
            isinstance(pinGain1, int) and
            isinstance(pinSpeed, int) and
            isinstance(pinAddress, int) and
                isinstance(pinPowerDown, int)):  # just check of it is integer

            self.__pinData = pinData
            self.__pinSck = pinSck
            self.__pinGain0 = pinGain0
            self.__pinGain1 = pinGain1
            self.__pinSpeed = pinSpeed
            self.__pinPowerDown = pinPowerDown
            self.__pinAddress = pinAddress
            self.__SetupGpio__()
        else:
            raise TypeError(
                'GPIO have to be pin numbers.\npin must be integer')

    def __SetupGpio__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pinData, GPIO.IN)
        GPIO.setup(self.__pinSck, GPIO.OUT)
        GPIO.setup(self.__pinGain0, GPIO.OUT)
        GPIO.setup(self.__pinGain1, GPIO.OUT)
        GPIO.setup(self.__pinSpeed, GPIO.OUT)
        GPIO.setup(self.__pinPowerDown, GPIO.OUT)
        GPIO.setup(self.__pinAddress, GPIO.OUT)

        self.PowerReset()

    def __single_clock(self):
        GPIO.output(self.__pinSck, True)
        GPIO.output(self.__pinSck, False)

    def _ready(self):
        _is_ready = GPIO.input(self.__pinData) == 0
        logging.debug("check data ready for reading: {result}".format(
            result="YES" if _is_ready is True else "NO"))
        return _is_ready

    def PowerReset(self):
        GPIO.output(self.__pinPowerDown, 0)
        sleep(1)
        GPIO.output(self.__pinPowerDown, 1)

    def ReadVoltage(self, channel):
        raw = self.ReadRawValue(channel)
        return raw * 2.9802325940409414817025043609744e-7 / self.__gain

    def ReadRawValue(self, channel):
        if (isinstance(channel, int)):
            GPIO.output(self.__pinSck, False)

            if (channel == 0):
                GPIO.output(self.__pinAddress, False)
            elif (channel == 1):
                GPIO.output(self.__pinAddress, True)
            else:
                raise TypeError('Channel Error\n')

            return self._WaitUntilDataReadyAndReadRaw()
        else:
            raise TypeError('Channel must be integer\n')

    def _WaitUntilDataReadyAndReadRaw(self, max_tries=40):
        ready_counter = 0
        self.__single_clock()
        # loop until ADS1232 is ready
        while self._ready() is False:
            sleep(0.01)
            ready_counter += 1
            if ready_counter >= max_tries:
                logging.debug('self._read() not ready after 40 trials\n')
                return False

        return self._ReadSignedData()

    def _ReadSignedData(self):
        data_in = 0

        # read first 24 bits of data
        for i in range(24):
            self.__single_clock()
            data_in = (data_in << 1) | GPIO.input(self.__pinData)

        # self.__single_clock()

        signed_data = 0
        print(data_in & 0x800000)
        # 0b1000 0000 0000 0000 0000 0000 check if the sign bit is 1. Negative number.
        if (data_in & 0x800000):
            # convert from 2's complement to int
            signed_data = -((data_in ^ 0xffffff) + 1)
            print("NEG")
        else:  # else do not do anything the value is positive number
            signed_data = data_in
            print("POS")

        logging.debug('Converted 2\'s complement value: ' + str(signed_data))

        return signed_data

    def SetGain(self, gain):
        if (isinstance(gain, int)):
            if(gain in [1,2,64,128]):
                self.__gain=gain
                self.__configGain(gain)
        else:
            raise TypeError('Gian must be integer')

    def __configGain(self, gain):
        if (gain == 1):
            GPIO.output(self.__pinGain0, False)
            GPIO.output(self.__pinGain1, False)
        elif (gain == 2):
            GPIO.output(self.__pinGain0, True)
            GPIO.output(self.__pinGain1, False)
        elif (gain == 64):
            GPIO.output(self.__pinGain0, False)
            GPIO.output(self.__pinGain1, True)
        elif (gain == 128):
            GPIO.output(self.__pinGain0, True)
            GPIO.output(self.__pinGain1, True)
            
    def SetSpeed(self,speed):
        if (isinstance(speed, int)):
            if(speed==10):
                GPIO.output(self.__pinSpeed, False)
            elif(speed==80):
                GPIO.output(self.__pinSpeed, True)
            else:
                raise TypeError('Speed value must be 10 or 80')      
        else:
            raise TypeError('Speed must be integer')  
