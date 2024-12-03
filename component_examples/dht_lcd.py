from machine import I2C
from utils.main_loop import main_loop
from utils.interrupt_mutex import InterruptMutex
from components.button import Button
from components.dht import DHT
from components.lcd import LCD1602

dht = DHT(version = 11, pin_id = 16)
i2c = I2C(1, sda = 2, scl = 3, freq = 400000)
lcd = LCD1602(i2c)
unit_toggle = Button(15)

@unit_toggle.release_handler()
def toggle_temperature_unit():
  """ Toggles the temperature unit to use when measuring DHT temperature data. """
  if dht.temperature_unit == 'F':
    dht.temperature_unit = 'C'
  elif dht.temperature_unit == 'C':
    dht.temperature_unit = 'K'
  else:
    dht.temperature_unit = 'F'

  output_dht()

@InterruptMutex(discard_duplicates = True)
def output_dht():
  """ Output DHT sensor data to the LCD display. """
  text = f"T: {dht.temperature()} {dht.temperature_unit}\nH: {dht.humidity()} %"
  lcd.message(text)

main_loop(output_dht, 1000, cleanup = lcd.clear)
