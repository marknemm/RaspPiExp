from utils.main_loop import main_loop
from components.led import LED

led_arr = [
  LED(17),
  LED(16),
  LED(14),
  LED(15),
]

def reset_leds():
  """ Reset counter LEDs to `0`. """
  for led in led_arr:
    led.off()

def increment_counter():
  """ Main loop iteration callback for binary LED counter from `[0, 15]`. """
  for led in led_arr:
    led.toggle()
    if led.intensity != 0:
      break
  binary_arr = list(map(lambda led: 1 if led.intensity else 0, led_arr))
  binary_arr.reverse()
  print(binary_arr)

main_loop(increment_counter, 300, setup = reset_leds, cleanup = reset_leds)
