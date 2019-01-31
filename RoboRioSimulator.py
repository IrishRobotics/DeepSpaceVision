import numpy as np
import cv2
import math
import socket
import pickle
import sys
import struct
from matplotlib import pyplot as plt 

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

print(f'RoboRio Simulator')

imageFinal = None

Host = '0.0.0.0' # CHANGE THIS to roboRio Network Ip address
Port = 5804

# try:
#     recvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Connection
# except socket.error:
#     print (f'Couldnt connect with the socket-server: \n terminating program')
#     sys.exit(1)

recvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Tcp Connection

recvSocket.bind((Host, Port))
recvSocket.listen(1)
conn, addr = recvSocket.accept()
print(f'Connection address: {addr}')

while True:
    data = conn.recv(4) # buffer size is 1024 bytes
    #print (f'received message:, {data}')
    if data: 
        message = struct.unpack('!i', data)
        messageId = message[0]
        #print(f'{messageId}')
        
        if messageId == 1:           
            data = conn.recv(28)
            messageType1 = struct.unpack('!ddhhhi', data) 
            
            targetAngle = messageType1[0]
            targetDistance = messageType1[1]
            timeHour = messageType1[2]
            timeMinute = messageType1[3]
            timeSecond = messageType1[4]
            timeMicroSecond = messageType1[5]




            print(f'got vision target found {targetAngle} {targetDistance} {timeHour}:{timeMinute}:{timeSecond}.{timeMicroSecond}')

        elif messageId == 2:
            print('got no vision target found')

        elif messageId == 3:
            data = conn.recv(4)
            messageType3 = struct.unpack('!i', data)
            imageSize = messageType3[0]
            imageDataRecv = recvall(conn, imageSize)
            print(f'got image size = {imageSize}')
            #imageData = np.asarray(bytearray(imageDataRecv))
            # imageData = np.fromstring(imageDataRecv, np.uint8)
            # imageBGR = cv2.imdecode(imageData, flags=cv2.IMREAD_COLOR)
            # imageX = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
            imageX = pickle.loads(imageDataRecv, fix_imports=True, encoding="bytes")
            imageFinal = cv2.imdecode(imageX, cv2.IMREAD_COLOR)
            #cv2.imwrite('example.jpg', imageY)

    if imageFinal is not None:
        cv2.imshow('Contour Processed Image',imageFinal)
        cv2.waitKey(10)