from psychopy import visual, event, core
from numpy import sin, pi
import random
import matplotlib.pyplot as plt
import multiprocessing as mp
import sys
from socket import socket, AF_INET, SOCK_DGRAM
import time
import pickle

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys


class getStimulies(object):
    def __init__(self, PORT_NUMBER=5000, SIZE=4096):
        print("Initializing...")
        self.PORT_NUMBER = PORT_NUMBER

        self.SIZE = SIZE

        self.hostName = gethostbyname('0.0.0.0')

        self._stimuli_list = []

    def getStims(self):
        self.mySocket = socket(AF_INET, SOCK_DGRAM)
        self.mySocket.settimeout(60.0)
        self.mySocket.bind((self.hostName, self.PORT_NUMBER))
        print ("Waiting for data from BCI Application. Timeout(60s)")
        while True:
            (data, addr) = self.mySocket.recvfrom(self.SIZE)
            if not data == None:
                self._stimuli_list = pickle.loads(data)
                self.mySocket.close()
                print("Data received! Closing connection...")
                return self._stimuli_list

class ControlUnitSocket(object):
    def __init__(self, PORT_NUMBER=5000, SIZE=1024):
        self.PORT_NUMBER = PORT_NUMBER

        self.SIZE = SIZE

        self.hostName = gethostbyname('0.0.0.0')
        self.stim_shared = mp.Value('i', 0)
        self.terminate = mp.Event()
        self.lock = mp.Lock()

    def _listen(self, stim_shared):
        self.stim_shared = stim_shared
        self.mySocket = socket(AF_INET, SOCK_DGRAM)
        self.mySocket.setblocking(1)
        self.mySocket.bind((self.hostName, self.PORT_NUMBER))

        print("Server listening on port {0}\n".format(self.PORT_NUMBER))
        
        state = True
        while state:
            (data, addr) = self.mySocket.recvfrom(self.SIZE)
            if not data == None:
                stim = (int.from_bytes(data, "big"))
                #print ("stim",stim)
                with self.lock:
                    self.stim_shared.value = stim
                    
                if stim == 88:
                    state = False
                if self.terminate.is_set():
                    self.socket_process.terminate()
                    self.terminate.clear()


    def openConnection(self):
        self.socket_process = mp.Process(name="PythonSocket", target=self._listen,
                               args=(self.stim_shared,))
        self.socket_process.daemon = True
        self.socket_process.start()
    
    def closeConnection(self):
        self.socket_process.terminate()


class display(object):
    def __init__(self, socket, stims):
        
        self.socket = socket
        time.sleep(1)
        print("Initializing connection...")
        self.socket.openConnection()
        self.screen_resolution = [1366, 768] # Auto adjustable
        self.stimuli_freq = stims  # From lowest to highest, max 4

        self.window = visual.Window(self.screen_resolution, monitor="testMonitor",
                            units='pix', fullscr=False, color=[-1, -1, -1])


        self.sign_stimuli = visual.Polygon(
            self.window, 
            edges=3,
            radius=50, 
            pos=(0, 250), 
            ori=180, 
            color=[-1, 1, -1])

        self.stimuli_pos = {self.stimuli_freq[0]: (0, 250),
                    self.stimuli_freq[1]: (500, 250),
                    self.stimuli_freq[2]: (-500, 250),
                    0: (-5000, 2500), # OFF SCREEN
        }

        self.stimuli_1 = visual.Rect(
            win=self.window,
            units="pix",
            width=300,
            height=300,
            fillColor=[0, 1, 0]
        )

        self.stimuli_2 = visual.Rect(
            win=self.window,
            units="pix",
            width=300,
            height=300,
            fillColor=[1, 1, 0],
            pos=(500, 0)
        )

        self.stimuli_3 = visual.Rect(
            win=self.window,
            units="pix",
            width=300,
            height=300,
            fillColor=[1, 1, 0],
            pos=(-500, 0),
        )

        self.current_frame = 0

        self.stim_1 = visual.TextStim(self.window, str(self.stimuli_freq[0]) + 'hz',
                            color=(0, 1, 0), colorSpace='rgb')

        self.stim_2 = visual.TextStim(self.window, str(self.stimuli_freq[1]) + 'hz',
                                color=(0, 1, 0), colorSpace='rgb', pos=(500, 0))

        self.stim_3 = visual.TextStim(self.window, str(self.stimuli_freq[2]) + 'hz',
                                color=(0, 1, 0), colorSpace='rgb', pos=(-500, 0))

        #self.timer = core.CountdownTimer(0)
        state = True
    
        while state:

            self.color = sin(self.stimuli_freq[0]*pi*2*self.current_frame/60)
            self.color_2 = sin(self.stimuli_freq[1]*pi*2*self.current_frame/60)
            self.color_3 = sin(self.stimuli_freq[2]*pi*2*self.current_frame/60)

            self.sign_stimuli.pos = self.stimuli_pos[self.socket.stim_shared.value]
            self.sign_stimuli.draw()

            self.stimuli_1.setFillColor([-1, self.color, -1])
            self.stimuli_1.draw()

            self.stimuli_2.setFillColor([-1, self.color_2, -1])
            self.stimuli_2.draw()

            self.stimuli_3.setFillColor([-1, self.color_3, -1])
            self.stimuli_3.draw()

            # Text inside the box
            self.stim_1.draw()
            self.stim_2.draw()
            self.stim_3.draw()

            self.window.flip()
            self.current_frame += 1

            # if not self.timer.getTime() > 0:
            #     _default = 0
                #self.socket.stim_shared.value = 0
                #self.timer.add(5)
                #print(self.socket.stim_shared.value)
                #self.sign_stimuli.pos = self.stimuli_pos[self.socket.stim_shared.value]
                #self.sign_stimuli.draw()
                #self.timer.add(5)
                #self.sign_stimuli.pos = self.stimuli_pos[0]
                #self.timer.add(2)

            for key in event.getKeys():
                if key in ['escape', 'q']:
                    core.quit()


if __name__ == "__main__":
    myDisplay = display(stims=getStimulies().getStims(), socket=ControlUnitSocket())
