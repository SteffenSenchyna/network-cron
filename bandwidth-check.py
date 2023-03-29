import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
import time
from pymongo import MongoClient
import speedtest
from dotenv import load_dotenv
load_dotenv()
url = os.environ["MONGOURL"]
client = MongoClient(f'mongodb://{url}:27017/')
networkDB = client.network
bandwidthTable = networkDB.bandwidth
speed_test = speedtest.Speedtest()
counter = 0


def bytes_to_mb(bytes):
    KB = 1024  # One Kilobyte is 1024 bytes
    MB = KB * 1024  # One MB is 1024 KB
    return int(bytes/MB)


def bandwidthcheck():
    print("Performing bandwidth check")
    download_speed = bytes_to_mb(speed_test.download())
    upload_speed = bytes_to_mb(speed_test.upload())
    utc_now = pytz.utc.localize(
        datetime.utcnow()).strftime("%Y-%m-%d:%H-%M-%S")
    bandwidth = {
        "downloadSpeed": download_speed,
        "uploadSpeed":  upload_speed,
        "created_at": datetime.utcnow(),
    }
    print(bandwidth)
    try:
        result = bandwidthTable.insert_one(bandwidth)
        if result.acknowledged != True:
            print("Could not upload Syslog message to DB")

        print(f"Posted to DB with id {result.inserted_id}")

    except Exception as e:
        print(e)


bandwidthcheck()
