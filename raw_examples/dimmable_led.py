from time import sleep

from machine import ADC, PWM, Pin

analogLED = PWM(Pin(15))
analogLED.freq(1000)

pot = ADC(28)

SEED = 50
BASE = 65535 ** (1 / SEED)

while True:
  try:
    potVal = pot.read_u16()
    exp = round(potVal / 65535 * SEED)
    brightness = round(BASE ** exp)
    analogLED.duty_u16(brightness)
    print(potVal, exp, brightness)
    sleep(0.1)
  except KeyboardInterrupt:
      break

print('Exiting...')
