from machine import ADC, Timer
from abstract.digital_filter import DigitalFilter
from abstract.digital_normalizer import DigitalNormalizer
from utils.deadband_filter import DeadbandFilter
from utils.linear_normalizer import LinearNormalizer

class Potentiometer:
  """ A Potentiometer (variable resistor dial) for producing and measuring analog voltage input on an ADC Pin. """

  def __init__(
    self,
    pin_id: int,
    sample_period_ms = 100,
    digital_filter: DigitalFilter | None = None,
    digital_normalizer: DigitalNormalizer | None = None,
  ):
    """
    Args:
      pin_id: The ID of the Pin that functions as the ADC input for the Potentiometer.
      sample_period_ms: The optional sample period in milliseconds, which determines the frequency at which to sample Potentiometer values. Defaults to `100`. If set to `0` or a negative number, then sampling does not occur, and the voltage value is read directly on each value property read.
      digital_filter: The optional `DigitalFilter` to apply to the sample voltage values. Defaults to a `DeadbandFilter(750, (1000, 64535))`. Supply `IdentityFilter` if no filtering should be applied.
      digital_normalizer: The optional `DigitalNormalizer` to apply to the sample voltage values after any filtering is performed. Defaults to `LinearNormalizer((0, 65535), (0, 100))`. Supply `IdentityNormalizer` if no normalization should be applied.
    """
    self.__pot_pin = ADC(pin_id)
    self.__value_u16 = 0
    self.__value = 0
    self.__digital_filter = digital_filter if digital_filter else DeadbandFilter(750, (1000, 64535))
    self.__digital_normalizer = digital_normalizer if digital_normalizer else LinearNormalizer((0, 65535), (0, 100))
    if sample_period_ms > 0:
      self.__sampling_timer = Timer(-1) # -1 for lower resource virtual timer
      self.__sampling_timer.init(period = sample_period_ms, callback = self.sample_value)
    self.sample_value()

  @property
  def value(self) -> int:
    """ The most recent filtered sample value with normalization applied. """
    if self.__sampling_timer is None: # If no periodic sampling, then use polling.
      self.sample_value()
    return self.__value

  @property
  def value_u16(self) -> int:
    """ The most recent filtered sample value in range `[0, 65535]`. """
    if self.__sampling_timer is None: # If no periodic sampling, then use polling.
      self.sample_value()
    return self.__value_u16

  def sample_value(self, _: Timer | None = None) -> int:
    """
    Manually samples the current voltage value, filters it using the
    configured `DigitalFilter`, and normalizes it using the configured `DigitalNormalizer`.

    Returns:
      The filtered and normalized sample value.
    """
    if self.__digital_filter:
      self.__value_u16 = round(self.__digital_filter.filter(self.__pot_pin.read_u16()))
    else:
      self.__value_u16 = self.__pot_pin.read_u16()

    if self.__digital_normalizer:
      self.__value = round(self.__digital_normalizer.normalize(self.__value_u16))

    return self.__value
