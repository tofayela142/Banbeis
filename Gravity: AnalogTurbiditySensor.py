import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()                                             
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1350000

def read_channel(channel):
    # Send and receive data from MCP3008
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_to_voltage(data, vref=3.3):
    return (data * vref) / 1023.0

try:
    while True:
        turbidity_adc = read_channel(0)  # Assuming CH0
        turbidity_voltage = convert_to_voltage(turbidity_adc)
        print(f"ADC Value: {turbidity_adc}, Voltage: {turbidity_voltage:.2f}V")
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
    print("Program terminated.")
