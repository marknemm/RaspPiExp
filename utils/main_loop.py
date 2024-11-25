from utime import sleep_ms
from utils.hardware_interrupt import HardwareInterrupt

def main_loop(callback, delay_ms = 100, setup = None, cleanup = None, auto_lock_interrupts = False):
  """
  Executes a given callback function on a main event loop.
  The main event loop iterates indefinitely until a `KeyboardInterrupt` occurs.

  Args:
    callback: The callback function to execute.
    delay_ms: An optional delay in milliseconds between each iteration of the main event loop. Defaults to `100`.
    setup: An optional setup callback function that will execute code before the main loop initializes. Defaults to `None`.
    cleanup: An optional cleanup callback function that will execute once the main loop completes. Defaults to `None`.
    auto_lock_interrupts: An optional flag that enables auto locking of all hardware interrupts before each loop iteration and unlocks them after each iteration. Defaults to `False`.
  """

  print("\n\nStarted.\n")

  if setup:
    setup()

  while True:
    try:
      if auto_lock_interrupts:
        for interrupt_instance in HardwareInterrupt.INSTANCES:
          interrupt_instance.lock()

      callback()

      if auto_lock_interrupts:
        for interrupt_instance in HardwareInterrupt.INSTANCES:
          interrupt_instance.unlock()

      sleep_ms(delay_ms)
    except KeyboardInterrupt:
      break

  if cleanup:
    cleanup()

  print("\n\nFinished.")