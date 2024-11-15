from components.button import Button

class RadioButtonArray:
  """
  An array of radio buttons where only one button can be toggled on at a time

  Args:
    pin_ids: A list containing Pin IDs from which to initialize `Button` objects
  """

  def __init__(self, pin_ids: list[int]):
    self.__buttons = list(map(Button, pin_ids))
    self.__registered_sel_handlers = []
    self.__sel_idx = None

    for i, button in enumerate(self.__buttons):
      button.register_release_handler(
        lambda button_idx = i: # capture current value of i
          self.__handle_button_release(button_idx))

    self.register_sel_handler(self.__handle_button_release)

  @property
  def len(self) -> int:
    """ The length of the button array """
    return len(self.__buttons)

  @property
  def sel_idx(self) -> int | None:
    """ The selected button's 0-based index in the array """
    return self.__sel_idx

  @sel_idx.setter
  def sel_idx(self, value: int | None):
    if value is not None and (value < 0 or value >= self.len):
      raise IndexError(f"Index out of bounds for RadioButtonArray with length {self.len}: {value}")

    self.__sel_idx = value

  @property
  def sel_interrupt(self):
    """
    Whether a hardware interrupt has occurred during the
    current iteration of the main event loop resulting in a new button selection.
    """
    for button in self.__buttons:
      if button.release_interrupt:
        return True
    return False

  def append(self, pin_id: int):
    """
    Appends a button to the radio button array.

    Args:
      pin_id: The Pin ID from which to initialize the new button.
    """
    self.__buttons.append(Button(pin_id))

  def insert(self, pin_id: int, idx: int):
    """
    Inserts a button at a given index in the radio button array.

    Args:
      pin_id: The Pin ID from which to initialize the new button.
      idx: The index at which to insert the new button.
    """
    self.__buttons.insert(idx, Button(pin_id))

  def remove(self, idx: int):
    """
    Removes a button at a given index in the radio button array.
    Deselects the button if it was selected, leaving no button selected.

    Args:
      idx: The index at which to remove the button.
    """
    self.__buttons.remove(self.__buttons[idx])
    if self.sel_idx == idx:
      self.reset()

  def reset(self):
    """ Resets the button array by unselecting any selected button """
    self.__sel_idx = None

  def register_sel_handler(self, handler):
    """
    Registers a button select hardware interrupt handler
    that is invoked whenever a new button is selected.

    The handler should accept the 0-based int index of the selected button as its single argument.

    Args:
      handler: The button select hardware interrupt handler to register.
    """
    if handler not in self.__registered_sel_handlers:
      self.__registered_sel_handlers.append(handler)


  def unregister_sel_handler(self, handler):
    """
    Unregisters a button select hardware interrupt handler
    so it is no  longer invoked whenever a new button is selected.

    Args:
      handler: The button select hardware interrupt handler to unregister.
    """
    if handler in self.__registered_sel_handlers:
      self.__registered_sel_handlers.remove(handler)

  def __handle_button_release(self, idx: int):
    """
    Internally handles button release hardware interrupt events.

    Args:
      idx: The 0-based index of the button that was released.
    """
    if self.sel_idx != idx:
      self.sel_idx = idx
      for handler in self.__registered_sel_handlers:
        handler(self.sel_idx)
