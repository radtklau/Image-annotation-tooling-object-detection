import time
import json

json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Eval 2\\6109_imperf_track_ids_perf_bbox_vid_4_eval_2.json'

with open(json_file) as f:
    data = json.load(f)

id = 6000
for ann in data['annotations']:
    ann['id'] = id
    id += 1

with open(json_file, 'w') as f:
    json.dump(data, f, indent=4)