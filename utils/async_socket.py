from asyncio import sleep as async_sleep
from socket import socket

class AsyncSocket(socket):
  """
  Create a new socket using the given address family, socket type and protocol number.
  This socket will have async functionality in addition to the base sync functionality.

  Note that specifying proto in most cases is not required
  (and not recommended, as some MicroPython ports may omit IPPROTO_* constants).
  Instead, type argument will select needed protocol automatically:

  ### Create STREAM TCP socket
  socket(AF_INET, SOCK_STREAM)
  ### Create DGRAM UDP socket
  socket(AF_INET, SOCK_DGRAM)

  Extends:
    socket
  """

  def __init__(self, *argv, **kwargs):
    super().__init__(*argv, **kwargs)
    self.__timeout: int | None = None

  @property
  def blocking(self) -> bool:
    """ Wether this socket's sync recvfrom calls have been set to blocking. """
    return self.__timeout is None

  @property
  def timeout(self) -> int | None:
    """
    The timeout in seconds on blocking socket operations (e.g. `recvfrom`).
    Can be a nonnegative floating point number, or `None`.

    If a non-zero value, subsequent socket operations will raise an `OSError` exception
    if the timeout period value has elapsed before the operation has completed.

    If zero, the socket is in non-blocking mode. If `None`, the socket is in blocking mode.
    """
    return self.__timeout

  def settimeout(self, value: int | None):
    super().settimeout(value)
    self.__timeout = value

  async def async_recvfrom(self, bufsize: int, async_sleep_ms = 100):
    """
    Receive data from the socket in a non-blocking async manner.

    Args:
      bufsize: The size of the bytes message buffer.

    Returns:
      An `AsyncGenerator` yielding a pair (bytes, address) where bytes is a bytes object
      representing the data received and address is the address of the socket sending the data.
    """
    recv_data = None

    while not recv_data:
      try:
        timeout = self.__timeout
        if timeout is None:
          self.setblocking(False)

        recv_data = self.recvfrom(bufsize)

        if timeout is not None:
          self.settimeout(timeout)
      except OSError:
        pass # Nothing received from the socket.
      finally:
        await async_sleep(async_sleep_ms / 1000) # Sleep and yield control to main event loop.

    return recv_data
