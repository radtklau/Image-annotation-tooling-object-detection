#author: Laurids Radtke 
#date: 18.12.21

import json
from centroidtracker import centroidtracker
import numpy as np

def main():
    track_ids_existing = 0
    track_ids_gen = 0
    track_ids_pre = []
    track_ids_post = []
    ct = centroidtracker(maxDisappearedNeighbor = 2, DISTANCE_TOLERANCE = 520, NEIGHBOR_TOLERANCE = (80,40))
    json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\annotations\\Iteration 4\\6401_almost_perf_track_ids_perf_bbox_vid_5_it_4.json'
    
    with open(json_file) as f:
        data = json.load(f)

    for ann in data['annotations']:
        track_ids_pre.append(ann['track_id'])
        if ann['track_id'] > 0:
            track_ids_existing += 1

    for img in data['images']: #go through every image
        rects = []
        classes = []
        img_annotations = []
        img_id = img['id']
        
        for ann in data['annotations']: #get annotation in image
            if img_id == ann['image_id']:
                    img_annotations.append([ann['category_id'], ann['bbox'], ann['id']])

        for info in img_annotations: #go through annotations of image
            box = np.asarray([info[1][0], info[1][1], info[1][0] + info[1][2], info[1][1] + info[1][3]])
            rects.append(box.astype("int"))
            classes.append(info[0])

        tracklets = ct.update(rects, classes)
        
        for track_id, centroid in tracklets.items():
            min_dist = (100000000,0)
            
            for ind,info in enumerate(img_annotations): #loop through annotations
                if (centroid[0] > info[1][0] and centroid[0] < info[1][0] + info[1][2]) and (centroid[1] > info[1][1] and centroid[1] < info[1][1] + info[1][3]): # centroid is in bbox
                    #calc dist to center
                    x_dist = ((info[1][0] + 0.5 * info[1][2]) - centroid[0]) #x 
                    y_dist = ((info[1][1] + 0.5 * info[1][3]) - centroid[1]) #y

                    if x_dist < 0:
                        x_dist *= -1
                    if y_dist < 0:
                        y_dist *= -1

                    dist = (x_dist + y_dist,ind)

                    if dist[0] < min_dist[0]:
                        min_dist = dist
                    
            for ann in data['annotations']:
                if ann['id'] == img_annotations[min_dist[1]][2]:
                    ann['track_id'] = track_id
                    track_ids_gen += 1
                    break             
            
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    for ann in data['annotations']:
        track_ids_post.append(ann['track_id'])

    with open('D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\annotations\\Iteration 4\\stats_iteration_4.txt', 'r+') as f: 
        stat_file = f.readlines()
        stat_file[25] = str(track_ids_pre) + "\n"
        stat_file[26] = str(track_ids_post) +"\n"

        f.seek(0)
        f.writelines(stat_file)
        f.truncate()

    print("track ids existing: "+str(track_ids_existing))
    print("track ids generated: "+str(track_ids_gen))
    
if __name__ == '__main__':
    main()