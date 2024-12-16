from lib.ir_rx.nec import NEC_8
from machine import Pin
from utils.main_loop import MainLoop

def callback(ir_bit, addr, ctrl):
  print(ir_bit, addr, ctrl)

ir = NEC_8(Pin(17, Pin.IN), callback)

MainLoop.run(lambda _: None, 1000, cleanup = ir.close)
