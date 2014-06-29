from ConfigParser import SafeConfigParser


class Config(object):
    def __init__(self, config_file):
        parser = SafeConfigParser()
        parser.read(config_file)

        self.amqp_server = parser.get('amqp', 'server')
        self.java_bin = parser.get('bin', 'java_bin')
        self.sikuli_ide = parser.get('bin', 'sikuli_ide')
        self.shell = parser.get('bin', 'shell')
