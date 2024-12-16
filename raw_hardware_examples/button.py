from time import sleep

from machine import Pin

button = Pin(14, Pin.IN, Pin.PULL_UP)
prevButtonVal = 1

redLED = Pin(15, Pin.OUT)
redLED.off()

while True:
  try:
    if prevButtonVal == 1 and button.value() == 0:
      redLED.toggle()
    prevButtonVal = button.value()
    sleep(0.1)
  except KeyboardInterrupt:
    break

print("Exiting...")
