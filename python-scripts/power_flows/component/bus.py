class Bus:
    def __init__(self, voltage=0, current=0):
        self.voltage = voltage
        self.current = current
        self.power = self._power_()

    def _power_(self):
        return self.voltage * self.current
