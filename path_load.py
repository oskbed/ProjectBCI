import os

class PortDiscover(object):
    def __init__(self):
        self.port = self.port_search()
    def port_search(self):
        _PORTS = []
        for i in os.listdir(path='/dev'):
            if "tty.usbserial" in i:
                _PORTS.append(i)
                break
        print ("USB devices: {}".format(_PORTS))
        if len(_PORTS) >= 2:
            print("Please, remove additional USB Devices from your computer and try again!")
        elif len(_PORTS) == 1:
            print("Connecting to port: {}".format(_PORTS[0]))
        elif len(_PORTS) == 0:
            print("No ports found!")
        else:
            print ("Sorry, something went wrong :(")
        return "/dev/" + _PORTS[0]
