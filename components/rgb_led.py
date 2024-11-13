from components.led import LED


class RgbLED:
  """
  An RGB LED controlled by PWM Pin output across 3 channels.

  Args:
    red_pin_id: The ID of the Pin that will control the red LED.
    green_pin_id: The ID of the Pin that will control the green LED.
    blue_pin_id: The ID of the Pin that will control the blue LED.
  """

  COLORS = ['RED', 'GREEN', 'BLUE']
  COLOR_CODES = [0, 1, 2]

  RED = COLOR_CODES[0]
  GREEN = COLOR_CODES[1]
  BLUE = COLOR_CODES[2]

  def __init__(self, red_pin_id: int, green_pin_id: int, blue_pin_id: int):
    self.__red_led = LED(red_pin_id)
    self.__green_led = LED(green_pin_id)
    self.__blue_led = LED(blue_pin_id)

  @property
  def freq(self) -> tuple[int, int, int]:
    """
    Gets all RGB frequency values in range [0, 65535].

    Returns:
      An RGB tuple containing all color frequency values in range [0, 65535].
    """
    return (
      self.__red_led.freq,
      self.__green_led.freq,
      self.__blue_led.freq,
    )

  @property
  def intensity(self) -> tuple[int, int, int]:
    """
    Gets all RGB color intensity values in range [0, 255].

    Returns:
      An RGB tuple containing all color intensity values in range [0, 255].
    """

    return (
      self.__red_led.intensity,
      self.__green_led.intensity,
      self.__blue_led.intensity,
    )

  @property
  def intensity_u16(self) -> tuple[int, int, int]:
    """
    Gets all RGB color intensity values in range [0, 65535].

    Returns:
      An RGB tuple containing all color intensity values in range [0, 65535].
    """

    return (
      self.__red_led.intensity_u16,
      self.__green_led.intensity_u16,
      self.__blue_led.intensity_u16,
    )

  def on(self, intensity = (255, 255, 255), freq = (1000, 1000, 1000)):
    """
    Turns the RGB LED on.

    Args:
      intensity: An optional RGB tuple containing all color intensity values. Defaults to (255, 255, 255).
      freq: An optional RGB tuple containing all color frequency (Hz) values. Defaults to (1000, 1000, 1000).
    """
    self.color_intensity(RgbLED.RED, intensity[RgbLED.RED])
    self.color_intensity(RgbLED.GREEN, intensity[RgbLED.GREEN])
    self.color_intensity(RgbLED.BLUE, intensity[RgbLED.BLUE])

    self.color_frequency(RgbLED.RED, freq[RgbLED.RED])
    self.color_frequency(RgbLED.GREEN, freq[RgbLED.GREEN])
    self.color_frequency(RgbLED.BLUE, freq[RgbLED.BLUE])

  def off(self):
    """ Turns the RGB LED completely off by zeroing out all color intensity values while leaving frequency as-is. """
    self.color_intensity(RgbLED.RED, 0)
    self.color_intensity(RgbLED.GREEN, 0)
    self.color_intensity(RgbLED.BLUE, 0)

  def color_frequency(self, color: int, value: int | None = None) -> int:
    """
    Sets and/or gets the intensity of a given colored LED in range [0, 65535].

    Args:
      color: The color of the LED to set/get the frequency of (RgbLED.RED, RgbLED.GREEN, RgbLED.BLUE).
      value: The frequency value to set in range [0, 65535]. If not provided, only gets the value.

    Returns:
      The frequency of the colored LED in range [0, 65535].

    Raises:
      ValueError: If the color argument is outside of range [0, 2].
      ValueError: If the value argument is outside of range [0, 65535].
    """

    target_led = self.__get_led(color)

    if value is not None:
      target_led.freq = value

    return target_led.freq

  def color_intensity(self, color: int, value: int | None = None) -> int:
    """
    Sets and/or gets the intensity of a given colored LED in range [0, 255].

    Args:
      color: The color of the LED to set/get the intensity of (RgbLED.RED, RgbLED.GREEN, RgbLED.BLUE).
      value: The intensity value to set in range [0, 255]. If not provided, only gets the value.

    Returns:
      The intensity of the colored LED in range [0, 255].

    Raises:
      ValueError: If the color argument is outside of range [0, 2].
      ValueError: If the value argument is outside of range [0, 255].
    """

    target_led = self.__get_led(color)

    if value is not None:
      target_led.intensity = value

    return target_led.intensity

  def color_intensity_u16(self, color: int, value: int | None = None) -> int:
    """
    Sets and/or gets the intensity of a given colored LED in range [0, 65535].

    Args:
      color: The color of the LED to set the intensity of (RgbLED.RED, RgbLED.GREEN, RgbLED.BLUE).
      value: The intensity value to set in range [0, 65535].

    Returns:
      The intensity of the colored LED in range [0, 65535].

    Raises:
      ValueError: If the color argument is outside of range [0, 2].
      ValueError: If the value argument is outside of range [0, 65535].
    """

    target_led = self.__get_led(color)

    if value is not None:
      target_led.intensity_u16 = value

    return target_led.intensity_u16

  def __get_led(self, color: int) -> LED:
    """
    Gets the colored LED object.

    Args:
      color: The color of the LED to retrieve (RgbLED.RED, RgbLED.GREEN, RgbLED.BLUE).

    Returns:
      The retrieved colored LED object.

    Raises:
      ValueError: If the color argument is outside of range [0, 2].
    """

    if color == RgbLED.RED:
      return self.__red_led
    if color == RgbLED.GREEN:
      return self.__green_led
    if color == RgbLED.BLUE:
      return self.__blue_led

    raise ValueError(f"color must be an int in range [0, 2]; was given {color}")