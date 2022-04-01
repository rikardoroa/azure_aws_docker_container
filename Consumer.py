# Script by rikardoroa
# just Python it!
import sys
from Publisher import Rabbitmq
from Bucket_creation import *
import boto3
import pika
from pika.exceptions import  ChannelWrongStateError,StreamLostError
import os
from botocore.exceptions import EndpointConnectionError
from threading import Thread
import threading

class BasicMessageReceiver(Rabbitmq, AWSBucket):

    def __init__(self, pika_connector=pika.ConnectionParameters()):
        Rabbitmq.__init__(self, Rabbitmq.pika_connector)
        self.pika_connector = Rabbitmq.pika_connector
        AWSBucket.__init__(self, AWSBucket.AWS_secret, AWSBucket.AWS_key, AWSBucket.AWS_region)
        self.Bucket = AWSBucket.Bucket
        self.secret = AWSBucket.AWS_secret
        self.key = AWSBucket.AWS_key
        self.region = AWSBucket.AWS_region
        self.session = boto3.Session(aws_access_key_id=self.key, aws_secret_access_key=self.secret, region_name=self.region)
        self.principal = AWSBucket.Principal
        self.resource = AWSBucket.Resource
        self.bucket = AWSBucket.Bucket



    def callback_(self):
        connection = pika.BlockingConnection(self.pika_connector)
        channel = connection.channel()
        try:
            msj = channel.queue_declare("channel")
            new_data = []
            s3 = self.session.client('s3')
            files = ['deaths.json', 'hadmissions.json', 'test.json']
            if msj.method.message_count >= 0:
                try:
                    print("Uploading files to the AWS S3 Bucket from Queue..to Exit press CTRL + C")
                    for method_frame, properties, body in channel.consume('channel'):
                        new_body = body.decode("utf8")
                        new_data.append(new_body)

                        for index, file in enumerate(zip(files, new_data)):
                            s3.put_object(Bucket=self.bucket, Body=new_data[index], Key=files[index])
                        print("Wrinting a file to the S3 Bucket please wait..")


                        if msj.method.message_count == len(new_data):

                            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                            channel = connection.channel()
                            channel.basic_consume(queue='channel', on_message_callback=callback, auto_ack=False)
                            print("Please wait the messages are consuming in Queue..")
                            channel.start_consuming()
                except EndpointConnectionError:
                    print("connection lost with AWS Server, Please Check your Internet connection")

            else:
                print("No messages in queue..exiting")
                self.channel.queue_delete("channel")
                self.channel.close()
                self.connection.close()


        except KeyboardInterrupt:
            channel.stop_consuming()
            channel.queue_delete("channel")
            channel.close()
            connection.close()
            print("You Press CTRL + C to exit..")

    def run_consume_queue(self):
        # Running all functions in the main module
        try:
            thread_one = threading.Thread(target=self.callback_)
            thread_one.start()
            thread_one.join()
            return thread_one
        except KeyboardInterrupt:
            print("You are exiting the program...")


def callback(ch, method, properties, body):
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("All messages consumed")
    except KeyboardInterrupt:
        print("You are exiting the program...")










