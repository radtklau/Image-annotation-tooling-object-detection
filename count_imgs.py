import json
json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\annotations\\Eval 1\\6401_perfect_track_ids_perfect_bbox_vid_3_eval_1.json'

with open(json_file) as f:
    data = json.load(f)

c = 0
for img in data["images"]:
    c += 1

print(c)