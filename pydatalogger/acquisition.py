# -*- coding: utf-8 -*-
# (c) 2018 The Hiveeyes Developers <hello@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import attr
import logging

log = logging.getLogger(__name__)


class AcquisitionEngine:

    def __init__(self, dry_run=False):
        self.sensors = []
        self.dry_run = dry_run

    def register_sensor(self, sensor):
        self.sensors.append(sensor)

    def get_readings(self):
        readings = []
        for sensor in self.sensors:
            readings += sensor.read()

        #log.info('Readings:\n%s', readings)

        return readings

    def get_readings_serialized(self):
        items = []
        for reading in self.get_readings():
            items.append(attr.asdict(reading))
        return items


@attr.s(auto_attribs=True)
class Reading:
    value: float
    type: str
    unit: str
    device: str
    address: str


class BadReading(Exception):
    pass
