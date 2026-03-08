from programs.power_flows.component.bus import Bus
from programs.power_flows.component.converter import Converter
from programs.power_flows.component.solar_array import SolarArray


# Simulation Parameters
irradiance = 1.00  # Full sunlight
mppt_efficency = 1
HV_dcdc_efficency = 0.100
LV_bus_voltage = 54.6 #13S ranges from 38 to 55.
HV_bus_voltage = 450.0 # nominal, range unknown rn
identical_array = False # All arrays will be the same as the most powerful array.

def main():
    # Initialise solar array
    solar_array_1 = SolarArray(voc=32.0, isc=8.66, vmpp=27.38, impp=8.22, irradiance=irradiance)    # F1
    solar_array_2 = SolarArray(voc=17.86, isc=8.66, vmpp=15.28, impp=8.22, irradiance=irradiance)   # BL
    solar_array_3 = SolarArray(voc=17.86, isc=8.66, vmpp=15.28, impp=8.22, irradiance=irradiance)   # BR
    solar_array_4 = SolarArray(voc=17.86, isc=8.66, vmpp=11.46, impp=8.22, irradiance=irradiance)   # R1
    solar_array_5 = SolarArray(voc=17.86, isc=8.66, vmpp=20.38, impp=8.22, irradiance=irradiance)   # R2

    solar_array = [solar_array_1, solar_array_2, solar_array_3, solar_array_4, solar_array_5]
    if identical_array:
        solar_array_2 = solar_array_1
        solar_array_3 = solar_array_1
        solar_array_4 = solar_array_1    
        solar_array_5 = solar_array_1    


    # Initialise input bus
    input_bus_1 = Bus(voltage=solar_array_1.voltage, current=solar_array_1.current)
    input_bus_2 = Bus(voltage=solar_array_2.voltage, current=solar_array_2.current)
    input_bus_3 = Bus(voltage=solar_array_3.voltage, current=solar_array_3.current)
    input_bus_4 = Bus(voltage=solar_array_4.voltage, current=solar_array_4.current)
    input_bus_5 = Bus(voltage=solar_array_5.voltage, current=solar_array_5.current)
    input_bus = [input_bus_1, input_bus_2, input_bus_3, input_bus_4, input_bus_5]

    # Initialise mppt converter
    mppt_1 = Converter(efficiency=mppt_efficency, input_voltage=input_bus_1.voltage, input_current=input_bus_1.current, output_voltage=LV_bus_voltage)
    mppt_2 = Converter(efficiency=mppt_efficency, input_voltage=input_bus_2.voltage, input_current=input_bus_2.current, output_voltage=LV_bus_voltage)
    mppt_3 = Converter(efficiency=mppt_efficency, input_voltage=input_bus_3.voltage, input_current=input_bus_3.current, output_voltage=LV_bus_voltage)
    mppt_4 = Converter(efficiency=mppt_efficency, input_voltage=input_bus_4.voltage, input_current=input_bus_4.current, output_voltage=LV_bus_voltage)
    mppt_5 = Converter(efficiency=mppt_efficency, input_voltage=input_bus_5.voltage, input_current=input_bus_5.current, output_voltage=LV_bus_voltage)
    mppt = [mppt_1, mppt_2, mppt_3, mppt_4, mppt_5]

    # Initialise LV branch bus
    LV_branch_bus_1 = Bus(voltage=LV_bus_voltage, current=mppt_1.output_current)
    LV_branch_bus_2 = Bus(voltage=LV_bus_voltage, current=mppt_2.output_current)
    LV_branch_bus_3 = Bus(voltage=LV_bus_voltage, current=mppt_3.output_current)
    LV_branch_bus_4 = Bus(voltage=LV_bus_voltage, current=mppt_4.output_current)
    LV_branch_bus_5 = Bus(voltage=LV_bus_voltage, current=mppt_5.output_current)
    LV_branch_bus = [LV_branch_bus_1, LV_branch_bus_2, LV_branch_bus_3, LV_branch_bus_4, LV_branch_bus_5]

    # Initialise LV bus
    LV_current_sum = sum(bus.current for bus in LV_branch_bus)
    LV_bus = Bus(voltage=LV_bus_voltage, current=LV_current_sum)

    # Initialise HV dcdc converter
    HV_dcdc = Converter(efficiency=HV_dcdc_efficency, input_voltage=LV_bus_voltage, input_current=LV_bus.current, output_voltage=HV_bus_voltage)

    # Initialise HV bus
    HV_bus = Bus(voltage=HV_bus_voltage, current=HV_dcdc.output_current)

    # Data display
    width = 81
    print("\n|====== Simulation Parameters =========|")
    print(f"| Irradiance:             {irradiance:6.2f}   [%] |")
    print(f"| MPPT Efficiency:        {mppt_efficency:6.2f}   [%] |")
    print(f"| HV DC/DC Efficiency:    {HV_dcdc_efficency:6.2f}   [%] |")
    print(f"| LV Bus Voltage:         {LV_bus_voltage:6.2f}   [V] |")
    print(f"| HV Bus Voltage:         {HV_bus_voltage:6.2f}   [V] |")
    print(f"| Identical Array?        {identical_array:6}       |")
    print("|======================================|")

    # Input bus
    print("\n|" + "-" * (width - 2) + "|")
    print("|" + "Input Bus Values".center(width - 2) + "|")
    print("|" + "-" * (width - 2) + "|")
    for i, bus in enumerate(input_bus, start=1):
        print(f"|   Input Bus {i}   |  Voltage = {bus.voltage:6.2f} V  | Current = {bus.current:5.2f} A | Power = {bus.power:6.2f} W |")
    print("|" + "-" * (width - 2) + "|")

    # LV branch bus
    print("|" + "LV Branch Bus Values".center(width - 2) + "|")
    print("|" + "-" * (width - 2) + "|")
    for i, bus in enumerate(LV_branch_bus, start=1):
        print(f"| LV Branch Bus {i} |  Voltage = {bus.voltage:6.2f} V  | Current = {bus.current:5.2f} A | Power = {bus.power:6.2f} W |")
    print("|" + "-" * (width - 2) + "|")

    print("|" + "LV Bus Values (Aggregated)".center(width - 2) + "|")
    print("|" + "-" * (width - 2) + "|")
    print(f"|      LV Bus     |  Voltage = {LV_bus.voltage:6.2f} V  | Current = {LV_bus.current:5.2f} A | Power = {LV_bus.power:6.2f} W |")
    print("|" + "-" * (width - 2) + "|")

    print("|" + "HV Bus Values".center(width - 2) + "|")
    print("|" + "-" * (width - 2) + "|")
    print(f"|      HV Bus     |  Voltage = {HV_bus.voltage:6.2f} V  | Current = {HV_bus.current:5.2f} A | Power = {HV_bus.power:6.2f} W |")
    print("|" + "-" * (width - 2) + "|")

if __name__ == "__main__":
    main()










