from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_BROADCAST
from asyncio import sleep as async_sleep
from utils.main_loop import MainLoop
from utils.wifi import WiFi
from utils.async_socket import AsyncSocket

wifi = WiFi.init('MySpectrumWiFi43-2G', 'famousgate426')
print(wifi.ip_address)

BROADCAST_PORT = 5005
broadcast_udp_sock = AsyncSocket(AF_INET, SOCK_DGRAM)
broadcast_udp_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
broadcast_udp_sock.bind((wifi.ip_address, BROADCAST_PORT))

SERVER_TCP_PORT = 5006
server_tcp_sock = AsyncSocket(AF_INET, SOCK_STREAM)
server_tcp_sock.bind(('0.0.0.0', SERVER_TCP_PORT))
server_tcp_sock.listen()
server_tcp_connections: list[tuple[socket, str]] = []

async def receive_broadcast():
  """ Receive broadcast messages over LAN on port 5005. """
  data = await broadcast_udp_sock.async_recvfrom(1024)
  print(f"Received connection broadcast request from {data[1][0]}:{data[1][1]}")

  connect_data = f'''
    {{
      "service": "trip-alarm",
      "address": "{wifi.ip_address}",
      "port": {str(SERVER_TCP_PORT)}
    }}
  '''
  broadcast_udp_sock.sendto(connect_data.encode(), data[1])

async def accept_connections():
  """ Accept incoming TCP connections on port 5006. """
  connection = await server_tcp_sock.async_accept()
  print(f"Accepted connection from {connection[1][0]}:{connection[1][1]}")
  server_tcp_connections.append(connection)

async def send_data():
  """ Sends data to all connected TCP clients."""
  for conn in server_tcp_connections[:]: # Iterate over shallow copy so can remove items.
    print(f"Sending data to {conn[1][0]}:{conn[1][1]}.")
    try:
      conn[0].send(b'Ping')
    except OSError:
      print(f"Connection to {conn[1][0]}:{conn[1][1]} was closed.")
      server_tcp_connections.remove(conn)
  await async_sleep(10)

def cleanup():
  """ Cleanup resources once the main loop has finished. """
  broadcast_udp_sock.close()
  server_tcp_sock.close()
  wifi.active(False)
  print("cleanup")

MainLoop.run_async([receive_broadcast, accept_connections, send_data], cleanup = cleanup)
