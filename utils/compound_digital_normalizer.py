from abstract.digital_normalizer import DigitalNormalizer

class CompoundDigitalNormalizer(DigitalNormalizer):
  """ A `DigitalNormalizer` that combines several other `DigitalNormalizer` instances into a single one. """

  def __init__(self, digital_normalizers: list[DigitalNormalizer] | None = None):
    """
    Args:
      digital_normalizers: An optional list of `DigitalNormalizer` instances that shall be combined. All members have their `normalize` functions invoked in list order. Defaults to `[]`.
    """
    super().__init__()
    self.__digital_normalizers = digital_normalizers if digital_normalizers else []

  def add_normalizer(self, digital_normalizer):
    """
    Adds a `DigitalNormalizer` instance to this `CompoundDigitalNormalizer`. Each added `DigitalNormalizer` will have its `normalize` function invoked in the order it was added.

    Args:
      digital_normalizer: The `DigitalNormalizer` to add.

    Returns:
      This `CompoundDigitalNormalizer` instance for chaining method calls.
    """
    self.__digital_normalizers.append(digital_normalizer)
    return self

  def remove_normalizer(self, digital_normalizer):
    """
    Removes the first `DigitalNormalizer` instance found within this `CompoundDigitalNormalizer`.

    Args:
      digital_normalizer: The `DigitalNormalizer` to remove.

    Returns:
      This `CompoundDigitalNormalizer` instance for chaining method calls.
    """
    self.__digital_normalizers.remove(digital_normalizer)
    return self

  def clear(self):
    """ Clears all `DigitalNormalizer` instances found within this `CompoundDigitalNormalizer`. """
    self.__digital_normalizers.clear()

  def normalize(self, value: float) -> float:
    """
    Invokes all contained `DigitalNormalizer` instances in the order that they were added.

    Args:
      value: The value to normalize.

    Returns:
      The normalized value.
    """
    normalized_value = value

    for digital_normalizer in self.__digital_normalizers:
      normalized_value = digital_normalizer.normalize(normalized_value)

    return normalized_value
