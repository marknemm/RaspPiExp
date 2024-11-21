from abstract.digital_filter import DigitalFilter

class ExpMovingAverageFilter(DigitalFilter):
  """
  An exponential moving average (low-pass) filter that calculates the filter value
  by applying a small `smoothing_factor` weight to each new value:

  `(smoothing_factor * new_value) + ((1 - smoothing_factor * old_value))`.

  Args:
    smoothing_factor: The optional smoothing factor to apply to the filter. Defaults to `0.1`.
  """

  def __init__(self, smoothing_factor = 0.1):
    super().__init__()
    self.__smoothing_factor = smoothing_factor

  def filter(self, value: float) -> float:
    """
    Applies an exponential moving average (low-pass) filter to a given `value`.

    Args:
      value: The new value to apply the exponential moving average filter to.

    Returns:
      The resulting value from the exponential moving average filter.
    """
    if self.value is None:
      self._value = value
    else:
      new_weighted_value = self.__smoothing_factor * value
      old_weighted_value = (1 - self.__smoothing_factor) * self.value
      self._value = round(new_weighted_value + old_weighted_value)

    return self._value
