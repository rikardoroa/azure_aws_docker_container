# Script by rikardoroa
# just Python it!
import pika
from Azure_blobs_download import *
from pika.exceptions import AMQPConnectionError


class Rabbitmq:
    # pika connector attribute
    pika_connector = pika.ConnectionParameters(host='localhost')

    # init var and attribute
    def __init__(self, pika_connector=pika_connector):
        self.pika_connector = pika_connector


    def declare_queue(self, queue_name):
        #init queue connection an channel
        connection = pika.BlockingConnection(self.pika_connector)
        channel = connection.channel()
        try:
            print(f"Trying to declare queue({queue_name})...")
            channel.queue_declare(queue=queue_name)
            data = datasets_microservice.read_data_from_path()
            # sending the data to the queue
            for index, item in enumerate(data):
                message = pd.Series(data[index]).to_json(orient='records')
                channel.basic_publish(exchange="", routing_key="channel", body=message)
                print(f"Sent message.{message}")
        except AMQPConnectionError:
            print("Connection lost")


    def run_publish_queue(self):
        # Running all functions in the main module
        thread_one = threading.Thread(target=self.declare_queue("channel"))
        thread_one.start()
        thread_one.join()
        return thread_one

