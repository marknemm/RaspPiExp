class DigitalNormalizer:

  def __init__(self):
    self._value = None

  @property
  def value(self) -> float | None:
    return self._value

  def normalize(self, value: float) -> float:
    raise NotImplementedError('`normalize` method is not implemented in abstract class `DigitalNormalizer`.')
