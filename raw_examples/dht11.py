from dht import DHT11
from utils.main_loop import main_loop
from components.button import Button

unit_toggle = Button(15)
sensor = DHT11(16)

@unit_toggle.release_handler(with_mutex = True)
def print_measurements():
  """ Prints the measurements acquired by the DHT sensor. """
  temperature = sensor.temperature()
  temperature_unit = 'C'
  humidity = sensor.humidity()

  if unit_toggle.toggle_state:
    temperature = round(temperature * 1.8 + 32, 1)
    temperature_unit = 'F'

  print("\r", f"Temp: {temperature}{temperature_unit}   ", f"Humidity: {humidity}%", end='   ')

def measure_dht():
  """ Measures and prints the digital humidity and temperature. """
  sensor.measure()
  print_measurements()

main_loop(measure_dht, 1000)
