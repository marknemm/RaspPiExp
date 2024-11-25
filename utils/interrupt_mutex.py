class InterruptMutex:
  """ A mutex lock for preventing bound function invocations within the context of hardware interrupts. """

  def __init__(self):
    self.__locked = False
    self.__blocked_interrupt_handlers = []

  def __enter__(self):
    self.lock()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.unlock()
    return False # Propagate any raised exceptions.

  @property
  def locked(self) -> bool:
    """ The current locked state of the mutex. """
    return self.__locked

  def bind(self, func):
    """
    Binds this mutex to a given function.

    It will prevent it from being invoked if the `locked` state is `True`,
    and will immediately invoke any prevented function calls once the mutex is unlocked.

    Can be used as an annotation on a function or called directly.

    Args:
      func: The function to bind the mutex lock to.

    Returns:
      The input `func` controlled by this mutex lock.
    """
    def wrapper(*args, **kwargs):
      if self.locked:
        self.__blocked_interrupt_handlers.append(lambda: func(*args, **kwargs))
      else:
        func(*args, **kwargs)

    return wrapper

  def lock(self):
    """
    Locks this mutex preventing any calls to bound functions via the `bind` method or annotation
    from immediately evaluating, and queues the function calls for later evaluation once
    the mutex is unlocked via `unlock`.
    """
    self.__locked = True

  def unlock(self):
    """
    Unlocks this mutex which immediately invokes any blocked function calls to bound functions
    in the order that they occurred while locked.
    """
    while self.__blocked_interrupt_handlers:
      handler = self.__blocked_interrupt_handlers.pop(0)
      handler()
    self.__locked = False # Important to do this last so additional interrupts don't interrupt queued interrupts during unlock.
