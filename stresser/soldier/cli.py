#!/usr/bin/env python
import pika
import json
import sys
import uuid
from time import clock
from datetime import timedelta

from stresser.soldier import Config
from stresser.soldier.task import Task


class RpcServer(object):
    """
    Soldier is RPC Server.
    """
    def __init__(self, config):
        # Get server configs
        self._config = config

        # Create a connection to AMQP server.
        conn = pika.ConnectionParameters(host=self._config.amqp_server,
                                         connection_attempts=3,
                                         retry_delay=3)
        self.connection = pika.BlockingConnection(conn)

        # Get a channel from connection.
        self.channel = self.connection.channel()

        # Declare a random queue to listen task requests.
        result = self.channel.queue_declare(exclusive=True)
        self.listend_queue = result.method.queue

        # Bind it to the 'q_task' exchange.
        self.channel.exchange_declare(exchange='q_task', type='fanout')
        self.channel.queue_bind(exchange='q_task', queue=self.listend_queue)

        # Generate an UUID for each soldier.
        self.uuid = str(uuid.uuid4())

    def on_request(self, ch, method, props, body):
        task = Task(body)

        print " [.] Discovered task '%s'" % task.task_name
        print " [.] Downloading task executable from %s" % task.task_url
        # Download the task's executable
        task.get_executable(task.task_url)

        # Start timer.
        start = clock()

        # Start running task.
        print " [.] Running task: '%s'" % task.task_name
        result = task.start(self._config)
        print " [.] Task: '%s' is completed" % task.task_name

        # Calculation.
        elapsed_time = str(timedelta(seconds=(int(clock() - start))))

        # Send response back to commander.
        response = [{'uuid': self.uuid,
                     'result': result,
                     'elapsed_time': elapsed_time}]
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         body=json.dumps(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        sys.exit(1)

    config = Config(config_file)
    rpc = RpcServer(config)

    rpc.channel.basic_qos(prefetch_count=1)
    rpc.channel.basic_consume(rpc.on_request, queue=rpc.listend_queue)

    print " [x] Soldier %s is awaiting RPC requests" % rpc.uuid
    rpc.channel.start_consuming()


if __name__ == '__main__':
    main()
