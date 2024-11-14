from machine import Pin

from utils.debounce import debounce

class Button:
  """
  A toggle Button controlled by Pin input with internal pull up resistor.

  Args:
    pin_id: The ID of the MCU pin that will record the toggle state of the button.
    init_state: The optional initial state of the button; defaults to `False`.
  """

  def __init__(self, pin_id, init_state = False):
    self.__button_pin = Pin(pin_id, Pin.IN, Pin.PULL_UP)
    self.__state = init_state
    handle_press = debounce(self.__handle_press, 150)
    self.__button_pin.irq(handle_press, Pin.IRQ_RISING)
    self.__registered_interrupt_handlers = []

  @property
  def state(self) -> bool:
    """ The current toggle state of the button. """
    return self.__state

  @state.setter
  def state(self, value: bool):
    self.__state = value

  def toggle(self) -> bool:
    """
    Toggles the button state.

    Returns:
      The resulting state of the button.
    """
    self.__state = not self.__state
    return self.__state

  def register_interrupt_handler(self, handler):
    """
    Registers a button press interrupt handler function that will be invoked upon each button press.

    Args:
      handler: The button press interrupt handler function to register. Will be passed the current state of the button.
    """
    if handler not in self.__registered_interrupt_handlers:
      self.__registered_interrupt_handlers.append(handler)

  def unregister_interrupt_handler(self, handler):
    """
    Unregisters a button press interrupt handler function so that it will no longer be invoked upon each button press.

    Args:
      handler: The button press interrupt handler function to unregister.
    """
    if handler in self.__registered_interrupt_handlers:
      self.__registered_interrupt_handlers.remove(handler)

  def __handle_press(self, _: Pin):
    """ Handles the Pin hardware interrupt resulting from the button press. """
    self.toggle()
    for handler in self.__registered_interrupt_handlers:
      handler(self.state)
