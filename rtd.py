from ads1232 import ADS1232


class RTD:
    def __init__(self, ptRes, refRes, vExc, ads):
        if (isinstance(ptRes, int) and
            isinstance(refRes, int) and
                isinstance(vExc, float)):

            self.__refRessistor = refRes
            self.__vExc = vExc
            
            self.__setAds1232(ads)
            self.__setPtRes(ptRes)
            
            self.__Iref = vExc / (self.__refRessistor + self.__ptRes)
        else:
            raise TypeError('ptRes must be integer,\
                            refRes must be integer,\
                            vExc must be float.')

    def __setAds1232(self, ads):
        # if (ads is ADS1232):
            self.__ads1232 = ads
        # else:
            # raise TypeError('In RTD class ads in not ADS1232 object')

    def __setPtRes(self, ptRes):
        if (ptRes in [100, 100]):
            self.__ptRes = ptRes
        else:
            raise TypeError('ptRes value must be 100 or 1000')

    def ReadTemperature(self):
        ch0 = self.__ads1232.ReadVoltage(0)
        ch1 = self.__ads1232.ReadVoltage(1)
        v = ch0 - ch1 *2
        resistor =  v / self.__Iref
        return self.__CalculateTemperature(resistor)

    def __CalculateTemperature(self,res):
        #y=ax²+bx+c
        Temp = 0.00114 * res * res + 2.32391 * res - 243.81753    
        return Temp
    
    
    
