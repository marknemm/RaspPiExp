from time import sleep

from machine import ADC, Pin

greenLed = Pin(17, Pin.OUT)
yellowLed = Pin(14, Pin.OUT)
redLed = Pin(15, Pin.OUT)

pot = ADC(28)
prevPotVal = None

def resetLEDs():
  greenLed.off()
  yellowLed.off()
  redLed.off()

while True:
  try:
    potVal = round(pot.read_u16() / 65535 * 100)
    if prevPotVal != potVal:
      print(potVal)
      resetLEDs()
      if potVal < 75:
        greenLed.on()
      elif potVal >= 75 and potVal < 95:
        yellowLed.on()
      else:
        redLed.on()
    prevPotVal = potVal
    sleep(.1)
  except KeyboardInterrupt:
    break

print('Exiting...')
