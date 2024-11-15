from utime import sleep_ms

from utils.hardware_interrupt import HARDWARE_INTERRUPT_INSTANCES

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
      for interrupt_instance in HARDWARE_INTERRUPT_INSTANCES:
        interrupt_instance.clear_interrupt()
      callback()
      sleep_ms(delay_ms)
    except KeyboardInterrupt:
      break

  print("\n\nFinished.")