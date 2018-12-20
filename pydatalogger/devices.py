# -*- coding: utf-8 -*-
# (c) 2018 The Hiveeyes Developers <hello@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import time
import logging
from pydatalogger.util import mean

log = logging.getLogger(__name__)


class Device_ABE_DeltaSigmaPiADC:
    """
    https://github.com/abelectronicsuk/ABElectronics_Python_Libraries
    """

    def __init__(self, bus=None, address=None, address2=None, samplerate=None, gain=None):
        from ABE_helpers import ABEHelpers
        from ABE_ADCDifferentialPi import ADCDifferentialPi

        if bus is None:
            i2c_helper = ABEHelpers()
            bus = i2c_helper.get_smbus()

        # Initialize the ADC device using the default addresses and sample rate 18.
        # Sample rate can be 12, 14, 16 or 18.
        self.adc = ADCDifferentialPi(bus, address=address, address2=address2, rate=samplerate)

        # Set amplifier gain to 8.
        if gain is not None:
            self.adc.set_pga(gain)

    def read(self, channel):
        # Returns the voltage from the selected ADC channel - channels 1 to 8.
        return self.adc.read_voltage(channel)


class ADCWeightDecoder:

    def __init__(self, source):
        """
        TODO: Obtain all parameters from configuration.
        """

        self.source = source

        # Maximum weight of load cell in kg.
        self.capacity = 50

        # Set excitation voltage of load cell, external power supply.
        self.excitation_voltage = 5

        # Full scale calibration of the load cells, e.g. 2mV/V excitation voltage 1.
        # Data 1-4 taken from load cell data sheet.
        self.fullscale_output = (0.001953, 0.001948, 0.001943, 0.001933, 0.002, 0.002, 0.002, 0.002)

        # Zero Value in V of CZL601-50kg (including Unterboden of bee hive)
        # self.zerovalue = (0.000258, 0.000438, 0.000453, 0.000429, 0.000,0.000, 0.000, 0.000)
        self.zerovalue = (0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000)

    def read(self, channel):
        value = \
            (self.source.read(channel) - self.zerovalue[channel - 1]) * self.capacity / \
            (self.excitation_voltage * self.fullscale_output[channel - 1])
        return value


class MultiSensorReader:

    def __init__(self, source, channels=None, reading_count=10, wait=0.5):

        self.source = source

        # List of addresses to sample (e.g. load cells).
        self.channels = channels or []

        # Number of measurements to get average value and deviation.
        self.reading_count = reading_count

        # Time between measurements in seconds (set between 0.1 an 1 sec).
        self.wait = wait

    def read(self):
        value = 0
        for channel in self.channels:
            value += self.read_single(channel)
        return value

    def read_single(self, channel):
        readings = []
        for _ in range(self.reading_count):
            value = self.source.read(channel)
            readings.append(value)
            time.sleep(self.wait)
        return mean(readings)


