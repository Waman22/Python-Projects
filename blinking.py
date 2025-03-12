from machine import Pin
from time import sleep

led = Pin(13, Pin.OUT)
print('Blinking LED Example')
led2 = Pin(12, Pin.OUT)

while True:
  led.value(not led.value())
  sleep(0.5)
  led2.value(not led2.value())