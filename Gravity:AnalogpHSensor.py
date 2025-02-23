import spidev
import time

# MCP3008 SPI Setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0 (CE0)
spi.max_speed_hz = 1350000

# Calibration Constants (adjust based on your calibration)
V_pH7 = 2.5  # Voltage at pH 7
V_pH4 = 3.03  # Voltage at pH 4
Slope = (V_pH7 - V_pH4) / (7 - 4)  # Calculate slope

# Function to read ADC value from MCP3008
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

# Convert ADC value to voltage
def convert_to_voltage(adc_value, vref=3.3):
    return (adc_value / 1023.0) * vref

# Convert voltage to pH
def voltage_to_pH(voltage):
    return 7 + (voltage - V_pH7) / Slope

# Main loop to read sensor
try:
    while True:
        adc_value = read_adc(0)  # Read from CH0
        voltage = convert_to_voltage(adc_value)
        pH = voltage_to_pH(voltage)
        print(f"ADC: {adc_value}, Voltage: {voltage:.2f}V, pH: {pH:.2f}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    spi.close()
