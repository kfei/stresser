#!/usr/bin/env python
import pika
import json
import sys

from stresser.commander import Config


class RpcClient(object):
    """
    Commander is RPC Client.
    """
    def __init__(self, config):
        # Get client configs
        self._config = config

        # Create a connection to AMQP server.
        conn = pika.ConnectionParameters(host=self._config.amqp_server)
        self.connection = pika.BlockingConnection(conn)

        # Get a channel from connection.
        self.channel = self.connection.channel()

        # Declare a result queue to store responses.
        self.channel.queue_declare(queue='q_result')
        self.result_queue = 'q_result'

        # Declare an exchange for dispatching tasks.
        # 'fanout' means broadcast.
        self.channel.exchange_declare(exchange='q_task', type='fanout')

        # Register on_response as the callback function when consuming
        # messages from result queue.
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.result_queue)

        # Initial the result list
        self.result_list = []

    def on_response(self, ch, method, props, body):
        """
        Collect the response messages from result queue.
        """
        # Deserialize and get informations from the RPC response.
        response = json.loads(body)[0]
        elapsed_time = response['elapsed_time']
        uuid = response['uuid']

        # Append each soldier's result to result list.
        result = " [.] Solider %s took %s to complete." % (uuid, elapsed_time)
        self.result_list.append(result)

        # Print out results and quit if all expected soldiers are completed.
        if len(self.result_list) == self._config.wait_for_stop:
            for r in self.result_list:
                print r
            sys.exit(0)

    def call(self, task):
        """
        Broadcast a task to soldiers by sending message via q_task exchange.
        """
        # Tell soldiers to send results to result queue.
        properties = pika.BasicProperties(reply_to=self.result_queue)

        self.channel.basic_publish(exchange='q_task', routing_key='',
                                   properties=properties, body=task)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        sys.exit(1)

    config = Config(config_file)
    rpc = RpcClient(config)

    # Request soldiers to run task.
    print " [x] Broadcasting task: '%s'..." % config.task['task_name']
    rpc.call(json.dumps(config.task))

    # Waiting for any messages from the result queue.
    rpc.channel.start_consuming()
