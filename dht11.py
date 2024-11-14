from utime import sleep
from dht import DHT11

from components.button import Button

unit_toggle = Button(15)
sensor = DHT11(16)

interrupted = False

def print_measurements(is_interrupt: bool | None = None):
  """
  Prints the measurements acquired by the DHT sensor.

  Params:
    is_interrupt: The current state of the unit toggle button if this method was triggered by a button interrupt,
    otherwise defaults to `None`.
  """
  global interrupted
  interrupted = is_interrupt is not None

  temperature = sensor.temperature()
  temperature_unit = 'C'
  humidity = sensor.humidity()

  if temperature is not None and humidity is not None:
    if unit_toggle.state:
      temperature = round(temperature * 1.8 + 32)
      temperature_unit = 'F'

    # Check if main loop was interrupted via button press during its measurement and print cycle to prevent race
    if not interrupted or is_interrupt is not None:
      print("\r", f"Temp: {temperature}{temperature_unit}\t", f"Humidity: {humidity}%", end='')

unit_toggle.register_interrupt_handler(print_measurements)

while True:
  try:
    sensor.measure()
    print_measurements()
    sleep(1)
  except KeyboardInterrupt:
    break

print("\n\nFinished.")
