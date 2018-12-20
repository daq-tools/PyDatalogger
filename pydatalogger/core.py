# -*- coding: utf-8 -*-
# (c) 2018 The Hiveeyes Developers <hello@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging
from importlib import import_module

from pydatalogger.acquisition import AcquisitionEngine
from pydatalogger.util import exception_traceback

log = logging.getLogger(__name__)


def make_engine(options, settings):

    #log.info('Settings:\n%s', settings)

    # The main workhorse.
    engine = AcquisitionEngine(
        dry_run=options['dry-run'],
    )

    sensor_library = import_module('pydatalogger.sensors')
    for sensor_name, sensor_options in settings.sensors.items():
        log.info('Registering sensor %s', sensor_name)
        try:
            factory = getattr(sensor_library, sensor_name)

            sensor_kwargs = sensor_options.parameters or {}
            sensor = factory(**sensor_kwargs)
            engine.register_sensor(sensor)
            log.info('Registering sensor %s succeeded', sensor_name)

        except Exception as ex:
            if options.debug:
                log.warning('Registering sensor %s failed: %s. Traceback:\n%s', sensor_name, ex, exception_traceback())
            else:
                log.warning('Registering sensor %s failed: %s', sensor_name, ex)

    return engine