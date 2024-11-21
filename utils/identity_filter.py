from abstract.digital_filter import DigitalFilter

class IdentityFilter(DigitalFilter):
  """
  A `DigitalFilter` that performs identity filtering
  where the input value is returned as the filtered output value.
  """

  def normalize(self, value: float) -> float:
    """
    Performs identity filtering where the input value is the filter output value.

    Args:
      value: The value to filter.

    Returns:
      The input `value`.
    """
    return value
