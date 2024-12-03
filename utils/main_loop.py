from asyncio import gather, run, sleep as async_sleep
from utime import sleep_ms

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
  try:
    if setup:
      setup()

    while True:
      callback()
      if delay_ms > 0:
        sleep_ms(delay_ms)
  except KeyboardInterrupt:
    pass
  finally:
    if cleanup:
      cleanup()

def main_async_loop(async_coroutines: list, delay_ms = 100, setup = None, cleanup = None):
  """
  Executes given async Coroutines on a main asyncio event loop.
  The main event loop iterates indefinitely until a `KeyboardInterrupt` occurs.

  Args:
    async_coroutines: The async Coroutines to execute.
    delay_ms: An optional delay in milliseconds between each iteration of each coroutine. Defaults to `100`.
    setup: An optional setup callback function that will execute code before the main loop initializes. Defaults to `None`.
    cleanup: An optional cleanup callback function that will execute once the main loop completes. Defaults to `None`.
  """
  try:
    if setup:
      setup()

    async def async_loop(cb):
      while True:
        await cb()
        await async_sleep(0.1)

    async def main():
      async_loops = map(lambda c: async_loop(c) if callable(c) else c, async_coroutines)
      await gather(*async_loops)

    run(main()) # Setup main asyncio event loop.
  except KeyboardInterrupt:
    pass
  finally:
    if cleanup:
      cleanup()
