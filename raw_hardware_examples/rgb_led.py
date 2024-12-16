from time import sleep

from machine import ADC, PWM, Pin

potHigh = ADC(28)
potLow = ADC(27)

redLED = PWM(Pin(13))
greenLED = PWM(Pin(14))
blueLED = PWM(Pin(15))

redLED.freq(1000)
redLED.duty_u16(0)

greenLED.freq(1000)
greenLED.duty_u16(0)

blueLED.freq(1000)
blueLED.duty_u16(0)

SEED = 16
BASE = 4095 ** (1 / SEED)

while True:
  try:
    potHighVal = potHigh.read_u16()
    potLowVal = potLow.read_u16()

    expHigh = potHighVal / 65535 * SEED
    expLow = potLowVal / 65535 * SEED

    channelHigh = round(BASE ** expHigh) - 1
    channelLow = round(BASE ** expLow) - 1

    hexRGB = (channelHigh << 12) + channelLow

    redChannel = hexRGB >> 16
    greenChannel = (hexRGB >> 8) & 0x00ff
    blueChannel = hexRGB & 0x0000ff

    redLED.duty_u16(round(redChannel / 255 * 65535))
    greenLED.duty_u16(round(greenChannel / 255 * 65535))
    blueLED.duty_u16(round(blueChannel / 255 * 65535))

    print(redChannel, greenChannel, blueChannel)
    sleep(0.1)
  except KeyboardInterrupt:
      break

print('Exiting...')
