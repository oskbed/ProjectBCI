#!/usr/bin/env python
# -*- coding: utf-8 -*-

import app

# GLOBAL VARIABLES

# Port adress of OpenBCI Cyton board
BCI_PORT = '/dev/ttyUSB0'

#==============================================================================#
# Run application
#==============================================================================#


# Initialize app
test = app.CcaLive(port=BCI_PORT, connect=True)




# Set stimulus for experiment. Max value = 4.
test.add_stimuli(22)
test.add_stimuli(8)
test.add_stimuli(2)

print("Starting application...")
test.decission()

test.get_correlation()

# Make sure it's dead.
if test.prcs.is_alive():
    print("Terminating process...")
    test.prcs.terminate()
    print("Done!")
