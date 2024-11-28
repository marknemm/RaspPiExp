from socket import socket, AF_INET, SOCK_DGRAM

SERVER_IP = '192.168.1.37'
SERVER_PORT = 2222

udp_client = socket(AF_INET, SOCK_DGRAM)

try:
  while True:
    cmd = input('What is your command: ')
    encoded_cmd = cmd.encode('utf-8')

    udp_client.sendto(encoded_cmd, (SERVER_IP, SERVER_PORT))
except KeyboardInterrupt:
  pass

udp_client.close()
