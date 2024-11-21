class DigitalFilter:
  """
  An abstract class that defines a filter interface for filtering digital values.
  """

  def __init__(self):
    self._value: float | None = None

  @property
  def value(self) -> float | None:
    """ The current or most recent value of the filter. """
    return self._value

  def filter(self, value: float) -> float:
    """
    Generic filter interface for all classes derived from `DigitalFilter`.

    Args:
      value: The value to be filtered.

    Raises:
      NotImplementedError: If this abstract method is called directly.

    Returns:
      The filtered value result.
    """
    raise NotImplementedError('`filter` method is not implemented in abstract class `DigitalFilter`')
