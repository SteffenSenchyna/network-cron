import datetime
import json
import os
import pytz
from flask import Response
import napalm
import boto3
from dotenv import load_dotenv


def putS3(hostname, config):
    session = boto3.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
        aws_secret_access_key=os.environ["AWS_SECRET_KEY"]
    )
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    formated_date = utc_now.strftime("%Y-%m-%dT%H-%M-%S")
    s3_client = session.resource("s3")
    s3_object = s3_client.Object(
        "networkbackups", f'{hostname}/{formated_date}.txt')
    try:
        result = s3_object.put(Body=(config))
        return result
    except Exception as e:
        print(str(e))
        return e


def postBackup(request):
    load_dotenv()
    ips = request.get_json()["ips"]
    print(ips)
    driver = napalm.get_network_driver('ios')
    for i in ips:
        device = driver(hostname=i, username=os.environ["USERNAME"], password=os.environ["PASSWORD"], optional_args={
                        'secret': os.environ["SECRET"]})
        try:
            device.open()
            hostname = device.get_facts()['hostname']
            config = device.get_config()['running']
            device.close()
            putS3(hostname, config)
        except Exception as e:
            print(str(e))
            return Response(str(e), status=400)

    return Response("Succesfully posted all backups to S3", status=201)


class Request:
    def __init__(self, payload):
        self.payload = payload

    def get_json(self):
        return json.loads(self.payload)


ips = {
    "ips": [
        "10.0.5.21",
        "10.0.5.22",
        "10.0.5.31",
        "10.0.5.32"
    ]
}
request_string = json.dumps(ips)

request = Request(request_string)
postBackup(request)
