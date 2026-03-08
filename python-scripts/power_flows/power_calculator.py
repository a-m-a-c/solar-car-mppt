import argparse

from power_flows.component.bus import Bus
from power_flows.component.converter import Converter
from power_flows.component.solar_array import SolarArray


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the MPPT power flow simulation")
    parser.add_argument("--irradiance", type=float, default=1.0, help="Irradiance fraction (0 to 1)")
    parser.add_argument("--mppt-efficiency", type=float, default=1.0, help="MPPT converter efficiency")
    parser.add_argument("--hv-dcdc-efficiency", type=float, default=0.98, help="HV DC/DC efficiency")
    parser.add_argument("--lv-bus-voltage", type=float, default=45.0, help="LV bus voltage in V")
    parser.add_argument("--hv-bus-voltage", type=float, default=450.0, help="HV bus voltage in V")
    parser.add_argument(
        "--identical-array",
        action="store_true",
        default=False,
        help="Use the first array values for all arrays",
    )
    return parser


def run_simulation(args: argparse.Namespace) -> None:
    solar_arrays = [
        SolarArray(voc=32.0, isc=8.66, vmpp=27.38, impp=8.22, irradiance=args.irradiance),  # F1
        SolarArray(voc=17.86, isc=8.66, vmpp=15.28, impp=8.22, irradiance=args.irradiance),  # BL
        SolarArray(voc=17.86, isc=8.66, vmpp=15.28, impp=8.22, irradiance=args.irradiance),  # BR
        SolarArray(voc=17.86, isc=8.66, vmpp=11.46, impp=8.22, irradiance=args.irradiance),  # R1
        SolarArray(voc=17.86, isc=8.66, vmpp=20.38, impp=8.22, irradiance=args.irradiance),  # R2
    ]

    if args.identical_array:
        solar_arrays = [solar_arrays[0]] * 5

    input_buses = [Bus(voltage=array.voltage, current=array.current) for array in solar_arrays]

    mppt_converters = [
        Converter(
            efficiency=args.mppt_efficiency,
            input_voltage=bus.voltage,
            input_current=bus.current,
            output_voltage=args.lv_bus_voltage,
        )
        for bus in input_buses
    ]

    lv_branch_buses = [
        Bus(voltage=args.lv_bus_voltage, current=converter.output_current)
        for converter in mppt_converters
    ]

    lv_bus = Bus(
        voltage=args.lv_bus_voltage,
        current=sum(bus.current for bus in lv_branch_buses),
    )

    hv_dcdc = Converter(
        efficiency=args.hv_dcdc_efficiency,
        input_voltage=args.lv_bus_voltage,
        input_current=lv_bus.current,
        output_voltage=args.hv_bus_voltage,
    )

    hv_bus = Bus(voltage=args.hv_bus_voltage, current=hv_dcdc.output_current)

    width = 81
    print("\n|====== Simulation Parameters =========|")
    print(f"| Irradiance:             {args.irradiance:6.2f}   [%] |")
    print(f"| MPPT Efficiency:        {args.mppt_efficiency:6.2f}   [%] |")
    print(f"| HV DC/DC Efficiency:    {args.hv_dcdc_efficiency:6.2f}   [%] |")
    print(f"| LV Bus Voltage:         {args.lv_bus_voltage:6.2f}   [V] |")
    print(f"| HV Bus Voltage:         {args.hv_bus_voltage:6.2f}   [V] |")
    print(f"| Identical Array?        {str(args.identical_array):6}       |")
    print("|======================================|")

    print("\n|" + "-" * (width - 2) + "|")
    print("|" + "Input Bus Values".center(width - 2) + "|")
    print("|" + "-" * (width - 2) + "|")
    for i, bus in enumerate(input_buses, start=1):
        print(
            f"|   Input Bus {i}   |  Voltage = {bus.voltage:6.2f} V  | "
            f"Current = {bus.current:5.2f} A | Power = {bus.power:6.2f} W |"
        )
    print("|" + "-" * (width - 2) + "|")

    print("|" + "LV Branch Bus Values".center(width - 2) + "|")
    print("|" + "-" * (width - 2) + "|")
    for i, bus in enumerate(lv_branch_buses, start=1):
        print(
            f"| LV Branch Bus {i} |  Voltage = {bus.voltage:6.2f} V  | "
            f"Current = {bus.current:5.2f} A | Power = {bus.power:6.2f} W |"
        )
    print("|" + "-" * (width - 2) + "|")

    print("|" + "LV Bus Values (Aggregated)".center(width - 2) + "|")
    print("|" + "-" * (width - 2) + "|")
    print(
        f"|      LV Bus     |  Voltage = {lv_bus.voltage:6.2f} V  | "
        f"Current = {lv_bus.current:5.2f} A | Power = {lv_bus.power:6.2f} W |"
    )
    print("|" + "-" * (width - 2) + "|")

    print("|" + "HV Bus Values".center(width - 2) + "|")
    print("|" + "-" * (width - 2) + "|")
    print(
        f"|      HV Bus     |  Voltage = {hv_bus.voltage:6.2f} V  | "
        f"Current = {hv_bus.current:5.2f} A | Power = {hv_bus.power:6.2f} W |"
    )
    print("|" + "-" * (width - 2) + "|")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_simulation(args)


if __name__ == "__main__":
    main()
