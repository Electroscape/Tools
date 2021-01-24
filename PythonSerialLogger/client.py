# Import socket module 
import socket			 

# Create a socket object 
s = socket.socket()		 

# Define the port on which you want to connect 
port = 12345				

# connect to the server on local computer
try:
    s.connect(('127.0.0.1', port))
except socket.error as msg:
    print('oops!')
    s.close()

# receive data from the server

while True:
    message = s.recv(1024).decode()
    if message:
        print(message)

# close the connection 
s.close()
