from collections import deque
from abstract.digital_filter import DigitalFilter

class MovingAverageFilter(DigitalFilter):
  """
  A moving average filter that calculates the current value as an average of the
  last `window_size` values whenever a new value is received.

  Args:
    window_size: The optional size of the moving average window, or the number of recent values used to compute the moving average. Defaults to `10`.
  """

  def __init__(self, window_size = 10):
    super().__init__()
    self.__window = deque(maxlen=window_size)

  def filter(self, value: float) -> float:
    """
    Applies a moving average filter to a given `value`.

    Args:
      value: The new value to apply the moving average filter to.

    Returns:
      The resulting value from the moving average filter.
    """
    self.__window.append(value)
    self._value = sum(self.__window) // len(self.__window)
    return self._value
