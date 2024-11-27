from utils.debounce import debounce
from utils.interrupt_mutex import InterruptMutex

class InterruptListener:
  """
  A hardware interrupt listener that listens for interrupts and invokes all registered handlers using a debounce delay.

  Also, optionally enforces only one execution of a handler function at a time using an `InterruptMutex`.
  """

  def __init__(self, handler = None):
    """
    Args:
      handler: An optional default handler function for the hardware interrupt. Takes no arguments.
    """
    self.__registered_interrupt_handlers = []
    self.__mutex = InterruptMutex()

    if handler:
      self.handler(handler)

  @property
  def mutex(self) -> InterruptMutex:
    """
    A mutex used to lock the hardware interrupt's handler callback(s) registered using
    the `with_mutex` flag set to `True.

    The mutex will prevent race conditions by auto-locking whenever the registered
    handler callbacks are entered, and auto-unlocking upon exit.

    Use `mutex.lock()` to manually lock this `HardwareInterrupt`. When locked,
    any interrupts will cease to immediately invoke registered handler callbacks.

    Use `mutex.unlock()`to manually unlock this `HardwareInterrupt`. When unlocked,
    all callbacks that were blocked due to the lock will immediately be executed.

    Be cautious to avoid causing deadlocks by manually invoking lock/unlock.
    """
    return self.__mutex

  def listen(self, debounce_ms = 150):
    """
    Generates an interrupt listener callback function that
    should be bound to a specific hardware component's interrupt signal.

    The interrupt listener callback will internally debounce all interrupts,
    set the interrupt flag, and invoke any registered interrupt handler functions.

    Args:
      debounce_ms: An optional number of milliseconds to debounce handling of the hardware interrupt. The hardware interrupt will only be handled once `debounce_ms` has elapsed since the last interrupt. Defaults to `150`.

    Returns:
      This `HardwareInterrupt` instance.
    """
    def invoke_registered_handlers(*args, **kwargs):
      for registered_handler in self.__registered_interrupt_handlers:
        registered_handler()

    return debounce(invoke_registered_handlers, debounce_ms)

  def handler(self, with_mutex = False):
    """
    Generates a function decorator that can be used to register a
    hardware interrupt handler function that will be invoked each time this interrupt is triggered.

    Args:
      with_mutex: Whether or not to control access to the handler function with a mutex (lock). Defaults to `False`.

    Returns:
      The function decorator for marking a decorated function as a hardware interrupt handler.
    """
    return lambda handler: self.register_handler(handler, with_mutex)

  def register_handler(self, handler, with_mutex = False):
    """
    Registers a hardware interrupt handler function
    that will be invoked each time this interrupt is triggered.

    Args:
      handler: The hardware interrupt handler function to register.
      with_mutex: Whether or not to control access to the handler function with a mutex (lock). Defaults to `False`.

    Returns:
      The registered hardware interrupt handler function.
      If `with_mutex` was set to `True` the function will be wrapped in a mutex that
      only allows one invocation to process at a time.
    """
    if handler not in self.__registered_interrupt_handlers:
      if with_mutex:
        handler = self.mutex.bind(handler)
      self.__registered_interrupt_handlers.append(handler)

    return handler

  def unregister_handler(self, handler):
    """
    Unregisters a hardware interrupt handler function so that it
    will no longer be invoked upon each interrupt.

    Args:
      handler: The hardware interrupt handler function to unregister.
    """
    if handler in self.__registered_interrupt_handlers:
      self.__registered_interrupt_handlers.remove(handler)
