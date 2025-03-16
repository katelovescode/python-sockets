import socket
import sys
import re

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = int(sys.argv[1])

s.bind(('', port))

s.listen()

request = ''

response = ("HTTP/1.1 200 OK\r\n"
"Content-Type: text/plain\r\n"
"Content-Length: 6\r\n"
"Connection: close\r\n"
"\r\n"
"Hello!\r\n\r\n")

while True:
  new_connection = s.accept()
  print(new_connection)
  new_socket = new_connection[0]
  while True:
    data = new_socket.recv(4096).decode("ISO-8859-1")
    if "\r\n\r\n" in data:
      request = request + data
      print("Received full request {request}".format(request=request))
      print("Sending response {response}".format(response=response))
      new_socket.sendall(response.encode("ISO-8859-1"))
      print("Closing")
      new_socket.close()
      request = ''
      break
    else:
      request = request + data