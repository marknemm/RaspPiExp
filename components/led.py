from machine import PWM, Pin


class LED:
  """
  An LED controlled by PWM (Pulse Width Modulation) Pin output

  Args:
    pin_id: The ID of the Pin that will control the LED
    freq: The optional PWM frequency (Hz) for the LED; defaults to 1000
  """

  def __init__(self, pin_id: int, freq = 1000):
    self.__led_pin = PWM(Pin(pin_id, Pin.OUT))
    self.__led_pin.freq(freq)
    self.__led_pin.duty_u16(0)

  @property
  def freq(self) -> int:
    """ The PWM frequency (Hz) for the LED """
    return self.__led_pin.freq()

  @freq.setter
  def freq(self, value):
    if value < 0 or value > 65535:
      raise ValueError(f"The freq must be an int in range [0, 65535]; was given {value}")
    self.__led_pin.freq(value)

  @property
  def intensity_u16(self) -> int:
    """ The intensity (PWM duty cycle) of the LED in range [0, 65535] """
    return self.__led_pin.duty_u16()

  @intensity_u16.setter
  def intensity_u16(self, value: int):
    if value < 0 or value > 65535:
      raise ValueError(f"intensity_u16 must be an int in range [0, 65535]; was given {value}")
    self.__led_pin.duty_u16(value)

  @property
  def intensity(self) -> int:
    """ The intensity (PWM duty cycle) of the LED in range [0, 255] """
    return round(self.intensity_u16 / 65535 * 255)

  @intensity.setter
  def intensity(self, value: int):
    if value < 0 or value > 255:
      raise ValueError(f"intensity must be an int in range [0, 255]; was given {value}")
    self.intensity_u16 = round(value / 255 * 65535)
