from network import WLAN, STA_IF
from time import sleep_ms, ticks_ms, ticks_diff

class WiFi(WLAN):
  """
  Utility for connecting to a `WLAN` Wi-Fi network.

  Extends:
    WLAN
  """

  __CONNECTIONS: dict[str, 'WiFi'] = {}

  def __del__(self):
    WiFi.__CONNECTIONS.pop(self.config('ssid'))
    self.active(False)

  def __enter__(self):
    self.active(True)

  def __exit__(self, exc_type, exc_value, traceback):
    self.active(False)
    return False # Propagate any raised exceptions.

  @staticmethod
  def init(
    ssid: str,
    key: str | None = None,
    *,
    bssid: str | None = None,
    non_blocking = False,
    timeout_ms = 10000
  ) -> 'WiFi':
    """
    Initializes a singleton `WiFi` instance, activates it, and uses it to connect this device to the WLAN.
    If a `WiFi` instance has been previously initialized for the associated access point, then re-uses it.

    Args:
      ssid: The service set identifier or Wi-Fi username.
      key: The Wi-Fi password key associated with the `ssid`. Defaults to `None`.
      bssid: The basic service set identifier used to differentiate multiple access points on the same network. Defaults to `None`.
      non_blocking: Optionally set to `True` in order to not have this method block while waiting for a connection to an access point on the LAN. Defaults to `False`.
      timeout_ms: An optional timeout value in milliseconds that determines the max amount of time this method may block for while waiting for a connection to an access point on the LAN.

    Raises:
      TimeoutError: Raised if `timeout_ms` elapses while waiting for a connection to an access point on the LAN.

    Returns:
      WiFi: The created `WiFi` instance.
    """
    return WiFi.__CONNECTIONS.get(ssid) or WiFi(STA_IF).connect(ssid, key, bssid = bssid, non_blocking = non_blocking, timeout_ms = timeout_ms)

  def connect(
    self,
    ssid: str | None = None,
    key: str | None = None,
    *,
    bssid: str | None = None,
    non_blocking = False,
    timeout_ms = 30000
  ) -> 'WiFi':
    """
    Connects this device to WLAN Wi-Fi. Implicitly invokes `active(True)` before forming the connection.

    Args:
      ssid: The service set identifier or Wi-Fi username. Defaults to `None`.
      key: The Wi-Fi password key associated with the `ssid`. Defaults to `None`.
      bssid: The basic service set identifier used to differentiate multiple access points on the same network. Defaults to `None`.
      non_blocking: Optionally set to `True` in order to not have this method block while waiting for a connection to an access point on the LAN. Defaults to `False`.
      timeout_ms: An optional timeout value in milliseconds that determines the max amount of time this method may block for while waiting for a connection to an access point on the LAN.

    Raises:
      TimeoutError: Raised if `timeout_ms` elapses while waiting for a connection to an access point on the LAN.

    Returns:
      WiFi: This `WiFi` instance.
    """
    self.active(True)
    super().connect(ssid, key, bssid = bssid)

    start_tick = ticks_ms()

    if not non_blocking:
      while not self.isconnected():
        sleep_ms(10)
        if ticks_diff(ticks_ms(), start_tick) >= timeout_ms:
          raise RuntimeError(f"Could not connect to Wi-Fi using ssid {ssid} within {timeout_ms}ms.")

    WiFi.__CONNECTIONS[self.config('ssid')] = self
    return self

  @property
  def ip_address(self) -> str:
    """ The IP address bound to this device on the LAN. """
    return self.ifconfig()[0]


if __name__ == '__main__':
  wifi = WiFi.init('MySpectrumWiFi43-2G', 'famousgate426')
  with wifi:
    print('Connected: ', wifi.ip_address)
