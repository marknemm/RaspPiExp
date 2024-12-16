from machine import I2C
from utils.main_loop import MainLoop
from components.oled import SSD1306_I2C

i2c = I2C(1, sda = 2, scl = 3, freq = 400000)
dsp = SSD1306_I2C(128, 64, i2c)

def main():
  msg = 'Hello World!'
  dsp.text(msg, 0, 0)
  dsp.show()

MainLoop.run(main, setup = dsp.poweron, cleanup = dsp.poweroff)
