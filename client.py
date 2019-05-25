import sys
from socket import socket, AF_INET, SOCK_DGRAM
import time
import random


SERVER_IP = '192.168.0.18'
#SERVER_IP = '127.0.0.1'
PORT_NUMBER = 5000
SIZE = 1024
print("Test client sending packets to IP {0}, via port {1}\n".format(
    SERVER_IP, PORT_NUMBER))

mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.connect((SERVER_IP, PORT_NUMBER))

stimuli_order = random.choices([10, 12, 0], k=21)
n = 0 


# while True:
#     time.sleep()
#     n += 1 
time.sleep(5)
mySocket.send(bytes([10]))