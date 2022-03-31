# Script by rikardoroa
# just Python it!
import threading
import pandas as pd
from azure.storage.blob import BlobServiceClient, ContainerClient
import os
import re
import glob
import json
import numpy as np
from dotenv import load_dotenv

load_dotenv()


class datasets_microservice:
     # regex pattern
    pattern = r'[a-z]{1,20}.csv'
    # credentials
    key = os.getenv('Key_Blob')
    cuenta = os.getenv('Account')
    sas_credential = os.getenv('sas_credential')
    contenedor = os.getenv('Container')
    input_container = os.getenv('Input_container')
    conn = os.getenv('conn_string')


    # var initialization
    def __init__(self, pattern=pattern, key=key,
                 cuenta=cuenta, sas_credential=sas_credential,
                 contenedor=contenedor, input_container=input_container, conn=conn):
        self.pattern = pattern
        self.key = key
        self.cuenta = cuenta
        self.sas_credential = sas_credential
        self.contenedor = contenedor
        self.input_container = input_container
        self.conn = conn

    def get_blob_from_azure(self):
        # list of files in the container
        container = ContainerClient.from_connection_string(conn_str=self.conn, container_name=self.input_container)
        blob_list = []
        blob_name = []
        [blob_list.append(blob.name) for blob in container.list_blobs()]
        blob = [re.findall(self.pattern, item) for item in blob_list[1:]]
        [blob_name.append(subitem[0]) for subitem in blob]
        # iterating through blob containers
        for blobname in blob_name:
            # connection
            blob_service_client_instance = BlobServiceClient(account_url=f"{self.cuenta}.blob.core.windows.net",  credential=self.key)
            blob_client_instance = blob_service_client_instance.get_blob_client(self.contenedor, blobname, snapshot=None)
            # downloading data from blob container
            blob_data = blob_client_instance.download_blob().readall()
            # writing blob files
            with open(blobname, "wb") as my_blob:
                file = my_blob.write(blob_data)
                print("writing files:", f'{file}')
        print('Data downloaded from Azure blob storage account')

    @staticmethod
    def read_data_from_path():
        path = os.path.abspath("*.csv")
        csv_files = []
        cols = []
        payload = []
        [csv_files.append(files) for files in glob.glob(path)]
        for csv in csv_files:
            read_csv_file = pd.read_csv(csv, encoding="latin1", sep="\t")
            for col in read_csv_file.columns:
                cols.append(col)
        cols = [re.sub('[^a-zA-Z0-9_]', ',', item) for item in cols]
        cols = [item.replace(",,,", "") for item in cols]
        cols = [item.split(",") for item in cols]
        cols = [list(dict.fromkeys(items)) for items in cols]
        for index, item in enumerate(zip(cols, csv_files)):
            my_data = pd.read_csv(csv_files[index], encoding="latin1", sep=",", skiprows=2, names=cols[index], dtype="object")
            json_data = my_data.apply(lambda row: json.loads(row.to_json()), axis=1)
            payload.append(json_data)
        array_payload = np.asarray(payload, dtype=object)
        return array_payload


    def run_download_azure_blobs(self):
        thread_one = threading.Thread(target=self.get_blob_from_azure)
        thread_one.start()
        thread_one.join()
        thread_two = threading.Thread(target=datasets_microservice.read_data_from_path)
        thread_two.start()
        thread_two.join()
        return thread_one, thread_two
