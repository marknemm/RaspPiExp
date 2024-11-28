from socket import socket, AF_INET, SOCK_DGRAM
import network
from time import sleep_ms

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('MySpectrumWiFi43-2G', 'famousgate426')

while not wifi.isconnected():
  print('Waiting for connection...')
  sleep_ms(250)
print('Connected: ', wifi.ifconfig())

server_ip = wifi.ifconfig()[0]
SERVER_PORT = 2222
BUFFER_SIZE = 1024 # bytes

udp_server = socket(AF_INET, SOCK_DGRAM)
udp_server.bind((server_ip, SERVER_PORT))

try:
  while True:
    (message, address) = udp_server.recvfrom(BUFFER_SIZE)
    decoded_message = message.decode('utf-8')
    print(decoded_message)
except KeyboardInterrupt:
  pass

udp_server.close()
wifi.disconnect()
