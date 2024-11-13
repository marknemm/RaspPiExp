from time import sleep

from machine import Pin

ledArr = [
    Pin(17, Pin.OUT),
    Pin(16, Pin.OUT),
    Pin(14, Pin.OUT),
    Pin(15, Pin.OUT)
]

def resetLEDs():
    """
    Reset Counter
    """
    for led in ledArr:
        led.off()

print('Starting...')
resetLEDs()

while True:
    try:
        for led in ledArr:
            led.toggle()
            if led.value() != 0:
                break
        binaryArr = list(map(lambda led: 1 if led.value() else 0, ledArr))
        binaryArr.reverse()
        print(binaryArr)
        sleep(.3)
    except KeyboardInterrupt:
        break

resetLEDs()
print('Exiting...')
