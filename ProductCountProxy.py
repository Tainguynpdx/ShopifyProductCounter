import requests
import time
import threading
from discord_webhook import DiscordEmbed, DiscordWebhook
import random

links = ['https://shop.palaceskateboards.com/', 'https://oqium.com/', 'https://www.dailypaperclothing.com/']
WebhookUrl = ' INSERT WEBHOOK'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

proxie_list = [
"http://ip1",
"http://ip2",
"http://ip3"
]

def post_discord(links, count):
    webhook = DiscordWebhook(url=WebhookUrl, username='Shopify Product Counter')
    embed = DiscordEmbed(title=(str(links)), url=links, description='New products added. Count: '+ '**' + (str(count)) +'**')
    embed.set_footer(text='Developed by DRB02#0001')
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()
    print('[SUCCESS] --> Successfully sent success webhook!')

def main(links):
    last_count = 0
    proxies = {
        'https': random.choice(proxie_list)
    }   
    while True:
        try:
            link = links + 'collections/all/count.json'
            api = requests.get(link, headers=headers, proxies=proxies).json()
            count = api['collection']['products_count']
            if count > last_count:
                last_count = count
                post_discord(links, count)
                
            else:
                print(link + ' No new products')
            time.sleep(30)
        except:
            link = links + 'collections/new/count.json'
            api = requests.get(link, headers=headers).json()
            count = api['collection']['products_count']
            if count > last_count:
                last_count = count
                post_discord(links, count)
            else:
                print(link + ' No new products')
            time.sleep(30)

if __name__ == "__main__":
    for i in links:
        threading.Thread(target=main,args=(i,)).start()
