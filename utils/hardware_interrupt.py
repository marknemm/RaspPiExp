from utils.debounce import debounce
from utils.interrupt_mutex import InterruptMutex

class HardwareInterrupt:
  """
  A container for hardware interrupt functionality.
  """

  INSTANCES: list['HardwareInterrupt'] = []
  """
  Keep track of all initialized `HardwareInterrupt` instances
  so that they may be easily referenced by the main event loop.
  """

  def __init__(self, handler = None):
    """
    Args:
      handler: An optional default handler function for the hardware interrupt. Takes no arguments.
    """
    self.__registered_interrupt_handlers = []
    self.__mutex = InterruptMutex()

    @self.__mutex.bind
    def handle_interrupt(*args, **kwargs):
      for handler in self.__registered_interrupt_handlers:
        handler()
    self.__handle_interrupt = handle_interrupt

    if handler:
      self.handler(handler)

    HardwareInterrupt.INSTANCES.append(self)

  def __del__(self):
    HardwareInterrupt.INSTANCES.remove(self)

  @property
  def mutex(self) -> InterruptMutex:
    """
    A mutex used to lock the hardware interrupt's handler callback(s) to prevent race conditions.

    Use `mutex.lock()` to lock this `HardwareInterrupt`. When locked,
    any interrupts will cease to immediately invoke registered handler callbacks.

    Use `mutex.unlock()`to unlock this `HardwareInterrupt`. When unlocked,
    all callbacks that were blocked due to the lock will immediately be executed.
    """
    return self.__mutex

  def listener(self, debounce_ms = 150):
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
    return debounce(self.__handle_interrupt, debounce_ms)

  def handler(self, handler):
    """
    Annotation to register a hardware interrupt handler function
    that will be invoked each time this interrupt occurs.

    Args:
      handler: The hardware interrupt handler function to register.

    Returns:
      The registered hardware interrupt handler function.
    """
    if handler not in self.__registered_interrupt_handlers:
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

  def lock(self):
    """
    Locks this `HardwareInterrupt`, preventing all interrupt handlers
    from being invoked until `unlock` is invoked.
    """
    self.__mutex.lock()

  def unlock(self):
    """
    Unlocks this `HardwareInterrupt`, immediately invoking all interrupt handlers
    that were blocked between the previous call to `lock` and this call to `unlock`.
    """
    self.__mutex.unlock()
