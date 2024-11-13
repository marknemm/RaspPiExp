def map_exponential(value: float, exp_steps: int, value_range: tuple[float, float]) -> float:
  """
  Maps a value on a linear curve to a value on an exponential curve that fits within the range bounding the linear curve

  Args:
    value: The linear value to map to the exponential curve
    exp_steps: The number of steps or data points to map to on the linear curve
    range: The range bounding the curve

  Returns:
    The value mapped to the exponential curve
  """

  scale = value_range[1] - value_range[0]
  base = scale ** (1 / exp_steps)
  exp = (value - value_range[0]) / scale * exp_steps
  return (base ** exp) + value_range[0]

def map_range(value: float, src_range: tuple[float, float], dest_range: tuple[float, float]) -> float:
  """
  Maps a value in a given src range to a value in a given dest range

  Args:
    value: The value within the src range to map to a value in the dest range
    src_range: The source range
    dest_range: The destination range

  Returns:
    The value mapped to the dest range
  """
  src_scale = src_range[1] - src_range[0]
  percentage = (value - src_range[0]) / src_scale

  dest_scale = dest_range[1] - dest_range[0]
  return (dest_scale * percentage) + dest_range[0]
