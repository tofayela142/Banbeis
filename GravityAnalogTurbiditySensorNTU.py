import spidev
import time
import math
from RPLCD.i2c import CharLCD

# Initialize SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, device 0
spi.max_speed_hz = 1350000  # SPI speed

# Initialize I2C LCD
lcd = CharLCD('PCF8574', 0x27)  # Address for I2C LCD

# MCP3008 channel for the sensor
sensor_channel = 0

# Function to read data from MCP3008
def read_adc(channel):
    # MCP3008 requires 3 bytes: start bit, single-ended channel, and a dummy byte
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    # Combine the last two bytes to get the 10-bit ADC value
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Function to round to decimal places
def round_to_dp(value, decimal_places):
    multiplier = 10 ** decimal_places
    return round(value * multiplier) / multiplier

def main():
    while True:
        volt = 0
        # Average 800 readings for stability
        for _ in range(800):
            sensor_value = read_adc(sensor_channel)
            volt += (sensor_value / 1023.0) * 5 * 2.41  # Convert to voltage
        volt = volt / 800  # Average the readings
        volt = round_to_dp(volt, 2)  # Round to 2 decimal places

        # Calculate NTU based on voltage
        if volt < 2.5:
            ntu = 3000
        else:
            ntu = -1120.4 * (volt ** 2) + 5742.3 * volt - 4353.8

        # Display on LCD
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(f"{volt} V")  # Display voltage
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"{ntu} NTU")  # Display NTU

        time.sleep(0.01)  # Small delay for stability

if name == "main":
    main()
