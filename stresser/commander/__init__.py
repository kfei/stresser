from ConfigParser import SafeConfigParser


class Config(object):
    def __init__(self, config_file):
        parser = SafeConfigParser()
        parser.read(config_file)

        self.task = [{'task_name': parser.get('task', 'name'),
                 'task_type': parser.get('task', 'type'),
                 'task_url': parser.get('task', 'url')}]
        self.wait_for_stop = parser.getint('task', 'count')
        self.amqp_server = parser.get('amqp', 'server')
