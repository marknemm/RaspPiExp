from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from time import sleep

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

s.sendto(b"Hello, Pico W -- 5005", ("192.168.1.255", 5005))
sleep(.25)

s.sendto(b"Hello, Pico W -- 5006", ("192.168.1.255", 5006))
sleep(.25)

s.sendto(b"Hello, Pico W -- 5007", ("192.168.1.255", 5007))
sleep(.25)

s.sendto(b"Hello, Pico W -- 5008", ("192.168.1.255", 5008))
