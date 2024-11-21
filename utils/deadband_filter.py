from abstract.digital_filter import DigitalFilter

class DeadbandFilter(DigitalFilter):
  """
  A deadband (low-pass) filter that only updates the current value if the new value
  is more than `deadband` units away from the previous update value.

  Args:
    deadband: The optional size of the band in which new values will be discarded. Only values outside of this band will be accepted. Defaults to `10`.
    apply_range: The optional numeric range in which the filter shall be applied. If filtered values fall outside this range, then they shall no longer be filtered and will be automatically used for update.
  """

  def __init__(self, deadband = 10.0, apply_range: tuple[float, float] = (float('-inf'), float('inf'))):
    super().__init__()
    self.deadband = deadband
    self.apply_range = apply_range

  def filter(self, value: float) -> float:
    """
    Applies a deadband (low-pass) filter to a given `value`.

    Args:
      value: The new value to apply the deadband filter to.

    Returns:
      The resulting value from the deadband filter.
    """
    outside_apply_range = value < self.apply_range[0] or value > self.apply_range[1]
    if outside_apply_range or self._value is None or abs(value - self._value) > self.deadband:
      self._value = value
    return self._value
