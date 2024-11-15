from utils.debounce import debounce

class HardwareInterrupt:
  """
  A container for hardware interrupt functionality.

  Args:
    handler: An optional default handler function for the hardware interrupt. Takes no arguments.
  """

  def __init__(self, handler = None):
    self.__interrupt = False
    self.__registered_interrupt_handlers = []

    if handler:
      self.register_handler(handler)

    HARDWARE_INTERRUPT_INSTANCES.append(self)

  @property
  def interrupt(self) -> bool:
    """
    Whether or not this hardware interrupt has occurred
    during the current iteration of the main event loop.
    """
    return self.__interrupt

  def gen_listener(self, handler = None, debounce_ms = 100):
    """
    Generates an interrupt listener callback function that
    should be bound to a specific hardware component's interrupt signal.

    The interrupt listener callback will internally debounce all interrupts,
    set the interrupt flag, and invoke any registered interrupt handler functions.

    Args:
      handler: An optional default handler function for the hardware interrupt. Takes no arguments.
      debounce_ms: An optional number of milliseconds to debounce handling of the hardware interrupt. The hardware interrupt will only be handled once `debounce_ms` has elapsed since the last interrupt. Defaults to `100`.

    Returns:
      This `HardwareInterrupt` instance.
    """
    if handler:
      self.register_handler(handler)

    return debounce(self.__handle_interrupt, debounce_ms)

  def __handle_interrupt(self, *args, **kwargs):
    """
    Main hardware interrupt handler callback that shall perform default setup and teardown
    surrounding calls to all registered interrupt handlers.
    Will also apply any configured `debounce_ms` which defaults to 100 milliseconds.
    """
    self.clear_interrupt() # Clear interrupt flag so that the interrupt handler doesn't encounter it and bail
    for handler in self.__registered_interrupt_handlers:
      handler()
    self.__interrupt = True # Set interrupt flag so that main event loop and other handlers don't race

  def clear_interrupt(self):
    """
    Clears the `interrupt` flag to designate that this hardware interrupt
    has not occurred during the current iteration of the main event loop.
    """
    self.__interrupt = False

  def register_handler(self, handler):
    """
    Registers a hardware interrupt handler function that
    will be invoked each time this interrupt occurs.

    Args:
      handler: The hardware interrupt handler function to register. The function takes no arguments.
    """
    if handler not in self.__registered_interrupt_handlers:
      self.__registered_interrupt_handlers.append(handler)

  def unregister_handler(self, handler):
    """
    Unregisters a hardware interrupt handler function so that it
    will no longer be invoked upon each interrupt.

    Args:
      handler: The hardware interrupt handler function to unregister.
    """
    if handler in self.__registered_interrupt_handlers:
      self.__registered_interrupt_handlers.remove(handler)

HARDWARE_INTERRUPT_INSTANCES: list[HardwareInterrupt] = []
