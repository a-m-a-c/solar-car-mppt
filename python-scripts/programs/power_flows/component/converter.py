class Converter:
    def __init__(self, efficiency, input_voltage, input_current, output_voltage):
        self.efficiency = efficiency
        self.input_voltage = input_voltage
        self.input_current = input_current
        self.output_voltage = output_voltage

        self.output_current = self._calculate_output_current()

    def _calculate_output_current(self):
        input_power = self.input_voltage * self.input_current
        output_power = input_power * self.efficiency

        return output_power / self.output_voltage
