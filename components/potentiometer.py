from machine import ADC
from utils.normalize import map_exponential, map_range


class Potentiometer:
  """
  A Potentiometer for measuring analog voltage input on an ADC Pin

  Args:
    pin_id: The ID of the MCU Pin that functions as the ADC input for the Potentiometer
  """

  def __init__(self, pin_id: int):
    self.__pot_pin = ADC(pin_id)

  @property
  def value_u16(self) -> int:
    """ The current analog value measured by the potentiometer in range [0, 65535] """
    return self.__pot_pin.read_u16()

  @property
  def value(self) -> int:
    """ The current analog value measured by the potentiometer in range [0, 100] """
    return round(self.value_u16 / 65535 * 100)

  def exp_normalize_value(self, exp_steps = 50, out_range = (0, 65535)) -> int:
    """
    Gets current exponentially normalized analog value measured by the potentiometer.

    Args:
      steps: The optional number of steps to map the original value to on an exponential curve; defaults to 50.
      map_range: The range to bound the mapped exponential curve by; defaults to [0, 65535].

    Returns:
      The exponentially normalized analog value.
    """
    norm_value = self.range_normalize_value(out_range)
    return round(map_exponential(norm_value, exp_steps, out_range))

  def range_normalize_value(self, out_range) -> int:
    """
    Gets current range normalized analog value measured by the potentiometer.

    Args:
      out_range: The range to map the value to.

    Returns:
      The range normalized analog value.
    """
    return round(map_range(self.value_u16, (0, 65535), out_range))
