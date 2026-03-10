from programs.boost_converter.battery import Battery
from programs.boost_converter.solar_panel import SolarPanel
import numpy as np

def calculateDutyCycle(v_in, v_out):
    d = 1 - (v_in / v_out)
    return d

def calculateOutputVoltage(v_in, d):
    v_out = v_in / (1 - d)
    return v_out

def calculateInductance(v_in, v_out, delta_i, f_sw):
    # Calculate duty cycle for nominal input and output voltages
    d = calculateDutyCycle(v_in, v_out)
    # Calculate inductance using the formula: L = (V_IN * D) / (DELTA_I * F_SW) 
    l = (v_in * d) / (delta_i * f_sw)
    return l

def calculateRippleCurrent(v_in, v_out, l, f_sw):
    d = calculateDutyCycle(v_in, v_out)
    delta_i = (v_in * d) / (l * f_sw)
    return delta_i

def calculateWorstCaseRippleCurrent(solarPanel: SolarPanel, battery: Battery, l, f_sw):
    vin_array = np.linspace(0, solarPanel.getVoc(), 100)
    vout_array = np.linspace(battery.cell_voltage_min, battery.cell_voltage_max, 100)

    max_ripple_current = 0
    for i in range(len(vin_array)):
        for j in range(len(vout_array)):
            delta_i = calculateRippleCurrent(vin_array[i], vout_array[j], l, f_sw)
            if delta_i > max_ripple_current:
                max_ripple_current = delta_i
                worst_case_vin = vin_array[i]
                worst_case_vout = vout_array[j]
    
    return max_ripple_current

def calculateSwitchingFrequency(v_in, v_out, l, delta_i):
    d = calculateDutyCycle(v_in, v_out)
    f_sw = (v_in * d) / (l * delta_i)
    return f_sw

def calculateOutputCapacitance(v_in, v_out, i_in, delta_v, f_sw, eff = 1.0):
    i_out = v_in*i_in * eff/ v_out
    d = calculateDutyCycle(v_in, v_out)
    t_off = (1-d) / f_sw
    c = (i_out * t_off) / delta_v
    return c
