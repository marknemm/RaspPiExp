from machine import PWM, Pin

analogOut = PWM(Pin(15))
analogOut.freq(1000)
analogOut.duty_u16(0)

while True:
  try:
    voltage = float(input('Input voltage [0, 3.3]: '))
    if voltage >= 0 and voltage <= 3.3:
      dutyCycle = round(voltage / 3.3 * 65535)
      analogOut.duty_u16(dutyCycle)
    else:
      print('Voltage is out of bounds; must be in range [0, 3.3]')
  except KeyboardInterrupt:
    break

print('Exiting...')
