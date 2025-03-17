import socket
import sys
import re

s = socket.socket()
full_domain_name = sys.argv[1]

if len(sys.argv) < 3 or sys.argv[2] == '':
  print("")
  print("USAGE: python3 webclient.py [full_path] [port]")
  print("    Please include a port number as the last argument (even if it's in the host path, i.e. 'http://localhost:3131/my/path/to/file.txt')")
  print("")
  sys.exit()
else:
  port = int(sys.argv[2])

url_parts = re.split(r'^((?:.*?(?=:\/\/))*)(?::\/\/)?(?=.*\.)([A-Za-z0-9\-\.]+)(?::?[0-9]*)(.*)$', full_domain_name)[2:4]

host = url_parts[0]

try:
  if url_parts[1] == '':
    path = '/'
  else:
    path = url_parts[1]
except:
  print("File name must use a supported extension: txt")
  sys.exit()

s.settimeout(3)

try:
  s.connect((host, port))
except Exception as inst:
  print(inst)
  sys.exit()

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