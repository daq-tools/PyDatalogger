# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [

    # Core
    'six==1.11.0',
    'appdirs==1.4.3',
    'docopt==0.6.2',
    'attrs==18.2.0',
    'munch==2.3.2',
    'pyyaml==3.13',

    # Sensor adapters (sources)
    'sensor==5',
    'hx711==1.1.2.3',

    # Data output adapters (sinks)
    'paho-mqtt==1.4.0',

]

extras = {
    'test': [
        'pytest==4.0.1',
        'pytest-cov==2.6.0',
    ],
}

setup(name='pydatalogger',
      version='0.0.0',
      description='PyDatalogger - Data logging made easy',
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: System :: Networking :: Monitoring",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
      author='The Hiveeyes Developers',
      author_email='hello@hiveeyes.org',
      url='https://github.com/daq-tools/PyDatalogger',
      keywords='datalogger data logger acquisition',
      packages=find_packages(),
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      test_suite='pydatalogger.test',
      install_requires=requires,
      extras_require = extras,
      tests_require=extras['test'],
      dependency_links=[
      ],
      entry_points={
          'console_scripts': [
              'pydatalogger = pydatalogger.commands:run',
          ],
      },
)
