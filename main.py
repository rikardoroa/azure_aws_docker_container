# Script by rikardoroa
# just Python it!
from flask import Flask, jsonify
from Azure_blobs_download import datasets_microservice
from Bucket_creation import AWSBucket
from Publisher import Rabbitmq
from Consumer import BasicMessageReceiver
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
consumer = datasets_microservice()
consumer_bucket = AWSBucket()
publish_queue = Rabbitmq()
consume_queue = BasicMessageReceiver()


@app.route('/')
def index():
    return 'Server is UP!!'


@app.route('/live')
def get_live():
    return jsonify({'status': 'ok'})


@app.route('/ready')
def get_ready():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    try:
        # consumer.setup()
        consumer.run_download_azure_blobs()
        consumer_bucket.run_bucket_creation_policy()
        publish_queue.run_publish_queue()
        consume_queue.run_consume_queue()
        # app.run()
        app.run(host="0.0.0.0", port=3000, debug=True)
    except KeyboardInterrupt:
        print("You Press CTRL + C to exit..")
