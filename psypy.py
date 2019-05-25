from psychopy import visual, event, core
from numpy import sin, pi
import random
import matplotlib.pyplot as plt

import sys
from socket import socket, AF_INET, SOCK_DGRAM
import time

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys

# PORT_NUMBER = 5000
# SIZE = 1024

# hostName = gethostbyname('0.0.0.0')

# mySocket = socket(AF_INET, SOCK_DGRAM)
# mySocket.setblocking(1)
# mySocket.bind((hostName, PORT_NUMBER))

#print("Test server listening on port {0}\n".format(PORT_NUMBER))

screen_resolution = [1366, 768] # Auto adjustable
stimuli_freq = [10, 12, 14, 66] # From lowest to highest, max 4

window = visual.Window(screen_resolution, monitor="testMonitor",
                       units='pix', fullscr=False, color=[-1, -1, -1])


stimuli_order = random.choices(stimuli_freq, k=21)

sign_stimuli = visual.Polygon(
    window, 
    edges=3,
    radius=50, 
    pos=(0, 250), 
    ori=180, 
    color=[-1, 1, -1])

stimuli_pos = {stimuli_freq[0]: (0, 250),
               stimuli_freq[1]: (500, 250),
               stimuli_freq[2]: (-500, 250),
               stimuli_freq[3]: (-5000, 2500),
}

stimuli_1 = visual.Rect(
    win=window,
    units="pix",
    width=300,
    height=300,
    fillColor=[0, 1, 0]
)

stimuli_2 = visual.Rect(
    win=window,
    units="pix",
    width=300,
    height=300,
    fillColor=[1, 1, 0],
    pos=(500, 0)
)

stimuli_3 = visual.Rect(
    win=window,
    units="pix",
    width=300,
    height=300,
    fillColor=[1, 1, 0],
    pos=(-500, 0),
)

current_frame = 0

stim_1 = visual.TextStim(window, str(stimuli_freq[0]) + 'hz',
                       color=(0, 1, 0), colorSpace='rgb')

stim_2 = visual.TextStim(window, str(stimuli_freq[1]) + 'hz',
                         color=(0, 1, 0), colorSpace='rgb', pos=(500, 0))

stim_3 = visual.TextStim(window, str(stimuli_freq[2]) + 'hz',
                         color=(0, 1, 0), colorSpace='rgb', pos=(-500, 0))


timer = core.CountdownTimer(5)

# while True: 
#     (data, addr) = mySocket.recvfrom(SIZE)
#     if not data == None:
#         stim = (int.from_bytes(data, "big"))
#         state = True

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
                print (stim)
                if stim == 88:
                    state = False

while True:
    #(data, addr) = mySocket.recvfrom(SIZE)

    color = sin(stimuli_freq[0]*pi*2*current_frame/60)
    color_2 = sin(stimuli_freq[1]*pi*2*current_frame/60)
    color_3 = sin(stimuli_freq[2]*pi*2*current_frame/60)

    #print(int.from_bytes(data, "big"))

    sign_stimuli.pos = stimuli_pos[10]
    sign_stimuli.draw()

    stimuli_1.setFillColor([-1, color, -1])
    stimuli_1.draw()

    stimuli_2.setFillColor([-1, color_2, -1])
    stimuli_2.draw()

    stimuli_3.setFillColor([-1, color_3, -1])
    stimuli_3.draw()

    # Text inside the box 
    stim_1.draw()
    stim_2.draw()
    stim_3.draw()
    
    window.flip()
    current_frame += 1

    for key in event.getKeys():
        if key in ['escape', 'q']:
            core.quit()

# if __name__ == '__main__':
#     open_socket()
#     #p = Process(target=open_socket)
#     #p.start()
#     #p.join()
