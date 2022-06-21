import json
import cv2
import csv
import os
from centroidtracker import centroidtracker
import numpy as np

directory = r"D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\BA\Datasets\\6098\\images"
info_read = r"D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6098\\topodot_corrected_landmarks_ocr_original.json"
info_write = r"D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6098\\topodot_corrected_landmarks_ocr_original_tracking_ids.json"
csv_file = r"D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6098\\lst_converted_reference_3.csv"
reverse = True

def main(maxDisappearedNeighbor = 2, DISTANCE_TOLERANCE = 520, NEIGHBOR_TOLERANCE = (80, 40)):
    track_arr = [[],[]]
    top_cat_ids = [70,89,72,87,90]
    ct = centroidtracker(maxDisappearedNeighbor = maxDisappearedNeighbor, DISTANCE_TOLERANCE = DISTANCE_TOLERANCE, NEIGHBOR_TOLERANCE = NEIGHBOR_TOLERANCE)
    with open(csv_file, 'r') as file, open(info_read) as json_file:
        reader = csv.reader(file)
        data = json.load(json_file)
        file_names = os.listdir(directory)

        for i, row in enumerate(reader): # (l) enumerate images in right sequence (like a video)
            if i < 68: #(l) why ignore first 68 images?
                continue
            for file in file_names:
                if row[1] in file:
                    name = file
            frame = cv2.imread(directory + "\\" + name)
            for image in data["images"]: #(l) go through images
                if image["file_name"] == name:
                    img_id = image["id"]
            rects = []
            classes = []
            ann_ids = []
            cat_ids = []
            for ann in data["annotations"]: #(l) go through annotations
                if ann["image_id"] == img_id: #(l) stop at every annotation that appears on our image
                    ann_id = ann["id"]
                    cat_id = ann["category_id"]
                    ann_ids.append(ann_id) #(l) safe ann ids for this image
                    cat_ids.append(cat_id) #safe cat ids for this images annotations
                    x = int(ann["bbox"][0])
                    y = int(ann["bbox"][1])
                    w = int(ann["bbox"][2])
                    h = int(ann["bbox"][3])
                    box = np.asarray([x, y, x + w, y + h])
                    rects.append(box.astype("int")) #(l) detection data
                    classes.append(ann["category_id"]) #(l) type of object
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #(l) draw rectangle on image
            objects = ct.update(rects, classes) #(l) pass detection data/boxes to centroid tracker, returns dict where key is tracking id and value is centroid (x,y coordinates)

            for (objectID, centroid) in objects.items(): #(l) TODO: manchmal mehr dict einträge als ann ids, sehr komisch. 
                for k,ann_id in enumerate(ann_ids): #for every ann_id of current image
                    bbox_info = []
                    for ann in data["annotations"]: #find bounding box info for annotation
                        if ann["id"] == ann_id:
                            for i in range(4):
                                bbox_info.append(int(ann["bbox"][i])) #safe bounding box info in list
                    
                    if centroid[0] > bbox_info[0] and centroid[0] < (bbox_info[0]+bbox_info[2]): #x
                        if centroid[1] > bbox_info[1] and centroid[1] < (bbox_info[1]+bbox_info[3]): #y
                            while objectID >= len(track_arr):
                                track_arr.append([])
                            if len(track_arr[objectID]) == 0 and cat_ids[k] not in top_cat_ids: #new object which is not in top 5 categories
                                track_arr[objectID].append("x")
                            elif len(track_arr[objectID]) != 0 and track_arr[objectID][0] == "x":
                                continue
                            else:
                                track_arr[objectID].append(ann_id)
                            break
                        else:
                            continue
                    else:
                        continue
                '''      
                text = "ID {}".format(objectID)
                text2 = img_id
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 3)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (255, 255, 255), -1)
                cv2.putText(frame, str(text2), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 3)
    
            cv2.imshow("frame", cv2.resize(frame, (1600, 1200)))
            if cv2.waitKey(0) == ord('q'):
                break
            cv2.destroyAllWindows()
            '''
    track_arr = [x for x in track_arr if x != ["x"]]
    l = 0
    for index, ann_ls in enumerate(track_arr):
        l += len(ann_ls)
        for ann in data["annotations"]:
            if ann["id"] in ann_ls:
                print("adding index")
                ann["track_id"] = index

    print(l)

    #with open(info_write, 'w') as json_file:
        #json_file.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))

    '''        
    with open('tracking_data.txt', 'w') as f:
        for track_id,ann_id in enumerate(track_arr):
            f.write(str(track_id))
            f.write(': ')
            f.write(str(ann_id))
            f.write('\n')
    '''
if __name__ == "__main__":
   main()
