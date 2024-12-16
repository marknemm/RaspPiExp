from machine import ADC, Pin

class Thermometer:
  """ A thermometer sensor that measures temperature using `ADC` voltage readings. """

  def __init__(self, adc_pin: ADC | Pin | int, temperature_unit = 'F'):
    self.__sensor_pin = adc_pin if isinstance(adc_pin, ADC) else ADC(adc_pin)
    self.__temperature_unit = 'F'
    self.__temperature_unit = temperature_unit

  @property
  def temperature_unit(self) -> str:
    """ The configured temperature unit to convert measured temperature values to. Either `'F'`, `'C'`, or `'K'`. """
    return self.__temperature_unit

  @temperature_unit.setter
  def temperature_unit(self, value: str):
    if value.strip().upper() not in ['F', 'C', 'K']:
      raise ValueError(f"Invalid temperature_unit value. Must be either 'F', 'C', or 'K'; was given '{value}'.")

    self.__temperature_unit = value.upper()

  def temperature(self, unit = '') -> float:
    """
    Measures the temperature by sampling the sensor's ADC voltage readings.

    Args:
      unit: An optional unit conversion for the retrieved temperature. Defaults to the configured `temperature_unit`.

    Raises:
      ValueError: If `unit` is not '', `F`, `C`, or `K` (case insensitive).

    Returns:
      The temperature value in the specified `unit`.
    """
    unit = unit.upper() if unit else self.temperature_unit
    conversion_factor = 3.3 / (65535)
    reading = self.__sensor_pin.read_u16() * conversion_factor

    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
    temperature = 27 - (reading - 0.706) / 0.001721

    if unit == 'F':
      temperature = temperature * 9 / 5 + 32
    elif unit == 'K':
      temperature = temperature + 273.15
    elif unit != 'C':
      raise ValueError(f"Invalid (temperature) unit value. Must be either 'F', 'C', or 'K'; was given '{unit}'")

    return temperature
