import struct
from micropython import const
from bluetooth import UUID, BLE as _BLE
from bluetooth import *
from utils.main_loop import MainLoop

BVE_ADV_TYPE_FLAGS = const(0x01)
BVE_ADV_TYPE_NAME = const(0x09)
BVE_ADV_TYPE_UUID16_COMPLETE = const(0x3)
BVE_ADV_TYPE_UUID32_COMPLETE = const(0x5)
BVE_ADV_TYPE_UUID128_COMPLETE = const(0x7)
BVE_ADV_TYPE_APPEARANCE = const(0x19)

BLE_APPEARANCE_UNKNOWN = const(0)
BLE_APPEARANCE_GENERIC_PHONE = const(64)
BLE_APPEARANCE_GENERIC_COMPUTER = const(128)
BLE_APPEARANCE_GENERIC_WATCH = const(192)
BLE_APPEARANCE_WATCH_SPORTS_WATCH = const(193)
BLE_APPEARANCE_GENERIC_CLOCK = const(256)
BLE_APPEARANCE_GENERIC_DISPLAY = const(320)
BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)
BLE_APPEARANCE_GENERIC_EYE_GLASSES = const(448)
BLE_APPEARANCE_GENERIC_TAG = const(512)
BLE_APPEARANCE_GENERIC_KEYRING = const(576)
BLE_APPEARANCE_GENERIC_MEDIA_PLAYER = const(640)
BLE_APPEARANCE_GENERIC_BARCODE_SCANNER = const(704)
BLE_APPEARANCE_GENERIC_THERMOMETER = const(768)
BLE_APPEARANCE_THERMOMETER_EAR = const(769)
BLE_APPEARANCE_GENERIC_HEART_RATE_SENSOR = const(832)
BLE_APPEARANCE_HEART_RATE_SENSOR_HEART_RATE_BELT = const(833)
BLE_APPEARANCE_GENERIC_BLOOD_PRESSURE = const(896)
BLE_APPEARANCE_BLOOD_PRESSURE_ARM = const(897)
BLE_APPEARANCE_BLOOD_PRESSURE_WRIST = const(898)
BLE_APPEARANCE_GENERIC_HID = const(960)
BLE_APPEARANCE_HID_KEYBOARD = const(961)
BLE_APPEARANCE_HID_MOUSE = const(962)
BLE_APPEARANCE_HID_JOYSTICK = const(963)
BLE_APPEARANCE_HID_GAMEPAD = const(964)
BLE_APPEARANCE_HID_DIGITIZER_TABLET = const(965)
BLE_APPEARANCE_HID_CARD_READER = const(966)
BLE_APPEARANCE_HID_DIGITAL_PEN = const(967)
BLE_APPEARANCE_HID_BARCODE_SCANNER = const(968)
BLE_APPEARANCE_GENERIC_GLUCOSE_METER = const(1024)
BLE_APPEARANCE_GENERIC_RUNNING_WALKING_SENSOR = const(1088)
BLE_APPEARANCE_RUNNING_WALKING_SENSOR_IN_SHOE = const(1089)
BLE_APPEARANCE_RUNNING_WALKING_SENSOR_ON_SHOE = const(1090)
BLE_APPEARANCE_RUNNING_WALKING_SENSOR_ON_HIP = const(1091)
BLE_APPEARANCE_GENERIC_CYCLING = const(1152)
BLE_APPEARANCE_CYCLING_CYCLING_COMPUTER = const(1153)
BLE_APPEARANCE_CYCLING_SPEED_SENSOR = const(1154)
BLE_APPEARANCE_CYCLING_CADENCE_SENSOR = const(1155)
BLE_APPEARANCE_CYCLING_POWER_SENSOR = const(1156)
BLE_APPEARANCE_CYCLING_SPEED_AND_CADENCE_SENSOR = const(1157)
BLE_APPEARANCE_GENERIC_PULSE_OXIMETER = const(3136)
BLE_APPEARANCE_PULSE_OXIMETER_FINGERTIP = const(3137)
BLE_APPEARANCE_PULSE_OXIMETER_WRIST_WORN = const(3138)
BLE_APPEARANCE_GENERIC_WEIGHT_SCALE = const(3200)
BLE_APPEARANCE_GENERIC_OUTDOOR_SPORTS_ACTIVITY = const(5184)
BLE_APPEARANCE_OUTDOOR_SPORTS_ACTIVITY_LOCATION_DISPLAY_DEVICE = const(5185)
BLE_APPEARANCE_OUTDOOR_SPORTS_ACTIVITY_LOCATION_AND_NAVIGATION_DISPLAY_DEVICE = const(5186)
BLE_APPEARANCE_OUTDOOR_SPORTS_ACTIVITY_LOCATION_POD = const(5187)
BLE_APPEARANCE_OUTDOOR_SPORTS_ACTIVITY_LOCATION_AND_NAVIGATION_POD = const(5188)

BLE_IRQ_CENTRAL_CONNECT = const(1)
BLE_IRQ_CENTRAL_DISCONNECT = const(2)
BLE_IRQ_GATTS_INDICATE_DONE = const(20)

class BLE(_BLE):
  """
  A class to represent a BLE device.

  Extends:
    BLE: The BLE class from the `bluetooth` module.
  """

  def __init__(self, active = True, *, adv_on_disconnect = True):
    """
    Args:
      active: Whether the BLE device should be active. Defaults to `True`.
      reconnect: Whether automatically restart advertising when a central device disconnects. Defaults to `True`.
    """
    super().__init__()
    self.adv_on_disconnect = adv_on_disconnect
    self.__connections: set[int] = set()
    self.active(active)
    self.irq(self.__handle_connection_events)

  def __del__(self):
    self.stop_advertise()
    self.connections.clear()
    self.active(False)

  def __enter__(self):
    self.active(True)
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.stop_advertise()
    self.active(False)
    return False # Re-raise any exceptions

  @property
  def connections(self) -> set[int]:
    """ The set of connection handles for connected central devices. """
    return self.__connections

  def advertise(
    self,
    name: str | None = None,
    services: list[UUID] | None = None,
    appearance = BLE_APPEARANCE_UNKNOWN,
    *,
    limited_disc = False,
    interval_us: int | None = 500000,
  ):
    """
    Generates a BLE device advertising payload and starts advertising it.

    Will activate the BLE device if not already active.

    Args:
      name: The advertisement name of the BLE device. Defaults to `None`.
      services: The list of service UUIDs associated with the BLE device. Defaults to `None`.
      appearance: The external appearance of the BLE device. Defaults to `BLE_APPEARANCE_UNKNOWN`.
      limited_disc: Whether the device is in limited discoverable mode. In limited mode, will advertise for `30 sec`, and then stops. In general mode, will advertise indefinitely. Defaults to `False` for general mode.
      interval_us: The advertising interval in microseconds rounded down to the nearest `625`. To stop advertising, set to `None`. Defaults to `500000` (500 ms).
    """
    self.active(True)
    adv_data = None
    if name:
      adv_data = advertising_payload(name, services, appearance, limited_disc = limited_disc)
    self.gap_advertise(interval_us, adv_data)

  def stop_advertise(self):
    """ Stops the BLE device advertising. """
    self.gap_advertise(None)

  def broadcast(self, value_handle: int, data: bool | bytes | float | int | str, request_type: str | None = None):
    """
    Broadcasts data to all connected central devices.

    Args:
      value_handle: The service handle to broadcast the data to.
      data: The data to broadcast.
      request_type: The optional type of request to send. Either `notify`, `indicate`, or `None`. Defaults to `None`. If `None`, the data is sent based on the connection's properties.

    Raises:
      ValueError: If the `data` or `request_type` value is invalid.
    """
    formatted_data = format_data(data)
    for conn_handle in self.connections:
      self.send(conn_handle, value_handle, formatted_data, request_type)

  def send(self, conn_handle: int, value_handle: int, data: bool | bytes | float | int | str, request_type: str | None = None):
    """
    Sends data to a connected central device.

    Args:
      conn_handle: The connection handle of the central device.
      value_handle: The value (service) handle to send the data to.
      data: The data to send.
      request_type: The optional type of request to send. Either `notify`, `indicate`, or `None`. Defaults to `None`. If `None`, the data is sent based on the connection's properties.

    Raises:
      ValueError: If the `data` or `request_type` value is invalid.
    """
    self.active(True)
    formatted_data = format_data(data)
    self.gatts_write(value_handle, formatted_data)

    if request_type is None or request_type == 'notify':
      self.gatts_notify(conn_handle, value_handle)

    if request_type is None or request_type == 'indicate':
      self.gatts_indicate(conn_handle, value_handle)

    if request_type not in ('notify', 'indicate', None):
      raise ValueError(f"Invalid request_type value. Must be either 'notify', 'indicate', or `None`. Was given '{request_type}'.")

  def __handle_connection_events(self, event, data):
    """
    Handles BLE connection and disconnection events via interrupts.

    See `BLE.irq()` for more information about the `event` types and associated `data`.

    Args:
      event: The event type.
      data: A tuple containing event specific data.
    """
    if event == BLE_IRQ_CENTRAL_CONNECT:
      print(f"Connected to central device with connection handle: {data[0]}")
      self.connections.add(data[0])
    elif event == BLE_IRQ_CENTRAL_DISCONNECT:
      print(f"Disconnected from central device with connection handle: {data[0]}")
      self.connections.remove(data[0])
      # Start advertising again to allow a new connection.
      if not MainLoop.keyboard_interrupt() and self.adv_on_disconnect:
        self.advertise()

def advertising_payload(
  name: str | None = None,
  services: list[UUID] | None = None,
  appearance = BLE_APPEARANCE_UNKNOWN,
  *,
  limited_disc = False,
) -> bytearray:
  """
  Generate a BLE device advertising payload to be passed to `gap_advertise(adv_data=...)`.

  Args:
    name: The advertisement name of the BLE device. Defaults to `None`.
    services: The list of service UUIDs associated with the BLE device. Defaults to `None`.
    appearance: The external appearance of the BLE device. Defaults to `BLE_APPEARANCE_UNKNOWN`.
    limited_disc: Whether the device is in limited discoverable mode. In limited mode, will advertise for `30 sec`, and then stops. In general mode, will advertise indefinitely. Defaults to `False` for general mode.

  Returns:
    The generated BLE advertising payload to be passed to `gap_advertise(adv_data=...)`.
  """
  payload = bytearray()

  def _append(adv_type: int, value: bytes):
    nonlocal payload
    payload += struct.pack("BB", len(value) + 1, adv_type) + value

  _append(
    BVE_ADV_TYPE_FLAGS,
    struct.pack("B", (0x01 if limited_disc else 0x02) + 0x04),
  )

  if name:
    _append(BVE_ADV_TYPE_NAME, name.encode('utf-8'))

  for uuid in services or []:
    b = bytes(uuid) # type: ignore
    if len(b) == 2:
      _append(BVE_ADV_TYPE_UUID16_COMPLETE, b)
    elif len(b) == 4:
      _append(BVE_ADV_TYPE_UUID32_COMPLETE, b)
    elif len(b) == 16:
      _append(BVE_ADV_TYPE_UUID128_COMPLETE, b)

  if appearance:
    _append(BVE_ADV_TYPE_APPEARANCE, struct.pack("<h", appearance))

  return payload

def decode_field(payload: bytes, adv_type: int) -> list[bytes]:
  """
  Decodes a field in the advertising payload.

  Args:
    payload: The advertising payload to decode the field within.
    adv_type: The type of the field to decode.

  Returns:
    The decoded field from the advertising payload.
  """
  i = 0
  result = []

  while i + 1 < len(payload):
    if payload[i + 1] == adv_type:
      result.append(payload[i + 2 : i + payload[i] + 1])
    i += 1 + payload[i]

  return result

def decode_name(payload: bytes) -> str:
  """
  Decodes the name field in the advertising payload.

  Args:
    payload: The advertising payload to decode the name field within.

  Returns:
    The decoded name from the advertising payload.
  """
  n = decode_field(payload, BVE_ADV_TYPE_NAME)
  return str(n[0], "utf-8") if n else ""

def decode_services(payload: bytes) -> list[UUID]:
  """
  Decodes the services field in the advertising payload.

  Args:
    payload: The advertising payload to decode the services field within.

  Returns:
    The decoded services from the advertising payload.
  """

  services = []

  for u in decode_field(payload, BVE_ADV_TYPE_UUID16_COMPLETE):
    services.append(UUID(struct.unpack("<h", u)[0]))

  for u in decode_field(payload, BVE_ADV_TYPE_UUID32_COMPLETE):
    services.append(UUID(struct.unpack("<d", u)[0]))

  for u in decode_field(payload, BVE_ADV_TYPE_UUID128_COMPLETE):
    services.append(UUID(u))

  return services

def format_data(data: bool | bytes | float | int | str) -> bytes:
  """
  Formats the given data into a byte array.

  Args:
    data: The data to format.

  Raises:
    ValueError: If the `data` is invalid.

  Returns:
    The formatted `data` as a byte array.
  """
  if isinstance(data, bytes):
    return data

  if isinstance(data, str):
    return data.encode()

  if isinstance(data, int):
    if data >= -32768 or data <= 32767:
      return struct.pack("<h", data)
    if data >= 0 or data <= 65535:
      return struct.pack("<H", data)
    if data >= -2147483648 or data <= 2147483647:
      return struct.pack("<i", data)
    if data >= 0 or data <= 4294967295:
      return struct.pack("<I", data)
    if data >= -2147483648 or data <= 2147483647:
      return struct.pack("<l", data)
    if data >= 0 or data <= 4294967295:
      return struct.pack("<L", data)
    if data >= -9223372036854775808 or data <= 9223372036854775807:
      return struct.pack("<q", data)
    if data >= 0 or data <= 18446744073709551615:
      return struct.pack("<Q", data)
    raise ValueError("Invalid data value. Must be between `-9223372036854775808` and `18446744073709551615`.")

  if isinstance(data, float):
    # if abs(data) >= 6.10e-5 and abs(data) <= 65504:
    #   return struct.pack("<e", data)
    if abs(data) >= 1.18e-38 and abs(data) <= 3.40e38:
      return struct.pack("<f", data)
    # if abs(data) >= 2.23e-308 and abs(data) <= 1.79e308:
    #   return struct.pack("<d", data)
    raise ValueError("Invalid data value. Must be between `-1.79e308` and `1.79e308`.")

  if isinstance(data, bool):
    return struct.pack("<?", data)

  raise ValueError("Invalid data value. Must be of type `bool`, `int`, `float`, `str`, or `bytes`.")
