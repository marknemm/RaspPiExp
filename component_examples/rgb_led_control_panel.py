from utils.main_loop import main_loop
from utils.exponential_normalizer import ExponentialNormalizer
from utils.linear_normalizer import LinearNormalizer
from components.radio_button_array import RadioButtonArray
from components.potentiometer import Potentiometer
from components.rgb_led import RgbLED

pot_intensity = Potentiometer(27, digital_normalizer = ExponentialNormalizer(50, (0, 65535)))
pot_frequency = Potentiometer(28, digital_normalizer = LinearNormalizer((0, 65535), (10, 1000)))

buttons = RadioButtonArray([13, 14, 15])
led = RgbLED(18, 17, 16)

def process_controls():
  """ Processes the LED control inputs and configures LED intensity and frequency outputs. """
  if buttons.sel_idx is not None:
    led.color_intensity_u16(buttons.sel_idx, pot_intensity.value)
    led.color_frequency(buttons.sel_idx, pot_frequency.value)

  print("\r", f"Intensity: {led.intensity}    Frequency: {led.freq}", end='               ')

main_loop(process_controls, setup = led.on, cleanup = led.off)
