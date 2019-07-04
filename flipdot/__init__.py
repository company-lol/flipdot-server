#!/usr/bin/python3
# coding: utf-8 

import time
from pyflipdot.sign import HanoverSign
from pyflipdot.pyflipdot import HanoverController
from flipdot.simulator import flipdotSim
from serial import Serial
import logging


class sign:

    LOG_LEVEL = logging.DEBUG

    def __init__(self, serial_port, address, cols, rows, name="Flippy", simulator=False):
        # Create a serial port (update with port name on your system)
        logging.basicConfig(level=self.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)
        self.sign = HanoverSign(address=int(address), width=int(cols), height=int(rows))
        if not simulator:
            try:
                self.ser = Serial(serial_port)
            except:
                raise Exception("Serial port not detected. Is your sign plugged in? ")
            self.controller = HanoverController(self.ser)
            self.controller.add_sign(name, self.sign)
        
        if simulator:
            self.simulator = flipdotSim(int(cols), int(rows))

    def send(self):
        self.display.send()

    def clear(self):
        self.logger.debug("erasing")
        empty = self.sign.create_image()
        self.render_image(empty)

    def render_numpy_array(self, image_data):
        if 'simulator' in dir(self):
            self.simulator.render_image(image_data)   
        else:
            self.controller.draw_image(image_data)
