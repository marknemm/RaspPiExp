from abstract.digital_filter import DigitalFilter

class CompoundDigitalFilter(DigitalFilter):
  """ A `DigitalFilter` that combines several other `DigitalFilter` instances into a single one. """

  def __init__(self, digital_filters: list[DigitalFilter] | None = None):
    """
    Args:
      digital_filters: An optional list of `DigitalFilter` instances that shall be combined. All members have their `filter` functions invoked in list order. Defaults to `[]`.
    """
    super().__init__()
    self.__digital_filters = digital_filters if digital_filters else []

  def add_filter(self, digital_filter):
    """
    Adds a `DigitalFilter` instance to this `CompoundDigitalFilter`. Each added `DigitalFilter` will have its `filter` function invoked in the order it was added.

    Args:
      digital_filter: The `DigitalFilter` to add.

    Returns:
      This `CompoundDigitalFilter` instance for chaining method calls.
    """
    self.__digital_filters.append(digital_filter)
    return self

  def remove_filter(self, digital_filter):
    """
    Removes the first `DigitalFilter` instance found within this `CompoundDigitalFilter`.

    Args:
      digital_filter: The `DigitalFilter` to remove.

    Returns:
      This `CompoundDigitalFilter` instance for chaining method calls.
    """
    self.__digital_filters.remove(digital_filter)
    return self

  def clear(self):
    """ Clears all `DigitalFilter` instances found within this `CompoundDigitalFilter`. """
    self.__digital_filters.clear()

  def filter(self, value: float) -> float:
    """
    Invokes all contained `DigitalFilter` instances in the order that they were added.

    Args:
      value: The value to filter.

    Returns:
      The filtered value.
    """
    filtered_value = value

    for digital_filter in self.__digital_filters:
      filtered_value = digital_filter.filter(filtered_value)

    return filtered_value
