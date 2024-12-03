import bluetooth, struct
from time import sleep

_IRQ_SCAN_RESULT = 5
_IRQ_SCAN_DONE = 6
# here instead of REDACTED you put the address of the transmitter that you get by print(bytes(ble.config('mac')[1])) on the transmitter
serverAddress = bytes(b'REDACTED')

#event handler function
def bt_irq(event, data):
    global receivedNumber, dataReceivedFlag
    if event == _IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, adv_type, rssi, adv_data = data
        address = bytes(addr)
        if address==serverAddress and not dataReceivedFlag:
            receivedNumber=struct.unpack('<i',bytes(adv_data))[0]
            dataReceivedFlag = True
    elif event == _IRQ_SCAN_DONE:
        print('scan finished.')

ble = bluetooth.BLE()
ble.active(True)
ble.irq(bt_irq)

scanDuration_ms = 100000 #specify how long the scanning should take
interval_us = 15000
window_us = 15000 #the same window as interval, means continuous scan
active = False #do not care for a reply for a scan from the transmitter

receivedNumber = 0
dataReceivedFlag = False
ble.gap_scan(scanDuration_ms,interval_us,window_us,active)

while True:
	if dataReceivedFlag:
		print(receivedNumber)
		dataReceivedFlag = False