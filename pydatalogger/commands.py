# -*- coding: utf-8 -*-
# (c) 2018 The Hiveeyes Developers <hello@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import sys
import json
import logging
from docopt import docopt
from pydatalogger import __appname__, __version__, core
from pydatalogger.telemetry import TelemetryEngine
from pydatalogger.util import normalize_options, setup_logging, load_configuration

log = logging.getLogger(__name__)


def run():
    """
    Usage:
      pydatalogger info
      pydatalogger readings [--config=<config>] [--target=<target>]... [--dry-run] [--debug]
      pydatalogger --version
      pydatalogger (-h | --help)

    Options:
      --config=<config>             Configuration file for runtime settings
      --target=<target>             Data output target
      --version                     Show version information
      --dry-run                     Skip publishing to MQTT bus
      --debug                       Enable debug messages
      -h --help                     Show this screen

    Examples:

      # Display readings in JSON format
      pydatalogger readings

      # Publish readings to MQTT broker on localhost
      pydatalogger readings --target=mqtt://localhost/testdrive

      # Publish readings to MQTT broker on remote host
      pydatalogger readings --target=mqtt://daq.example.org/testdrive

    """

    # Parse command line arguments
    options = normalize_options(docopt(run.__doc__, version=__appname__ + ' ' + __version__))

    # Setup logging
    debug = options.get('debug')
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    log.debug('Options: {}'.format(json.dumps(options, indent=4)))

    # Default output target is STDOUT.
    if not options['target']:
        options['target'] = ['json+stream://sys.stdout']

    settings = load_configuration(options['config'])

    # Register sensors with acquisition engine.
    engine = core.make_engine(options, settings)

    # Acquire data.
    if options['readings']:
        log.info('Will publish readings to {}'.format(options['target']))
        data = engine.get_readings()
        log.info('Acquired readings: %s', data)

    # Sanity checks.
    if data is None:
        log.error('No data to process')
        sys.exit(2)

    # Create and run output processing engine.
    engine = TelemetryEngine(options['target'], options.get('dry-run', False))
    engine.process(data)
