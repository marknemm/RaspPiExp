from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from utils.main_loop import main_async_loop
from utils.wifi import WiFi
from utils.async_socket import AsyncSocket

wifi = WiFi.init('MySpectrumWiFi43-2G', 'famousgate426')

async def receive(port):
  sock = AsyncSocket(AF_INET, SOCK_DGRAM)
  sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
  sock.bind((wifi.ip_address, port))

  while True:
    data = await sock.async_recvfrom(1024)
    print(f"From {data[1]}: {data[0].decode()}")

main_async_loop([receive(5005), receive(5006), receive(5007)])
