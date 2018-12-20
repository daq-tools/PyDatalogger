# -*- coding: utf-8 -*-
# (c) 2018 The Hiveeyes Developers <hello@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import sys
import yaml
import logging
import traceback

from munch import Munch, munchify
from six import StringIO


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-30s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)

    # TODO: Control debug logging of HTTP requests through yet another commandline option "--debug-http" or "--debug-requests"
    requests_log = logging.getLogger('requests')
    requests_log.setLevel(logging.WARN)


def normalize_options(options):
    normalized = {}
    for key, value in options.items():
        key = key.strip('--<>')
        normalized[key] = value
    return munchify(normalized)


def read_list(data, separator=u','):
    if data is None:
        return []
    result = list(map(lambda x: x.strip(), data.split(separator)))
    if len(result) == 1 and not result[0]:
        result = []
    return result


def exception_traceback(exc_info=None):
    """
    Return a string containing a traceback message for the given
    exc_info tuple (as returned by sys.exc_info()).

    from setuptools.tests.doctest
    """

    if not exc_info:
        exc_info = sys.exc_info()

    # Get a traceback message.
    excout = StringIO()
    exc_type, exc_val, exc_tb = exc_info
    traceback.print_exception(exc_type, exc_val, exc_tb, file=excout)
    return excout.getvalue()


def to_list(obj):
    """Convert an object to a list if it is not already one"""
    if not isinstance(obj, (list, tuple)):
        obj = [obj, ]
    return obj


def mean_general(numbers):
    """
    Calculate arithmetic mean.
    https://stackoverflow.com/questions/7716331/calculating-arithmetic-mean-one-type-of-average-in-python/7716358#7716358
    """
    return float(sum(numbers)) / max(len(numbers), 1)


def mean_python3(numbers):
    """
    Calculate arithmetic mean.
    https://stackoverflow.com/questions/7716331/calculating-arithmetic-mean-one-type-of-average-in-python/20820148#20820148
    """
    import statistics
    return statistics.mean(numbers)


mean = mean_python3


def load_configuration(configfile):
    if configfile is None:
        configfile = 'pydatalogger.yml'
    with open(configfile, 'r') as ymlfile:
        config = munchify(yaml.load(ymlfile))
        return config
