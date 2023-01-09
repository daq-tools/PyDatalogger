.. image:: https://img.shields.io/github/tag/daq-tools/pydatalogger.svg
    :target: https://github.com/daq-tools/pydatalogger

|

############
PyDatalogger
############

.. highlight: bash

*****
About
*****

Datalogger for SBC machines like BeagleBone, RaspberryPi or similar.


Supported sensor types
======================

- BME280
- BMP180
- DHT11
- DS18B20
- SDS011
- HX711
- ABE-DELTA-SIGMA-ADC


*****
Setup
*****
::

    git clone https://github.com/daq-tools/PyDatalogger.git
    cd PyDatalogger

    virtualenv --python=python3 .venv3
    source .venv3/bin/activate
    python setup.py develop


*****
Usage
*****
::

    $ pydatalogger --help

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


*******
Credits
*******

- `RPi-Beelogger`_ by Markus Hies, see `Beelogger Version 2`_
- `Hiverize-Sensorbeuten`_ by Hiverize_
- `luftdaten-python`_ for luftdaten.info sensor network
- BERadio_ by Hiveeyes_


**************
Other projects
**************

- `Terkin`_ is a flexible data logger application for MicroPython and CPython
  environments. It provides a lot of sensor-, networking- and telemetry-
  connectivity options.


.. _Beelogger Version 2: http://blog.hies.de/?p=281
.. _BERadio: https://github.com/hiveeyes/beradio
.. _Hiveeyes: https://hiveeyes.org
.. _Hiverize: https://hiverize.org/
.. _Hiverize-Sensorbeuten: https://github.com/hiveeyes/Hiverize-Sensorbeuten
.. _luftdaten-python: https://github.com/corny/luftdaten-python
.. _RPi-Beelogger: https://github.com/beelogger/RPi-Beelogger
.. _Terkin: https://github.com/hiveeyes/terkin-datalogger
