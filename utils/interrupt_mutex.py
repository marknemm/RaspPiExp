class InterruptMutex:
  """
  A mutex lock for preventing multiple simultaneous invocations
  of a function shared by the main event loop and hardware interrupts.

  Can be bound to a method via decorator or by manually invoking `bind`.
  """

  def __init__(self, discard_duplicates = False, manual = False):
    """
    Args:
      discard_duplicates: Whether to discard all duplicate blocked calls to the bound function when locked. Only the last call will be kept. Defaults to `False`.
      manual: Whether `lock` and `unlock` must be manually called; disables the automatic locking mechanism on the bound function's invocation. Defaults to `False`.
    """
    self.discard_duplicates = discard_duplicates
    self.manual = manual
    self.__locked = False
    self.__blocked_invocations = []

  def __call__(self, func):
    return self.bind(func)

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

  def bind(self, func, discard_duplicates: bool | None = None, manual: bool | None = None):
    """
    Binds this mutex to a given function.

    It will only allow one invocation of the bound function at a time by
    blocking any invocation of the function by a hardware interrupt when
    the main event loop is in the process of invoking it.

    Any attempts to invoke the bound function by a hardware interrupt while
    being invoked by the main event loop will be queued for immediate sequential
    invocation after the main event loop exists the function.

    Args:
      func: The function to bind the mutex lock to.
      discard_duplicates: Whether to discard all duplicate blocked calls to `func` when locked. Only the last call will be kept. Defaults to `self.discard_duplicates`.
      manual: Whether `lock` and `unlock` must be manually called; disables the automatic locking mechanism on `func` invocation. Defaults to `self.manual`.

    Returns:
      The input `func` controlled by this mutex lock.
    """
    if discard_duplicates is None:
      discard_duplicates = self.discard_duplicates
    if manual is None:
      manual = self.manual

    def wrapper(*args, **kwargs):
      if self.locked:
        if discard_duplicates:
          self.__blocked_invocations.clear()
        self.__blocked_invocations.append(lambda: func(*args, **kwargs))
      elif not manual:
        with self:
          func(*args, **kwargs)
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
    while self.__blocked_invocations:
      handler = self.__blocked_invocations.pop(0)
      handler()
    self.__locked = False # Important to do this last so additional interrupts don't interrupt queued blocked invocations during unlock.
