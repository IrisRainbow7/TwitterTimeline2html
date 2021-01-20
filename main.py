from datetime import datetime,timedelta
import requests
from requests_oauthlib import OAuth1
import sys


USER_TIMELINE_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json?tweet_mode=extended"
HOME_TIMELINE_URL = "https://api.twitter.com/1.1/statuses/home_timeline.json?tweet_mode=extended"

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
DATA_COUNT = 200



auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

if CONSUMER_KEY == '' or CONSUMER_SECRET == '' or ACCESS_TOKEN == '' or ACCESS_SECRET == '':
    print('認証情報が設定されていません')
    sys.exit()


params = { "count": DATA_COUNT }

now = datetime.now()
filename = 'timeline{}.html'.format(now.strftime("%Y%m%d"))
url = HOME_TIMELINE_URL

if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 3 and sys.argv[1] == 'home':
    params['since_id'] = sys.argv[2]
elif len(sys.argv) == 3 and sys.argv[1] == 'user':
    url = USER_TIMELINE_URL
    params['screen_name'] = sys.argv[2]
    filename = 'user{}.html'.format(sys.argv[2])
else:
    print('引数エラー')
    sys.exit()

res = requests.get(url, params=params, auth=auth)

html = """\
<!doctype html>
<html>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">
</head>
<body>
"""

for t in res.json():
    dt = datetime.strptime(t['created_at'], '%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
    html += """
<div class="bg-gray-50 dark:bg-black p-10 flex items-center justify-center py-1">
<div class="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-800 p-4 rounded-xl border max-w-xl w-full">
<div class="flex justify-between">
<a href="{}">
<div class="flex items-center">
<img class="h-11 w-11 rounded-full" src="{}"/>
<div class="ml-1.5 text-sm leading-tight">
<span class="text-black dark:text-white font-bold block ">{}</span>
<span class="text-gray-500 dark:text-gray-400 font-normal block">@{}</span>
</div>
</div>
</a>
</div>
<p class="text-black dark:text-white block text-xl leading-snug mt-3">{}</p>
""".format("https://twitter.com/"+t['user']['screen_name'],
        t["user"]["profile_image_url_https"].replace("_normal",""),
        t["user"]["name"],
        t["user"]["screen_name"],
        t["full_text"],
        )

    if 'extended_entities' in t and 'media' in t['extended_entities']:
        for m in t['extended_entities']['media']:
            html += """\
<img class="mt-2 rounded-2xl border border-gray-100 dark:border-gray-700" src="{}"/>
""".format(m['media_url_https'])


    html += """\
<a href="{}">
<p class="text-gray-500 dark:text-gray-400 text-base py-1 my-0.5 text-right">{}</p>
</a>
</div>
</div>
""".format("https://twitter.com/{}/status/{}".format(t['user']['screen_name'], t['id_str']),
        dt.strftime("%Y/%m/%d %H:%M:%S")
        )

html += "</body>\n</html>"

with open(filename, mode='w') as f:
    f.write(html)
