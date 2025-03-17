import socket
import sys

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = int(sys.argv[1])

s.bind(('', port))

s.listen()

def split_file_path(request):
  request_headers = request.split("\r\n")
  file_name = request_headers[0].split()[1].split("/")[-1]
  extension = file_name.split(".")[-1]
  if extension == "txt":
    file_type = 'text/plain; charset=iso-8859-1'
  elif extension == "html":
    file_type = 'text/html; charset=iso-8859-1'
  else:
    raise Exception("File type not supported")
  return { 'file_name': file_name, 'file_type': file_type}

def build_response(file_type, content_length, payload):
  return ("HTTP/1.1 200 OK\r\n"
  "Content-Type: {file_type}\r\n"
  "Content-Length: {content_length}\r\n"
  "Connection: close\r\n"
  "\r\n"
  "{payload}\r\n\r\n").format(file_type=file_type, content_length=content_length, payload=payload)

def error_415():
  return ("HTTP/1.1 415 Unsupported Media Type\r\n"
  "Content-Type: text/plain\r\n"
  "Content-Length: 26\r\n"
  "Connection: close\r\n"
  "\r\n"
  "415 unsupported media type\r\n\r\n")

def error_404():
  return ("HTTP/1.1 404 Not Found\r\n"
  "Content-Type: text/plain\r\n"
  "Content-Length: 13\r\n"
  "Connection: close\r\n"
  "\r\n"
  "404 not found\r\n\r\n")

while True:
  new_connection = s.accept()
  new_socket = new_connection[0]
  while True:
    print("getting new data")
    request = ''
    data = new_socket.recv(4096).decode("ISO-8859-1")
    if "\r\n\r\n" in data:
      request = request + data
      print("Received full request {request}".format(request=request))

      # SERVE A FILE HERE
      
      try:
        path_dict = split_file_path(request=request)
        with open(path_dict['file_name'], "rb") as file_contents:
          contents = file_contents.read().decode("ISO-8859-1")
        response = build_response(file_type=path_dict['file_type'], content_length=len(contents), payload=contents)
        print("Sending: ", response)
        new_socket.sendall(response.encode("ISO-8859-1"))
      except Exception as inst:
        print(inst)
        print(inst.args)
        if inst.args[0] == "File type not supported":
          new_socket.sendall(error_415().encode("ISO-8859-1"))
        elif inst.args[0] == 2:
          new_socket.sendall(error_404().encode("ISO-8859-1"))
      finally:
        print("Closing")
        new_socket.close()
        break
    else:
      request = request + data

