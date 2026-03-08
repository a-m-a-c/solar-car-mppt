class SolarArray:
    def __init__(self, voc, isc, vmpp, impp, irradiance):
        self.voc = voc  # Open-circuit voltage
        self.isc = isc  # Short-circuit current
        self.vmpp = vmpp  # Voltage at maximum power point
        self.impp = impp  # Current at maximum power point
        self.irradiance = irradiance  # Percent of full sunlight (0 to 1)

        self.voltage = vmpp
        self.current = impp * irradiance

    def get_max_power(self):
        """Calculate the maximum power output of the solar array."""
        return self.vmpp * self.impp
