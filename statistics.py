#author: Laurids Radtke 
#date: 16.01.22

import json

json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\annotations\\Iteration 4\\6401_perf_track_ids_perf_bbox_vid_5_it_4.json'

with open(json_file) as f:
        data = json.load(f)

count = 0
for ann in data['annotations']:
        count+= 1

count_img = 0
for img in data['images']:
        count_img += 1

print(count)
print(count_img)
print(count/count_img)