from programs.boost_converter.battery import Battery
from programs.boost_converter.solar_panel import SolarPanel
from programs.boost_converter.boost_calculator import (
    calculateDutyCycle,
    calculateOutputVoltage,
    calculateInductance,
    calculateRippleCurrent,
    calculateWorstCaseRippleCurrent,
    calculateSwitchingFrequency,
    calculateOutputCapacitance
)

sp1 = SolarPanel("F1", 43)
battery = Battery(2.5, 3.6, 4.2, 13)
F_SW = 500000
L = calculateInductance(sp1.getVmpp(), battery.voltage_nom, 0.1*sp1.getImpp(), F_SW)

def main():
    print("Solar Panel MPP Voltage:", sp1.getVmpp())
    print("Solar Panel MPP Current:", sp1.getImpp())
    print("Inductance uH:", L*1e6)
    print("Ripple Current:", calculateRippleCurrent(sp1.getVmpp(), battery.voltage_nom, L, F_SW))
    print("Worst Case Ripple Current:", calculateWorstCaseRippleCurrent(sp1, battery, L, F_SW))
    print("Output Capacitance uF:", calculateOutputCapacitance(sp1.getVmpp(), battery.voltage_nom, sp1.getImpp(), 0.01*battery.voltage_nom, F_SW)*1e6)

if __name__ == "__main__":
    main()