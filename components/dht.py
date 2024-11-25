from machine import Timer
from dht import DHT11, DHT22, DHTBase

class DHT(DHTBase):
  """ A digital humidity and temperature sensor. """

  def __init__(self, version: int, pin_id: int, temperature_unit = 'F', sample_period_ms = 1000):
    """
    Args:
      version: The version of the DHT sensor. Must either be `11` or `22`.
      pin_id: The ID of the GPIO Pin to use for reading DHT sensor values.
      temperature_unit: The optional unit to convert measured temperature values to. Must be either `'F'`, `'C'`, or `'K'`. Defaults to `'F'`.
      sample_period_ms: The optional sample period in milliseconds, which determines the frequency at which to measure DHT values. Defaults to `1000`. If set to `0` or a negative number, then automatic periodic measurement does not occur, and manual calls to `measure` must be made.

    Raises:
      ValueError: If given an invalid `temperature_unit` value. Must be given `'F'`, `'C'`, or `'K'` (case insensitive).
      ValueError: If given an invalid DHT sensor `version` value. Must be given either `11` or `22`.
    """
    self.__temperature_unit = 'F'
    self.temperature_unit = temperature_unit

    if version == 11:
      self.__dht_sensor = DHT11(pin_id)
    elif version == 22:
      self.__dht_sensor = DHT22(pin_id)
    else:
      raise ValueError(f"Invalid DHT version. Valid values are 11 or 22; was given {version}.")

    if sample_period_ms > 0:
      self.__sampling_timer = Timer(-1) # -1 for lower resource virtual timer
      self.__sampling_timer.init(period = sample_period_ms, callback = self.measure)

  @property
  def version(self) -> int:
    """ The version of the DHT sensor. Either `11` or `22`. """
    return 11 if isinstance(self.__dht_sensor, DHT11) else 22

  @property
  def temperature_unit(self) -> str:
    """ The configured temperature unit to convert measured temperature values to. Either `'F'`, `'C'`, or `'K'`. """
    return self.__temperature_unit

  @temperature_unit.setter
  def temperature_unit(self, value: str):
    if value.strip().upper() not in ['F', 'C', 'K']:
      raise ValueError(f"Invalid temperature_unit value. Must be either 'F', 'C', or 'K'; was given '{value}'.")

    self.__temperature_unit = value.upper()

  def humidity(self) -> int:
    """
    Gets the last measured humidity from the DHT sensor.

    Returns:
      The last measured humidity value.
    """
    return self.__dht_sensor.humidity()

  def temperature(self, unit = '', ndigits = 0) -> float:
    """
    Gets the last measured temperature from the DHT sensor.

    Args:
      unit: An optional unit conversion for the retrieved temperature. Defaults to the configured `temperature_unit`.
      ndigits: An optional number of digits to the right of the decimal point to round to. Defaults to `0` for rounding to a whole number.

    Raises:
      ValueError: If `unit` is not '', `F`, `C`, or `K` (case insensitive).

    Returns:
      The last measured temperature value.
    """
    unit = unit.upper() if unit else self.temperature_unit

    temperature: float = self.__dht_sensor.temperature()

    if unit == 'F':
      temperature = temperature * 1.8 + 32
    elif unit == 'K':
      temperature = temperature + 273.15
    elif unit != 'C':
      raise ValueError(f"Invalid (temperature) unit value. Must be either 'F', 'C', or 'K'; was given '{unit}'")

    return round(temperature, ndigits) if ndigits else int(round(temperature))

  def measure(self, *args, **kwargs):
    """ Manually triggers a DHT sensor measurement for humidity and temperature. """
    self.__dht_sensor.measure()
