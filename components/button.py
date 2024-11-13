from machine import Pin


class Button:
  """
  A toggle Button controlled by Pin input with internal pull up resistor

  Args:
    pin_id: The ID of the MCU pin that will record the toggle state of the button
    init_state: The optional initial state of the button; defaults to `False`
  """

  def __init__(self, pin_id, init_state = False):
    self.__button_pin = Pin(pin_id, Pin.IN, Pin.PULL_UP)
    self.__state = init_state
    self.__prev_volt = None

  @property
  def state(self) -> bool:
    """ The current toggle state of the button """
    if self.__prev_volt == 1 and self.__button_pin.value() == 0:
      self.__state = not self.__state
    self.__prev_volt = self.__button_pin.value()
    return self.__state

  @state.setter
  def state(self, value: bool):
    self.__state = value
