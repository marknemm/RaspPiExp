class DigitalNormalizer:
  """
  An abstract class that defines a normalization interface for normalizing digital values.
  """

  def __init__(self):
    self._value: float | None = None

  @property
  def value(self) -> float | None:
    """ The current or most recent normalized value. """
    return self._value

  def normalize(self, value: float) -> float:
    """
    Generic normalize interface for all classes derived from `DigitalNormalizer`.

    Args:
      value: The value to be normalized.

    Raises:
      NotImplementedError: If this abstract method is called directly.

    Returns:
      The normalized value result.
    """
    raise NotImplementedError('`normalize` method is not implemented in abstract class `DigitalNormalizer`.')
