class Battery:
    def __init__(self, cell_voltage_min, cell_voltage_nom,cell_voltage_max, series_cells):
        self.cell_voltage_min = cell_voltage_min
        self.cell_voltage_nom = cell_voltage_nom
        self.cell_voltage_max = cell_voltage_max
        self.series_cells = series_cells
        self.voltage_min = cell_voltage_min * series_cells
        self.voltage_nom = cell_voltage_nom * series_cells
        self.voltage_max = cell_voltage_max * series_cells