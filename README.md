# Network Cron Jobs
This repository houses python script that are meant to be executed on a cron schedule to monitor and interact with netwokring devices. This repository is part of a larger project, which includes several microservices and other components that collectively provide tools to manage on-premise networking devices. The view the cluster architecture and the CI/CD pipeline for deployment, refer to the [Cluster Manifest Repository](https://github.com/SteffenSenchyna/cluster-chart).


## Prerequisites
* Python 3.7 or later
* A MongoDB database
* A Discord channel 
* An AWS Account with access to an S3 bucket

## Getting Started
To run this application, follow these steps:

* Clone this repository
* Install the required packages using `pip install -r requirements.txt`
* Run a job by selecting a python script in the jobs/

## Jobs
### Network Backup
This job performs network backups for multiple devices and stores them in an AWS S3 bucket. It uses Napalm, a Python library that makes it easy to automate the configuration and management of network devices. This code is written for IOS network devices. However, the code can be easily modified to support other network devices.

#### Usage
To run the script, execute the following command:
```
python jobs\backup.py

```
The script has the following variable to determine which devices to backup:
```
ips = {
    "ips": [
        "192.0.2.1",
        "192.0.2.2",
        "192.0.2.3"
    ]
}
```

### Bandwidth Check
This job performs a bandwidth check using the Python library speedtest-cli and uploads the results to a MongoDB database.
#### Usage
To run the script, execute the following command:
```
python jobs\bandwidth.py

```
#### MongoDB Storage
Each bandwidth job is stored within the bandwidth database, the bandwidth data is stored in the following format:
```
{
  "downloadSpeed": download_speed,
  "uploadSpeed":  upload_speed,
  "created_at": datetime.utcnow(),
}
```
### Network Scan 
This job is a network scanner that performs an ICMP ping sweep on devices in a network to determine their availability status. It pulls the device list to ping from the NetBox library. If any devices are not reached a discord alert will be sent.
#### Usage
To run the script, execute the following command:
```
python jobs\scan.py
```
### Interface Scan
This job performs an SNMP (Simple Network Management Protocol) query on a set of devices and calculates their interface bandwidth utilization. The results are then stored in a MongoDB database.
#### Usage
To run the script, execute the following command:
```
python jobs\interface.py
```
#### MongoDB Storage
Each interface job is stored within the interface database in a collection corresponding to the devices IP address, the interface data is stored in the following format:
```
{
  "interfaces": ints_util,
  "created_at": datetime.utcnow()
}
```
Where ints_util is an array containing the bandwidth utilization for each interface witht he following format:
```
{
  "ifDescr" = <Interface Description>
  "ifType" = <Interface Type>
  "utilization" = <Bandwidth Utilization>
}
```
## Environmental Variables
Create a .env file in the root directory of the project and set the following environment variables:
```
AWS_ACCESS_KEY=<aws_access_key>
AWS_SECRET_KEY=<aws_secret_key>
NETBOXTOKEN=<netbox_token>
NETBOXURL=<netbox_url>
USERNAME=<network_device_username>
PASSWORD=<network_device_password>
SECRET=<network_device_secret>
```

