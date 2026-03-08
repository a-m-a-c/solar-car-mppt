#import numpy

'''
This script calculates the values for key components in the boost converter.
These components include the inductors and capacitors.
We require a few parameters, such as input voltage, output voltage, switching frequency, and ripple current/voltage.
The script will then output the required inductance and capacitance values for the boost converter design.
'''
# Choose input/output parameters
EFFICIENCY = 1.0

V_IN_MIN = 0.0 # V
V_IN_NOM = 27.38 # V
V_IN_MAX = 32.0 # V
V_OUT_MIN = 32.5 # V
V_OUT_NOM = 46.8 # V
V_OUT_MAX = 54.6 # V

#I_IN_MIN = 0.0 # A
I_IN_NOM = 8.22 # A
#I_IN_MAX = 8.66 # A
# I_OUT will only use nominal values
I_OUT_MIN = V_IN_NOM * I_IN_NOM * EFFICIENCY / V_OUT_MAX # A
I_OUT_NOM = V_IN_NOM * I_IN_NOM * EFFICIENCY / V_OUT_NOM # A
I_OUT_MAX = V_IN_NOM * I_IN_NOM * EFFICIENCY / V_OUT_MIN # A

# Choose ripple parameter
DELTA_I = 0.82 # A               [Ripple Current = Imin * 2]
DELTA_V = 0.1 # V

# Choose switching frequency
F_SW = 100000 # Hz

def calculate_output_capacitance():
    print(" \n" + "-"*50)
    D = 1 - (V_IN_NOM / V_OUT_NOM)
    t_off = (1-D) / F_SW
    C = (I_OUT_NOM * t_off) / DELTA_V
    print(f"Switching Frequency: {F_SW} Hz, Duty Cycle: {D:.2f}, Ripple Voltage: {DELTA_V} V, Minimum Output Current: {I_OUT_MIN:.2f} A")
    print(f"Calculated Output Capacitance: {C:.6f} F or {C*1e6:.2f} uF or {C*1e9:.2f} nF")
    print("-"*50 + " \n")

def calculate_inductance():
    print(" \n" + "-"*50)
    # Calculate duty cycle for nominal input and output voltages
    D = 1 - (V_IN_NOM / V_OUT_NOM)
    # Calculate inductance using the formula: L = (V_IN * D) / (DELTA_I * F_SW)
    L = (V_IN_NOM * D) / (DELTA_I * F_SW)
    print(f"Switching Frequency: {F_SW} Hz, Duty Cycle: {D:.2f}, Ripple Current: {DELTA_I} A, Minimum Output Current: {DELTA_I/2:.2f} A")
    print(f"Calculated Inductance: {L:.6f} H or {L*1e3:.2f} mH or {L*1e6:.2f} uH")
    print("-"*50 + " \n")

def calculate_duty_cycle_for_output_voltages():
    print(" \n" + "-"*50)
    # Minimum Input
    D_MIN = 1 - (V_IN_MIN / V_OUT_MIN)
    D_NOM = 1 - (V_IN_MIN / V_OUT_NOM)
    D_MAX = 1 - (V_IN_MIN / V_OUT_MAX)
    print(f"Minimum Input Voltage (V={V_IN_MIN}) Duty Cycles for output voltages:")
    print(f"V_OUT: {V_OUT_MIN}  D_MIN: {D_MIN:.2f}")
    print(f"V_OUT: {V_OUT_NOM}  D_NOM: {D_NOM:.2f}")
    print(f"V_OUT: {V_OUT_MAX}  D_MAX: {D_MAX:.2f}")
    # Nominal Input
    D_MIN = 1 - (V_IN_NOM / V_OUT_MIN)
    D_NOM = 1 - (V_IN_NOM / V_OUT_NOM)
    D_MAX = 1 - (V_IN_NOM / V_OUT_MAX)
    print(f"Nominal Input Voltage (V={V_IN_NOM}) Duty Cycles for output voltages:")
    print(f"V_OUT: {V_OUT_MIN}  D_MIN: {D_MIN:.2f}")
    print(f"V_OUT: {V_OUT_NOM}  D_NOM: {D_NOM:.2f}")
    print(f"V_OUT: {V_OUT_MAX}  D_MAX: {D_MAX:.2f}")
    # Maximum Input
    D_MIN = 1 - (V_IN_MAX / V_OUT_MIN)
    D_NOM = 1 - (V_IN_MAX / V_OUT_NOM)
    D_MAX = 1 - (V_IN_MAX / V_OUT_MAX)
    print(f"Maximum Input Voltage (V={V_IN_MAX}) Duty Cycles for output voltages:")
    print(f"V_OUT: {V_OUT_MIN}  D_MIN: {D_MIN:.2f}")
    print(f"V_OUT: {V_OUT_NOM}  D_NOM: {D_NOM:.2f}")
    print(f"V_OUT: {V_OUT_MAX}  D_MAX: {D_MAX:.2f}")
    print("-"*50 + " \n")


def main():
    calculate_duty_cycle_for_output_voltages()
    calculate_inductance()
    calculate_output_capacitance()

if __name__ == "__main__":
    main()
