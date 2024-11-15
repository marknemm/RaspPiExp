from dht import DHT11

from components.button import Button

from utils.main_loop import main_loop

unit_toggle = Button(15)
sensor = DHT11(16)

def print_measurements(_ = None):
  """ Prints the measurements acquired by the DHT sensor. """
  temperature = sensor.temperature()
  temperature_unit = 'C'
  humidity = sensor.humidity()

  if temperature is not None and humidity is not None:
    if unit_toggle.toggle_state:
      temperature = round(temperature * 1.8 + 32, 1)
      temperature_unit = 'F'

    # Check if main loop was interrupted via button press during its measurement and print cycle to prevent race
    if not unit_toggle.release_interrupt:
      print("\r", f"Temp: {temperature}{temperature_unit}   ", f"Humidity: {humidity}%", end='   ')

def measure_dht():
  """ Measures and prints the digital humidity and temperature. """
  sensor.measure()
  print_measurements()

unit_toggle.register_release_handler(print_measurements)
main_loop(measure_dht, 1000)
