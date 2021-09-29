import sys
from socket import socket, AF_INET, SOCK_STREAM

# get server name from command line
if len(sys.argv) != 2:
    print('Usage: myftp ftp_server_name')
    sys.exit()
server = sys.argv[1]

# create control connection socket
control_socket = socket(AF_INET, SOCK_STREAM)

# initiate control TCP connection
try:
    control_socket.connect((server, 21))
except Exception:
    print(f'Error: server {server} cannot be found.')
    sys.exit()
print(f'Connected to {server}.')

# print message from server
response = control_socket.recv(1024).decode('utf-8').strip()
print(response)

# send user name to server
username = input('Enter username: ')
control_socket.send(bytes(f'USER {username}\r\n', 'utf-8'))
response = control_socket.recv(1024).decode('utf-8').strip()
print(response)

# send password to server
password = input('Enter password: ')
control_socket.send(bytes(f'PASS {password}\r\n', 'utf-8'))
response = control_socket.recv(1024).decode('utf-8').strip()
print(response)

# login successful
if response.startswith('230'):
    # main loop
    loop = True
    while loop:
        print('Please enter a command, only "quit" supported so far.')
        command = input('ftp> ')

        if command == 'quit':
            # end session
            control_socket.send(bytes('QUIT\r\n', 'utf-8'))
            response = control_socket.recv(1024).decode('utf-8').strip()
            print(response)
            control_socket.close()
            loop = False
        else:
            print(f'Error: command "{command}" not supported')