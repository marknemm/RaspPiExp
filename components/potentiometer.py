from machine import ADC, Timer
from abstract.digital_filter import DigitalFilter
from utils.deadband_filter import DeadbandFilter
from utils.normalize import map_exponential, map_range

class Potentiometer:
  """
  A Potentiometer for measuring analog voltage input on an ADC Pin

  Args:
    pin_id: The ID of the MCU Pin that functions as the ADC input for the Potentiometer.
    digital_filter: The optional `DigitalFilter` to apply to the sample voltage values. Defaults to a `DeadbandFilter`. If set to `None`, no filtering is applied.
    sample_period_ms: The optional sample period in milliseconds, which determines the frequency at which to sample Potentiometer values. Defaults to `100`. If set to `0` or a negative number, then sampling does not occur, and the unfiltered voltage value is read directly on each value property read.
  """

  def __init__(self, pin_id: int, digital_filter: DigitalFilter | None = DeadbandFilter(750, (1000, 64535)), sample_period_ms = 100):
    self.__pot_pin = ADC(pin_id)
    self.__value_u16 = self.__pot_pin.read_u16()
    self.__digital_filter = digital_filter
    if sample_period_ms > 0:
      self.__sampling_timer = Timer(-1) # -1 for lower resource virtual timer
      self.__sampling_timer.init(period = sample_period_ms, callback = self.__sample_value)

  @property
  def value_u16(self) -> int:
    """ The current analog value measured by the potentiometer in range [0, 65535] """
    if self.__sampling_timer is None: # If no periodic sampling, then use polling technique and read value directly.
      self.__sample_value()
    return self.__value_u16

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

  def __sample_value(self, _: Timer | None = None):
    """
    Samples the current voltage value and filters it using the configured `DigitalFilter`.
    """
    if self.__digital_filter:
      self.__value_u16 = round(self.__digital_filter.filter(self.__pot_pin.read_u16()))
    else:
      self.__value_u16 = self.__pot_pin.read_u16()
