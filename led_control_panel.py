from time import sleep

from components.radio_button_array import RadioButtonArray
from components.potentiometer import Potentiometer
from components.rgb_led import RgbLED

pot_intensity = Potentiometer(27)
pot_frequency = Potentiometer(28)

buttons = RadioButtonArray([13, 14, 15])

led = RgbLED(18, 17, 16)
led.on()

prev_intensity = None
prev_frequency = None

while True:
  try:
    if buttons.sel_idx is not None:
      intensity = pot_intensity.exp_normalize_value(50)
      led.color_intensity_u16(buttons.sel_idx, intensity)

      frequency = pot_frequency.range_normalize_value((10, 1000))
      led.color_frequency(buttons.sel_idx, frequency)

    if led.intensity != prev_intensity or led.freq != prev_frequency:
      print(f"Intensity: {led.intensity}\t -- \t Frequency: {led.freq}")
      prev_intensity = led.intensity
      prev_frequency = led.freq

    sleep(.1)
  except KeyboardInterrupt:
    break

led.off()
print("Finished.")

