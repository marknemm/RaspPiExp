from utime import sleep_ms

def main_loop(callback, delay_ms = 100):
  """
  Executes a given callback function on a main event loop.
  The main event loop iterates indefinitely until a `KeyboardInterrupt` occurs.

  Args:
    callback: The callback function to execute.
    delay_ms: The delay in milliseconds between each iteration of the main event loop;
    defaults to `100`.
  """

  print("\n\nStarting.\n")

  while True:
    try:
      callback()
      sleep_ms(delay_ms)
    except KeyboardInterrupt:
      break

  print("\n\nFinished.")