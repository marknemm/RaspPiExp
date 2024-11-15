from components.radio_button_array import RadioButtonArray
from components.potentiometer import Potentiometer
from components.rgb_led import RgbLED

from utils.main_loop import main_loop

pot_intensity = Potentiometer(27)
pot_frequency = Potentiometer(28)

buttons = RadioButtonArray([13, 14, 15])

led = RgbLED(18, 17, 16)
led.on()

def process_controls():
  """ Processes the LED control inputs and configures LED intensity and frequency outputs. """
  if buttons.sel_idx is not None:
    intensity = pot_intensity.exp_normalize_value(50)
    led.color_intensity_u16(buttons.sel_idx, intensity)

    frequency = pot_frequency.range_normalize_value((10, 1000))
    led.color_frequency(buttons.sel_idx, frequency)

  print("\r", f"Intensity: {led.intensity}    Frequency: {led.freq}", end='               ')

main_loop(process_controls)

led.off()
