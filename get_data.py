#!/usr/bin/env python
# coding: utf-8

# pid is the identifier of podcast host


############修改代码中这个pid即可################
PID='5e61155b418a84a046401f72' 
###################################

# import support libraries
import requests
from pyquery import PyQuery as pq

# get raw data
url = "https://www.xiaoyuzhoufm.com/podcast/{}".format(PID)
req = requests.get(url, timeout=30) 

html=req.content
raw_data=str(html,'utf-8')
#print(raw_data)

# get eid_index in raw_data
eid_index = [i for i in range(len(raw_data)) if raw_data.startswith('eid', i)]

# create list to store eid, eid is the identifier of each episode
eid_list = []

# get eid
for val in eid_index:
    eid_list.append(raw_data[val+6:val+30])


#podcast_name = {'title'}
field_names = {'pid','title', 'clapCount', 'commentCount', 'playCount', 'favoriteCount', 'pubDate', 'duration'}
data = []
for val in eid_list:
    # get url of episode
    each_episode_url = "https://www.xiaoyuzhoufm.com/_next/data/_Zwl7i3GWwo-JWx5km6lh/episode/{}.json".format(val)
    fh = requests.get(each_episode_url)
    json_data = fh.json()
    
    
    # find specific statistic we want
    #p1 = {key: value for key, value in json_data['pageProps']['episode']['podcast'].items() if key in podcast_name}
    #data.append(p1)
    
    p2 = {key: value for key, value in json_data['pageProps']['episode'].items() if key in field_names}
    data.append(p2)



# convert to csv file
import csv 
info = ['pid','title', 'clapCount', 'commentCount', 'playCount', 'favoriteCount', 'pubDate', 'duration']
with open('fm_data.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = info)
    writer.writeheader()
    writer.writerows(data)





    