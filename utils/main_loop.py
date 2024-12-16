from asyncio import gather, run, sleep as async_sleep
from time import sleep_ms

class MainLoop:
  """ A utility class for running a main event loop. """

  __iterations: int = 0
  __keyboard_interrupt: bool = False
  __running: bool = False

  @staticmethod
  def run(callback, delay_ms = 100, *, setup = None, cleanup = None):
    """
    Executes a given callback function on a main event loop.
    The main event loop iterates indefinitely until a `KeyboardInterrupt` occurs.

    Args:
      callback: The callback function to execute. Takes a single argument, the iteration count.
      delay_ms: An optional delay in milliseconds between each iteration of the main event loop. Defaults to `100`.
      setup: An optional setup callback function that will execute code before the main loop initializes. Defaults to `None`.
      cleanup: An optional cleanup callback function that will execute once the main loop completes. Defaults to `None`.
    """
    if MainLoop.running():
      raise RuntimeError("MainLoop is already running.")
    MainLoop.__running = True

    try:
      if setup:
        setup()

      while True:
        try:
          callback(MainLoop.iterations())
        except TypeError:
          callback()

        MainLoop.__iterations += 1
        if delay_ms > 0:
          sleep_ms(delay_ms)
    except KeyboardInterrupt:
      MainLoop.__keyboard_interrupt = True
    finally:
      if cleanup:
        cleanup()

  @staticmethod
  def run_async(async_coroutines: list, delay_ms = 100, *, setup = None, cleanup = None):
    """
    Executes given async Coroutines on a main asyncio event loop.
    The main event loop iterates indefinitely until a `KeyboardInterrupt` occurs.

    Args:
      async_coroutines: The async Coroutines to execute. Each Coroutine should take a single argument, the iteration count.
      delay_ms: An optional delay in milliseconds between each iteration of each coroutine. Defaults to `100`.
      setup: An optional setup callback function that will execute code before the main loop initializes. Defaults to `None`.
      cleanup: An optional cleanup callback function that will execute once the main loop completes. Defaults to `None`.
    """
    if MainLoop.running():
      raise RuntimeError("MainLoop is already running.")
    MainLoop.__running = True

    try:
      if setup:
        setup()

      async def main():
        async_loops = map(lambda c: MainLoop.__async_loop(c, delay_ms) if callable(c) else c, async_coroutines)
        await gather(*async_loops)

      run(main()) # Setup main asyncio event loop.
    except KeyboardInterrupt:
      MainLoop.__keyboard_interrupt = True
    finally:
      if cleanup:
        cleanup()

  @staticmethod
  async def __async_loop(callback, delay_ms):
    i = 0

    while True:
      try:
        await callback(i)
      except TypeError:
        await callback()

      i += 1
      if i > MainLoop.__iterations:
        MainLoop.__iterations = i
      await async_sleep(delay_ms / 1000)

  @staticmethod
  def iterations() -> int:
    """
    The number of iterations the main loop has executed.

    For async loops, this is the maximum number of iterations across all coroutines.
    """
    return MainLoop.__iterations

  @staticmethod
  def keyboard_interrupt() -> bool:
    """ Whether a `KeyboardInterrupt` has been raised. """
    return MainLoop.__keyboard_interrupt

  @staticmethod
  def running() -> bool:
    """ Whether the main loop is currently running. """
    return MainLoop.__running
