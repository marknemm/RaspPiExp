from abstract.digital_normalizer import DigitalNormalizer

class LinearNormalizer(DigitalNormalizer):
  """
  A `DigitalNormalizer` that performs linear mappings of sample values
  from their position in a `src_range` to their corresponding position in a `dest_range`.
  """

  def __init__(self, src_range: tuple[float, float], dest_range: tuple[float, float]):
    """
    Args:
      src_range: The source or initial linear range that sample values will fall within.
      dest_range: The destination or normalized linear range that normalized values will be generated within.
    """
    super().__init__()
    self.__src_range = src_range
    self.__dest_range = dest_range

  @property
  def src_range(self):
    """ The source or initial linear range that sample values will fall within. """
    return self.__src_range

  @property
  def dest_range(self):
    """ The destination or normalized linear range that normalized values will be generated within. """
    return self.__dest_range

  def normalize(self, value: float) -> float:
    """
    Normalizes a given `value` by performing a linear mapping from its position in the
    configured `src_range` to its corresponding value in the configured `dest_range`.

    Args:
      value: The value to normalize.

    Returns:
      The normalized value.
    """
    src_scale = self.src_range[1] - self.src_range[0]
    percentage = (value - self.src_range[0]) / src_scale

    dest_scale = self.dest_range[1] - self.dest_range[0]
    return (dest_scale * percentage) + self.dest_range[0]
