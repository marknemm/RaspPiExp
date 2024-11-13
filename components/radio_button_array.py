from components.button import Button

class RadioButtonArray:
  """
  An array of radio buttons where only one button can be toggled on at a time

  Args:
    pin_ids: A list containing Pin IDs from which to initialize `Button` objects
  """

  def __init__(self, pin_ids: list[int]):
    self.__buttons = list(map(lambda pin_id: Button(pin_id), pin_ids))
    self.__sel_idx = None

  @property
  def len(self) -> int:
    """ The length of the button array """
    return len(self.__buttons)

  @property
  def sel_idx(self) -> int | None:
    """ The selected button's 0-based index in the array """

    try:
      self.__sel_idx = next((i for (i, button) in enumerate(self.__buttons) if button.state))
    except StopIteration:
      pass

    self.__prep_button_states()

    return self.__sel_idx


  @sel_idx.setter
  def sel_idx(self, value: int | None):
    if value is not None and (value < 0 or value >= self.len):
      raise IndexError(f"Index out of bounds for RadioButtonArray with length {self.len}: {value}")

    self.__sel_idx = value
    self.__prep_button_states()

  def reset(self):
    """ Resets the button array by unselecting any selected button """
    self.__sel_idx = None

  def __prep_button_states(self):
    """ Prepares the buttons in the array so the next selection may be read """
    for button in self.__buttons:
      button.state = False
