class SolarPanel:

    def __init__(self, name, num_cells):
        self.name = name
        self.num_cells = num_cells

        # Parameters at 25°C and 1000 W/m²
        self.Voc = 0.744 * num_cells  # Open-circuit voltage (V)
        self.Isc = 8.66  # Short-circuit current (A)
        self.Vmpp = 0.673 * num_cells  # Voltage at maximum power point (V)
        self.Impp = 8.22  # Current at maximum power point (A)

        # Coefficients
        self.temp_voc = -0.27  # Temperature coefficient of Voc (%/°C)
        self.temp_isc = 0.055  # Temperature coefficient of Isc (%/°C)

    def getVoc(self, temperature = 25, irradiance = 1000):
        return self.Voc * (1 + self.temp_voc/100 * (temperature - 25))
    
    def getIsc(self, temperature = 25, irradiance = 1000):
        return self.Isc * (1 + self.temp_isc/100 * (temperature - 25)) * (irradiance / 1000)

    def getVmpp(self, temperature = 25, irradiance = 1000):
        return self.Vmpp * (1 + self.temp_voc/100 * (temperature - 25))
    
    def getImpp(self, temperature = 25, irradiance = 1000):
        return self.Impp * (1 + self.temp_isc/100 * (temperature - 25)) * (irradiance / 1000)