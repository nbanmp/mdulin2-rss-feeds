# from rfeed import rfeed
from datetime import datetime, timezone
from dateutil import tz
import requests
import json
from feedgen.feed import FeedGenerator

utc = tz.gettz('UTC')

fg = FeedGenerator()

r = requests.get("https://maxwelldulin.com/api/resources/getResources?page=1&per=1000&search=")
resources = json.loads(r.text)

for item in resources["Resources"]:
    fe = fg.add_entry()
    fe.id(item['URL'])
    fe.link(href=item['URL'])
    fe.description("\n".join(item['Descriptions']))
    fe.title(item["Title"])
    fe.author(name=item['HackerGroup'])
    fe.pubDate(datetime.fromisoformat(item['Date'].replace('Z', '+00:00')))

fg.title("Maxwell Dulin's Resources")
fg.author({'name': 'Maxwell Dulin', 'email': 'dulinmax@outlook.com'})
fg.link(href="https://maxwelldulin.com/Resources")
fg.subtitle('People often ask me "How did you learn how to hack?" The answer: by reading. This page is a collection of the blog posts and other articles that I have accumulated over the years of my journey. Enjoy!')
fg.language("en-US")

fg.lastBuildDate(datetime.now(timezone.utc))

fg.rss_file('resources-rss.xml')
fg.rss_file('resources-atom.xml')

print("Resource feed created!")

fg = FeedGenerator()

# Is there a way to get more than the last 5 blog posts in one request?
r = requests.post("https://maxwelldulin.com/api/blog/order/0")
blogs = json.loads(r.text)

for item in blogs["choppedlist"]:
    fe = fg.add_entry()
    url = "https://maxwelldulin.com/BlogPost?post=" + item['ID']["N"]
    fe.id(url)
    fe.link(href=url)
    fe.description(item['info']['M']['post']['S'])
    fe.title(item['info']['M']['title']['S'])
    fe.author(name="Maxwell Dulin")
    month, day, year = [int(x) for x in item['info']['M']['ddate']['S'].split('/')]
    fe.pubDate(datetime(year, month, day, tzinfo=utc))

fg.title("Maxwell Dulin's Blog")
fg.author({'name': 'Maxwell Dulin', 'email': 'dulinmax@outlook.com'})
fg.link(href="https://maxwelldulin.com/Blog")
fg.subtitle("ꓘ's 1337 blog")
fg.language("en-US")

fg.rss_file('blog-rss.xml')
fg.rss_file('blog-atom.xml')

print("Blog feed created!")
