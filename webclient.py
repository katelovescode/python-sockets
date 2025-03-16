import socket
import sys
import re

s = socket.socket()
host = sys.argv[1]

if len(sys.argv) < 3 or sys.argv[2] == '':
  port = 80
else:
  port = int(sys.argv[2])

url_parts = re.split(r'^((?:.*?(?=:\/\/))*)(?::\/\/)?(?=.*\.)([A-Za-z0-9\-\.]+)(.*)$', host)[2:4]

if url_parts[1] == '':
  path = '/'
else:
  path = url_parts[1]

s.connect((host, port))

http_request = ("GET {path} HTTP/1.1\r\n"
"Host: {host}\r\n"
"Connection: close\r\n\r\n"
).format(path=path, host=host)

print(http_request)

s.sendall(http_request.encode("ISO-8859-1"))

response = ''.encode("ISO-8859-1")

while True:
  data = s.recv(4096)
  if not data: break
  response = response + data

print(response.decode("ISO-8859-1"))