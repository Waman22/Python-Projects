import machine
import utime

# Define the ADC pin where the soil moisture sensor is connected (GP26 / ADC0)
soil_moisture = machine.ADC(26)  # GPIO 26 is ADC0

# Function to convert ADC reading to a percentage (assuming a 12-bit ADC)
def get_moisture_percentage():
    raw_value = soil_moisture.read_u16()  # Get the 16-bit ADC reading
    moisture_percentage = (raw_value / 65535) * 100  # Convert to percentage (0 to 100%)
    return moisture_percentage

while True:
    moisture = get_moisture_percentage()
    print("Soil Moisture Level: {:.2f}%".format(moisture))  # Display moisture percentage
    utime.sleep(2)  # Delay for 2 seconds before the next reading
    