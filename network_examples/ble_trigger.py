"""
This example demonstrates a simple temperature sensor peripheral.

The sensor's local value is updated, and it will notify any connected central every 10 seconds.
"""

from components.button import Button
from ubinascii import hexlify
from utils.main_loop import MainLoop
from utils.ble import BLE, BLE_APPEARANCE_GENERIC_THERMOMETER, UUID, FLAG_READ, FLAG_INDICATE, FLAG_NOTIFY
from components.thermometer import Thermometer

_ENV_SENSE_UUID = UUID(0x181A) # org.bluetooth.service.environmental_sensing
_TEMP_CHAR = (
  UUID(0x2A6E), # org.bluetooth.characteristic.temperature
  FLAG_READ | FLAG_INDICATE | FLAG_NOTIFY,
)
ENV_SENSE_SERVICE = (
  _ENV_SENSE_UUID,
  (_TEMP_CHAR,),
)

ble = BLE()
thermometer = Thermometer(4)
button = Button(15)

((service_handle,),) = ble.gatts_register_services((ENV_SENSE_SERVICE,))

ble.advertise('Pico W - Temp', [_ENV_SENSE_UUID], BLE_APPEARANCE_GENERIC_THERMOMETER)
print(f"Advertising 'Pico W - Temp' service --- {hexlify(_ENV_SENSE_UUID).decode().upper()}")

@button.release_handler()
def update_temperature():
  """ Update the temperature value and notify any connected centrals. """
  temperature = thermometer.temperature()
  print("write temp %.2f F" % temperature)
  ble.broadcast(service_handle, temperature)

MainLoop.run(lambda: None, 1000, cleanup = lambda: ble.active(False))
