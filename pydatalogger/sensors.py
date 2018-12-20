# -*- coding: utf-8 -*-
# (c) 2018 The Hiveeyes Developers <hello@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging

from pydatalogger.acquisition import Reading
from pydatalogger.devices import Device_ABE_DeltaSigmaPiADC, ADCWeightDecoder, MultiSensorReader
from pydatalogger.util import mean

log = logging.getLogger(__name__)


class SENSOR_DUMMY:

    def __init__(self, address):
        self.address = address

    def read(self):
        temperature = 42.42
        humidity = 84.84
        data = [
            Reading(device='Dummy', type='temperature', unit='celsius', address=self.address, value=temperature),
            Reading(device='Dummy', type='humidity', unit='%', address=self.address, value=humidity),
        ]
        return data


class SENSOR_BME280:
    """
    Derived from https://github.com/corny/luftdaten-python/blob/master/bme280/Adafruit_BME280_Example.py

    Will use Adafruit_GPIO.I2C as a default I2C implementation, if none is specified.
    """

    def __init__(self, i2c_adapter=None, address=None):
        self.i2c_adapter = i2c_adapter
        self.address = address

        import Adafruit_BME280 as BME280
        self.sensor = BME280.BME280(
            i2c=self.i2c_adapter, address=self.address,
            t_mode=BME280.BME280_OSAMPLE_8, p_mode=BME280.BME280_OSAMPLE_8, h_mode=BME280.BME280_OSAMPLE_8)

    def read(self):
        temperature = self.sensor.read_temperature()
        humidity = self.sensor.read_humidity()
        pressure = self.sensor.read_pressure() / 100
        data = [
            Reading(device='BME280', type='temperature', unit='celsius', address=self.address, value=temperature),
            Reading(device='BME280', type='humidity', unit='%', address=self.address, value=humidity),
            Reading(device='BME280', type='pressure', unit='hPa', address=self.address, value=pressure),
        ]
        return data


class SENSOR_BMP180:

    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

        # https://github.com/nickoala/sensor
        from sensor.BMP180 import BMP180
        self.sensor = BMP180(self.bus, self, address)

    def read(self):
        pressure, temperature = self.sensor.all()
        address = '{}/{}'.format(self.bus, self.address)
        data = [
            Reading(device='BMP180', type='temperature', unit='celsius', address=address, value=temperature.C),
            Reading(device='BMP180', type='pressure', unit='hPa', address=address, value=temperature.hPa),
        ]
        return data


class SENSOR_DHT11:

    def __init__(self, address):
        import Adafruit_DHT
        self.type = Adafruit_DHT.DHT11
        self.address = address

    def read(self):
        """
        Note that sometimes you won't get a reading and
        the results will be null (because Linux can't
        guarantee the timing of calls to read the sensor).
        If this happens try again!
        """
        # Adafruit_DHT.DHT11, 17
        import Adafruit_DHT
        humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT11, self.address)
        data = [
            Reading(device='DHT11', type='temperature', unit='celsius', address=self.address, value=temperature),
            Reading(device='DHT11', type='humidity', unit='%', address=self.address, value=humidity),
        ]
        return data


class SENSOR_DS18B20_SYSFS:

    def __init__(self, address):
        self.address = address

        # https://github.com/nickoala/sensor
        from sensor.DS18B20 import DS18B20
        self.sensor = DS18B20(self.address)

    def read(self):
        temperature = self.sensor.temperature()
        temperature_value = temperature.C
        if temperature_value == 85:
            raise BadReading('DS18B20 power-on value 85')

        data = [
            Reading(device='DS18B20', type='temperature', unit='celsius', address=self.address, value=temperature_value),
        ]
        return data


class SENSOR_DS18B20_OWFS:

    def __init__(self, address):
        self.address = address

        import ow
        ow.init('localhost:4304')
        self.sensor = ow.Sensor('/' + self.address)

    def read(self):
        temperature_value = self.sensor.temperature
        if temperature_value == 85:
            raise BadReading('DS18B20 power-on value 85')
        data = [
            Reading(device='DS18B20', type='temperature', unit='celsius', address=self.address, value=temperature_value),
        ]
        return data


class SENSOR_SDS011:
    """
    Example::

        sensor = SDS011('/dev/ttyUSB0')

    Derived from https://github.com/corny/luftdaten-python/blob/master/main.py
    """

    def __init__(self, address=None):
        self.address = address

        from sds011 import SDS011
        self.sensor = SDS011(self.address)

        # Set dutycyle to nocycle (permanent)
        self.sensor.dutycycle = 0

    def read(self):
        from sds011 import SDS011

        pm25_values = []
        pm10_values = []
        self.sensor.workstate = SDS011.WorkStates.Measuring
        try:
            for a in range(8):
                values = self.sensor.get_values()
                if values is not None:
                    pm10_values.append(values[0])
                    pm25_values.append(values[1])
        finally:
            self.sensor.workstate = SDS011.WorkStates.Sleeping

        pm25_value = mean(pm25_values)
        pm10_value = mean(pm10_values)

        data = [
            Reading(device='SDS011', type='particles-pm25', unit='unknown', address=self.address, value=pm25_value),
            Reading(device='SDS011', type='particles-pm10', unit='unknown', address=self.address, value=pm10_value),
        ]
        return data


class SENSOR_HX711:
    """
    See also https://pypi.org/project/hx711.
    """

    def __init__(self, dout_pin=5, pdsck_pin=6, channel='A', gain=64):
        self.address = 'dout={}, pdsck={}, channel={}'.format(dout_pin, pdsck_pin, channel)

        from hx711 import HX711

        # TODO: Obtain parameters from constructor.
        self.sensor = HX711(
            dout_pin=dout_pin,
            pd_sck_pin=pdsck_pin,
            channel=channel,
            gain=gain
        )

    def read(self):
        import RPi.GPIO as GPIO
        values = []
        try:
            # Before reading, reset the HX711 (not obligate).
            # FIXME: Really?
            self.sensor.reset()
            values = self.sensor.get_raw_data(num_measures=3)

        finally:
            # FIXME: Really?
            GPIO.cleanup()  # always do a GPIO cleanup in your scripts!

        value = mean(values)
        data = [
            Reading(device='HX711', type='weight', unit='kg', address=self.address, value=value),
        ]
        return data


class SENSOR_ABE_DELTA_SIGMA_ADC:

    def __init__(self, bus=None, address=None, address2=None, samplerate=None, gain=None, channels=None):

        self.address = '/'.join(map(str, [address, address2, samplerate, gain]))

        # Initialize the ADC device.
        self.device = Device_ABE_DeltaSigmaPiADC(address=address, address2=address2, samplerate=samplerate, gain=gain)

        # Add weight decoder to the pipeline.
        self.decoder = ADCWeightDecoder(source=self.device)

        # Read multiple devices multiple times.
        self.sensorreader = MultiSensorReader(source=self.decoder, channels=channels)

    def read(self):
        value = self.sensorreader.read()
        data = [
            Reading(device='ABE-DeltaSigma-ADC', type='weight', unit='kg', address=self.address, value=value),
        ]
        return data


class OWFSInfo:

    def info(self):
        # You can now start using OWFS to access your i2c devices and any connected sensors:
        # sudo /opt/owfs/bin/owfs --i2c=ALL:ALL --allow_other /mnt/1wire
        # for details check: https://www.abelectronics.co.uk/kb/article/3/owfs-with-i2c-support-on-raspberry-pi
        # starting owfs and logging sensors found to file
        import ow
        ow.init('localhost:4304')
        sensorlist = ow.Sensor('/').sensorList()
        for sensor in sensorlist:
            log.info("Device found: " +
                     "Type=" + sensor.type + " Family=" + sensor.family +
                     " Address=" + sensor.address + " ID=" + sensor.id)
