from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
# PORT_NUMBER = 5000
# SIZE = 1024

# hostName = gethostbyname('0.0.0.0')

# mySocket = socket(AF_INET, SOCK_DGRAM)
# mySocket.settimeout(30)
# mySocket.bind((hostName, PORT_NUMBER))

# print("Test server listening on port {0}\n".format(PORT_NUMBER))

# while True:
#         (data, addr) = mySocket.recvfrom(SIZE)

#         if data != None:
#             print (int.from_bytes(data, "little"))
#             print(type((int.from_bytes(data, "little"))))
# sys.ext()


def open_socket():
    PORT_NUMBER = 5000

    SIZE = 1024

    hostName = gethostbyname('0.0.0.0')

    mySocket = socket(AF_INET, SOCK_DGRAM)
    mySocket.setblocking(1)
    mySocket.bind((hostName, PORT_NUMBER))

    print("Test server listening on port {0}\n".format(PORT_NUMBER))
    state = True
    while state:
            (data, addr) = mySocket.recvfrom(SIZE)
            if not data == None:
                stim = (int.from_bytes(data, "big"))
                print(stim)
                if stim == 88:
                    state = False

open_socket()