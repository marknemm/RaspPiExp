from utime import ticks_ms

def debounce(func, delay_ms: int):
  """
  Produces a debounced version of the function `func` that will only be invoked
  after `delay_ms` milliseconds have passed since the last time it was invoked.

  Args:
    func: The function that shall be debounced.
    delay_ms: The debounce delay in milliseconds.

  Returns:
    The debounce version of the input function.
  """
  last_called = 0

  def wrapper(*args, **kwargs):
    nonlocal last_called
    if ticks_ms() - last_called >= delay_ms:
      last_called = ticks_ms()
      return func(*args, **kwargs)

  return wrapper
