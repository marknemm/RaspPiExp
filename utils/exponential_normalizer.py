from abstract.digital_normalizer import DigitalNormalizer

class ExponentialNormalizer(DigitalNormalizer):
  """
  A `DigitalNormalizer` that performs exponential mappings of sample values
  from their linear position to their position on an exponential curve with
  Y-axis bounded by `dest_range`.
  """

  def __init__(
    self,
    exp_steps: int,
    src_range: tuple[float, float],
    dest_range: tuple[float, float] | None = None
  ):
    """
    Args:
      exp_steps: The number of mapped data points evenly spaced on the X-axis of the exponential curve.
      src_range: The range bounding Y;-axis values on the source linear curve.
      dest_range: The optional range bounding Y-axis values on the destination exponential curve. Defaults to `src_range`.
    """
    super().__init__()
    self.__exp_steps = exp_steps
    self.__src_range = src_range
    self.__dest_range = dest_range if dest_range else src_range

  @property
  def exp_steps(self):
    """ The number of mapped data points evenly spaced on the X-axis of the exponential curve. """
    return self.__exp_steps

  @property
  def src_range(self):
    """ The range bounding Y-axis values on the source linear curve. """
    return self.__src_range

  @property
  def dest_range(self):
    """ The range bounding Y-axis values on the destination exponential curve. """
    return self.__dest_range

  def normalize(self, value: float) -> float:
    """
    Normalizes given values on a linear curve to one of `exp_step` data points
    on an exponential curve that fits within the configured `dest_range`.

    Args:
      value: The value to normalize.

    Returns:
      The normalized value.
    """
    src_scale = self.src_range[1] - self.src_range[0]
    dest_scale = self.dest_range[1] - self.dest_range[0]

    base = dest_scale ** (1 / self.exp_steps)
    exp = (value - self.src_range[0]) / src_scale * self.exp_steps
    return (base ** exp) + self.dest_range[0]