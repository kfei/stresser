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
            self.task = [{'task_name': parser.get('task', 'name'),
                          'task_type': parser.get('task', 'type'),
                          'task_url': parser.get('task', 'url')}]
        except NoOptionError:
            sys.exit(u'Task parse failed')

        try:
            self.wait_for_stop = parser.getint('task', 'count')
        except NoOptionError:
            sys.exit(u'Can not find setting for number of Soldiers')
