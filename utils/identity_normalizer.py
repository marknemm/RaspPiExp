from abstract.digital_normalizer import DigitalNormalizer

class IdentityNormalizer(DigitalNormalizer):
  """
  A `DigitalNormalizer` that performs identity normalization
  where the input value is returned as the normalized output value.
  """

  def normalize(self, value: float) -> float:
    """
    Performs identity normalization where the input value is the normalized output value.

    Args:
      value: The value to normalize.

    Returns:
      The input `value`.
    """
    return value
