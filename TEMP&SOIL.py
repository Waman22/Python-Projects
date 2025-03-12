import machine
import utime
from time import sleep
from picozero import pico_temp_sensor
from machine import Pin  # Import the Pin class from machine module

# Define the LED pins
led_1 = Pin(13, Pin.OUT)
led_2 = Pin(12, Pin.OUT)

# Define the ADC pin where the soil moisture sensor is connected (GP26 / ADC0)
soil_moisture = machine.ADC(26)  # GPIO 26 is ADC0

# Convert from celsius to fahrenheit
def celsius_to_fahrenheit(temp_celsius): 
    temp_fahrenheit = temp_celsius * (9/5) + 32 
    return temp_fahrenheit

# Function to convert ADC reading to a percentage (assuming a 12-bit ADC)
def get_moisture_percentage():
    raw_value = soil_moisture.read_u16()  # Get the 16-bit ADC reading
    moisture_percentage = (raw_value / 65535) * 100  # Convert to percentage (0 to 100%)
    return moisture_percentage

while True:
    moisture = get_moisture_percentage()
    print("Soil Moisture Level: {:.2f}%".format(moisture))  # Display moisture percentage
    utime.sleep(2)  # Delay for 2 seconds before the next reading
    
    # Reading and printing the internal temperature
    temperatureC = pico_temp_sensor.temp
    temperatureF = celsius_to_fahrenheit(temperatureC)

    print("Internal Temperature:", temperatureC, "°C")
    print("Internal Temperature:", temperatureF, "°F")
    
    # Check if the temperature is too high or too low
    if temperatureC >= 25:
        led_1.value(1)  # Turn on led_1
        led_2.value(0)  # Ensure led_2 is off
        print("Temperature is too high")
        if moisture >= 85:
            led_1.value(0)  # Turn on led_1
            led_2.value(1)  # Ensure led_2 is off
            print("Moisture is too high")
            if moisture <= 85:
                led_1.value(1)  # Turn on led_1
                led_2.value(0)  # Ensure led_2 is off
                print("Moisture is too low")
    else:
        #led_1.value(0)  # Ensure led_1 is off
        #led_2.value(1)  # Turn on led_2
        print("Temperature is too low")
    
    # Wait one second between each reading
    sleep(5)

    
