
class Asset:
    def __init__(self, name, data): ##data is a multidimensional list of timestamps and arduino readings
        self.name = name
        self.data = data

class Battery(Asset):
    def __init_subclass__(self, alertThreshold, alertFlagStatus):
        self.alertThreshold = alertThreshold
        self.alertFlagStatus = False

class Sensor(Asset):
    def __init_subclass__(self, alertThreshold, alertFlagStatus):
        self.alertThreshold = alertThreshold
        self.alertFlatStatus = False