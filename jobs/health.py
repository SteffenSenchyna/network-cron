import os
import subprocess
import threading
from dotenv import load_dotenv
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed


def getScan():
    print("Performing health check")
    load_dotenv()
    discordURL = os.environ["DISCORDURL"]
    netboxURL = os.environ["NETBOXURL"]
    NETBOXTOKEN = os.environ["NETBOXTOKEN"]
    url = f"http://{netboxURL}/api/dcim/devices/?site_id=4"
    threads = []
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Token {NETBOXTOKEN}"
    }

    response = requests.get(url, headers=headers).json()
    response = response["results"]
    # with open("devices.json", "w") as outfile:
    #     json.dump(response, outfile)
    downHosts = []

    def ping(ip, host, downHosts):
        result = subprocess.run(
            ['ping', '-c', '1', "-W", "200", ip], stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            host["ping_status"] = "up"
        else:
            host["ping_status"] = "down"
            downHosts.append(host["name"])

    try:
        for i in response:
            ip = i["primary_ip4"]["address"].split("/")
            t = threading.Thread(target=ping, args=(
                ip[0], i, downHosts))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        if len(downHosts) > 0:
            print(f"The following devices could not be reached {downHosts}")
            webhook = DiscordWebhook(
                url=discordURL)
            embed = DiscordEmbed(
                title='Network Event', description='The following network devices management IPs cannot be pinged', color='03b2f8')
            embed.set_author(name='NetBot',
                             icon_url='https://avatars0.githubusercontent.com/u/14542790')
            embed.set_footer(text='Down Network Devices')
            embed.set_timestamp()
            embed.add_embed_field(name='Devices', value=str(downHosts)[1:-1])
            # add embed object to webhook
            webhook.add_embed(embed)
            response = webhook.execute()
    except Exception as e:
        print(e)


getScan()
