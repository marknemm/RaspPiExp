from machine import Pin
from utils.interrupt_listener import InterruptListener

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

    self.__press_listener = InterruptListener()
    self.__release_listener = InterruptListener(self.toggle)

    self.__button_pin.irq(self.__press_listener.listen(), Pin.IRQ_FALLING)
    self.__button_pin.irq(self.__release_listener.listen(), Pin.IRQ_RISING)

    self.press_handler = self.__press_listener.handler
    self.release_handler = self.__release_listener.handler

  @property
  def pressed(self) -> bool:
    """ The current pressed state of the button. """
    return self.__button_pin.value() == 0

  @property
  def toggle_state(self) -> bool:
    """ The current toggle state of the button. """
    return self.__toggle_state

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
