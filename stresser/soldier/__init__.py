import sys
from ConfigParser import SafeConfigParser, NoOptionError


class Config(object):
    def __init__(self, config_file):
        parser = SafeConfigParser()
        parser.read(config_file)

        try:
            self.amqp_server = parser.get('amqp', 'server')
        except NoOptionError:
            sys.exit(u'Can not find AMQP message broker setting')

        try:
            self.java_bin = parser.get('bin', 'java_bin')
        except NoOptionError:
            self.java_bin = None

        try:
            self.sikuli_ide = parser.get('bin', 'sikuli_ide')
        except NoOptionError:
            self.sikuli_ide = None

        try:
            self.shell = parser.get('bin', 'shell')
        except NoOptionError:
            self.shell = None
