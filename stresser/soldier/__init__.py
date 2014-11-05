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
            self.sikuli_cmd = parser.get('bin', 'sikuli_cmd')
        except NoOptionError:
            self.sikuli_cmd = None

        try:
            self.shell = parser.get('bin', 'shell')
        except NoOptionError:
            self.shell = None
