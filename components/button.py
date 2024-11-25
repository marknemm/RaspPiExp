from machine import Pin
from utils.hardware_interrupt import HardwareInterrupt
from utils.interrupt_mutex import InterruptMutex

class Button():
  """
  A press Button controlled by Pin input with internal pull up resistor.
  Keeps track of the 'toggle' state based on the sequence of previous button presses.
  """

  def __init__(self, pin_id, init_toggle_state = False):
    """
    Args:
      pin_id: The ID of the Pin that will record the toggle state of the button.
      init_toggle_state: The optional initial toggle state of the button; defaults to `False`.
    """
    self.__button_pin = Pin(pin_id, Pin.IN, Pin.PULL_UP)
    self.__toggle_state = init_toggle_state

    self.__press_interrupt = HardwareInterrupt()
    self.__release_interrupt = HardwareInterrupt(self.toggle)

    self.__button_pin.irq(self.__press_interrupt.listener(), Pin.IRQ_FALLING)
    self.__button_pin.irq(self.__release_interrupt.listener(), Pin.IRQ_RISING)

  @property
  def pressed(self) -> bool:
    """ The current pressed state of the button. """
    return self.__button_pin.value() == 0

  @property
  def toggle_state(self) -> bool:
    """ The current toggle state of the button. """
    return self.__toggle_state

  @property
  def press_interrupt(self) -> HardwareInterrupt:
    """ The `HardwareInterrupt` associated with button presses. """
    return self.__press_interrupt

  @property
  def press_mutex(self) -> InterruptMutex:
    """
    An `InterruptMutex` for locking the press `HardwareInterrupt` handler
    in order to prevent races with the main event loop.
    """
    return self.press_interrupt.mutex

  @property
  def release_interrupt(self) -> HardwareInterrupt:
    """ The `HardwareInterrupt` associated with button releases. """
    return self.__release_interrupt

  @property
  def release_mutex(self) -> InterruptMutex:
    """
    An `InterruptMutex` for locking the release `HardwareInterrupt` handler
    in order to prevent races with the main event loop.
    """
    return self.release_interrupt.mutex

  @toggle_state.setter
  def toggle_state(self, value: bool):
    self.__toggle_state = value

  def toggle(self) -> bool:
    """
    Toggles the button toggle state.

    Returns:
      The resulting toggle state of the button.
    """
    self.__toggle_state = not self.__toggle_state
    return self.__toggle_state

  def press_handler(self, func):
    """
    Annotation to register a button press hardware interrupt handler function
    that will be invoked each time the button is pressed.

    Args:
      handler: The hardware interrupt handler function to register.

    Returns:
      The registered hardware interrupt handler function.
    """
    return self.__press_interrupt.handler(func)

  def release_handler(self, func):
    """
    Annotation to register a button release hardware interrupt handler function
    that will be invoked each time the button is released.

    Args:
      handler: The hardware interrupt handler function to register.

    Returns:
      The registered hardware interrupt handler function.
    """
    return self.__release_interrupt.handler(func)
