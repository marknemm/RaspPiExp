from utime import sleep_ms
from utils.hardware_interrupt import HARDWARE_INTERRUPT_INSTANCES

def main_loop(callback, delay_ms = 100, setup = None, cleanup = None):
  """
  Executes a given callback function on a main event loop.
  The main event loop iterates indefinitely until a `KeyboardInterrupt` occurs.

  Args:
    callback: The callback function to execute.
    delay_ms: An optional delay in milliseconds between each iteration of the main event loop. Defaults to `100`.
    setup: An optional setup callback function that will execute code before the main loop initializes. Defaults to `None`.
    cleanup: An optional cleanup callback function that will execute once the main loop completes. Defaults to `None`.
  """

  print("\n\nStarted.\n")

  if setup:
    setup()

  while True:
    try:
      for interrupt_instance in HARDWARE_INTERRUPT_INSTANCES:
        interrupt_instance.clear_interrupt()
      callback()
      sleep_ms(delay_ms)
    except KeyboardInterrupt:
      break

  if cleanup:
    cleanup()

  print("\n\nFinished.")