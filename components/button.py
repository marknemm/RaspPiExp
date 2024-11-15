from machine import Pin
from utils.hardware_interrupt import HardwareInterrupt

class Button():
  """
  A press Button controlled by Pin input with internal pull up resistor.
  Keeps track of the 'toggle' state based on the sequence of previous button presses.

  Args:
    pin_id: The ID of the MCU pin that will record the toggle state of the button.
    init_toggle_state: The optional initial toggle state of the button; defaults to `False`.
  """

  def __init__(self, pin_id, init_toggle_state = False):
    self.__button_pin = Pin(pin_id, Pin.IN, Pin.PULL_UP)
    self.__toggle_state = init_toggle_state

    self.__press_interrupt = HardwareInterrupt()
    self.__release_interrupt = HardwareInterrupt(self.toggle)

    self.__button_pin.irq(self.__press_interrupt.gen_listener(), Pin.IRQ_FALLING)
    self.__button_pin.irq(self.__release_interrupt.gen_listener(), Pin.IRQ_RISING)

  @property
  def pressed(self) -> bool:
    """ The current pressed state of the button. """
    return self.__button_pin.value() != 0

  @property
  def toggle_state(self) -> bool:
    """ The current toggle state of the button. """
    return self.__toggle_state

  @property
  def press_interrupt(self) -> bool:
    """ Whether or not a button press hardware interrupt has occurred during the current iteration of the main event loop. """
    return self.__press_interrupt.interrupt

  @property
  def release_interrupt(self) -> bool:
    """ Whether or not a button release hardware interrupt has occurred during the current iteration of the main event loop. """
    return self.__release_interrupt.interrupt

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

  def register_press_handler(self, handler):
    """
    Registers a button press hardware interrupt handler
    which will be invoked on each button press.

    Args:
      handler: The button press hardware interrupt handler function.
    """
    self.__press_interrupt.register_handler(handler)

  def unregister_press_handler(self, handler):
    """
    Unregisters a button press hardware interrupt handler
    so that it will no longer be invoked on each button press.

    Args:
      handler: The button press hardware interrupt handler function.
    """
    self.__press_interrupt.unregister_handler(handler)

  def register_release_handler(self, handler):
    """
    Registers a button release hardware interrupt handler
    which will be invoked on each button release.

    Args:
      handler: The button release hardware interrupt handler function.
    """
    self.__release_interrupt.register_handler(handler)

  def unregister_release_handler(self, handler):
    """
    Unregisters a button release hardware interrupt handler
    so that it will no longer by invoked on each button press.

    Args:
      handler: The button release hardware interrupt handler function.
    """
    self.__release_interrupt.unregister_handler(handler)
