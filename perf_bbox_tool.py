#author: Laurids Radtke
#date: 13.01.2022
#This tool is for perfecting the bounding box information, so basecally you can draw a box on an image and it adds the annotation, it also gatheres statistical data and lets you remove boxes

import json
import cv2
import time


# mouse callback function
def draw_rectangle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        new_rect.append((x * 2,y * 2))
    elif event == cv2.EVENT_LBUTTONUP:
        new_rect.append((x * 2,y * 2)) #double it because image is scaled down

if __name__ == '__main__':
    start_time = time.time()
    correction_run = 1
    anno_last_img = 0

    total_boxes_cat_1 = 0 #1
    total_boxes_cat_2 = 0 #2

    total_del_box_cat_1 = 0 #3
    total_del_box_cat_2 = 0 #4

    total_added_box_cat_1 = 0 #5
    total_added_box_cat_2 = 0 #6

    sum_x_total_del_box_cat_1 = 0 #7
    sum_y_total_del_box_cat_1 = 0 #8

    sum_x_total_del_box_cat_2 = 0 #9
    sum_y_total_del_box_cat_2 = 0 #10

    sum_x_total_added_box_cat_1 = 0 #11
    sum_y_total_added_box_cat_1 = 0 #12

    sum_x_total_added_box_cat_2 = 0 #13
    sum_y_total_added_box_cat_2 = 0 #14

    total_corrected_box_cat_1 = 0 #15
    total_corrected_box_cat_2 = 0 #16

    sum_x_del_box_cat_1 = 0 #17
    sum_y_del_box_cat_1 = 0 #18

    sum_x_del_box_cat_2 = 0 #19
    sum_y_del_box_cat_2 = 0 #20

    sum_x_added_box_cat_1 = 0 #21
    sum_y_added_box_cat_1 = 0 #22

    sum_x_added_box_cat_2 = 0 #23
    sum_y_added_box_cat_2 = 0 #24

    last_used_ann_id_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Code\\laurids_code\\last_used_ann_id.txt'
    f = open(last_used_ann_id_file, 'r')
    ann_id = int(f.read())
    ann_id += 1 #because we read in last used
    f.close()
    new_rect = []
    json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\annotations\Iteration 4\\6401_imperf_track_ids_perf_bbox_vid_5_it_4.json'
    images_directory = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\images\\'
    statistics_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\annotations\\Iteration 4\\stats_iteration_4.txt'

    with open(json_file) as f:
        data = json.load(f)

    max_id = 0
    for i in data['images']:
        max_id = i['id']

    #######
    with open(statistics_file, 'r+') as f: #count total boxes
        stat_file = f.readlines()
        for anno in data["annotations"]: #1-2
                #1
                if anno["category_id"] == 1:    
                    total_boxes_cat_1 += 1
                #2
                if anno["category_id"] == 2:
                    total_boxes_cat_2 += 1

        stat_file[0] = str(total_boxes_cat_1) + "\n"
        stat_file[1] = str(total_boxes_cat_2) + "\n"

        f.seek(0)
        f.writelines(stat_file)
        f.truncate()
    #######

    im_id_left_off = 1
    f = 0
    for ind,image in enumerate(data['images']): #go through images
        if ind < 456:
            continue

        file_name = image['file_name']
        id = image['id']

        print("image "+str(ind)+"/"+str(len(data['images'])))
        
        with open(statistics_file, 'r+') as f:
            stat_file = f.readlines()
            lt = float(stat_file[24])
            t = time.time()
            stat_file[24] = str(lt + (t - start_time)) + "\n"
            start_time = t

            f.seek(0)
            f.writelines(stat_file)
            f.truncate()

        '''
        if ind == 0:
            a = data["annotations"][-1]["id"] #get ann id from last ann
            if a >= 6000: #if its new added ann
                ann_id = a + 1
                im_id_left_off = data["annotations"][-1]["image_id"] #change -1 if you want to start earlier not with the last annotation
        
        
        if id != im_id_left_off and f == 0:
            continue
        elif id == im_id_left_off:
            f = 1
        '''


        annotations_current_img  = list(filter(lambda annotation: annotation['image_id'] == id, data['annotations']))

        frame = cv2.imread(images_directory + file_name)
        height, width, channels = frame.shape
        cv2.setMouseCallback("frame",draw_rectangle)

        future_bbox_list = []
        if image['id'] < max_id - 10:
            future_img  = list(filter(lambda image: image['id'] == id + 10, data['images']))
            future_img_id = future_img[0]['id']
            annotations_future_img  = list(filter(lambda annotation: annotation['image_id'] == future_img_id, data['annotations']))
            if annotations_future_img:
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                for future_anno in annotations_future_img:
                    future_bbox_list.append(future_anno['bbox'])

        rect_flag = 0
        rm = [] #id of annotation to be removed
        k = 0
        while True:
            k += 1
            '''
            if cv2.waitKey(1) == ord('w'):
                if correction_run == 0:
                    correction_run = 1
                    print("correction_run == 1")
                elif correction_run == 1:
                    correction_run = 0
                    print("correction_run == 0")
            '''
            if annotations_current_img:
                if not anno_last_img:
                    time.sleep(1)
                    anno_last_img = 1
                else:
                    k = 1000
            else:
                k = 1000
                anno_last_img = 0

            for anno in annotations_current_img:
                bbox = anno['bbox'] 
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                color = (0, 255, 0)

                if len(new_rect) == 2: #check if new rect is in other bbox
                    if(new_rect[0][0] >= p1[0] and new_rect[1][0] >= p1[0] and new_rect[0][0] <= p2[0] and new_rect[1][0] <= p2[0] and
                    new_rect[0][1] >= p1[1] and new_rect[1][1] >= p1[1] and new_rect[0][1] <= p2[1] and new_rect[1][1] <= p2[1] and
                    abs(new_rect[0][0]-new_rect[1][0]) < 10 and abs(new_rect[0][1]-new_rect[1][1]) < 10): #has to be very small to delete
                        #remove annotation
                        
                        #######
                        if not correction_run: #3-4,7-10
                            with open(statistics_file, 'r+') as f:
                                stat_file = f.readlines()
                                if anno["category_id"] == 1:
                                    #3
                                    total_del_box_cat_1 = int(stat_file[2])
                                    total_del_box_cat_1 += 1
                                    stat_file[2] = str(total_del_box_cat_1) + "\n"
                                    #7
                                    sum_x_total_del_box_cat_1 = float(stat_file[6])
                                    sum_x_total_del_box_cat_1 += bbox[2]
                                    stat_file[6] = str(sum_x_total_del_box_cat_1) + "\n"
                                    #8
                                    sum_y_total_del_box_cat_1 = float(stat_file[7])
                                    sum_y_total_del_box_cat_1 += bbox[3]
                                    stat_file[7] = str(sum_y_total_del_box_cat_1) + "\n"

                                elif anno["category_id"] == 2:
                                    #4
                                    total_del_box_cat_2 = int(stat_file[3])
                                    total_del_box_cat_2 += 1
                                    stat_file[3] = str(total_del_box_cat_2) + "\n"
                                    #9
                                    sum_x_total_del_box_cat_2 = float(stat_file[8])
                                    sum_x_total_del_box_cat_2 += bbox[2]
                                    stat_file[8] = str(sum_x_total_del_box_cat_2) + "\n"
                                    #10
                                    sum_y_total_del_box_cat_2 = float(stat_file[9])
                                    sum_y_total_del_box_cat_2 += bbox[3]
                                    stat_file[9] = str(sum_y_total_del_box_cat_2) + "\n"

                                f.seek(0)
                                f.writelines(stat_file) 
                                f.truncate()
                        #######   
                        #######
                        if correction_run: #15-20
                            with open(statistics_file, 'r+') as f:
                                stat_file = f.readlines()
                                #15
                                if anno["category_id"] == 1:
                                    total_corrected_box_cat_1 = int(stat_file[14])
                                    total_corrected_box_cat_1 += 1
                                    stat_file[14] = str(total_corrected_box_cat_1) + "\n"
                                #16
                                elif anno["category_id"] == 2:
                                    total_corrected_box_cat_2 = int(stat_file[15])
                                    total_corrected_box_cat_2 += 1
                                    stat_file[15] = str(total_corrected_box_cat_2) + "\n"

                                if anno["category_id"] == 1:
                                    #17
                                    sum_x_del_box_cat_1 = float(stat_file[16])
                                    new_sum_x_del_box_cat_1 = (sum_x_del_box_cat_1 + bbox[2]) 
                                    stat_file[16] = str(new_sum_x_del_box_cat_1) + "\n"
                                    #18
                                    sum_y_del_box_cat_1 = float(stat_file[17])
                                    new_sum_y_del_box_cat_1 = (sum_y_del_box_cat_1 + bbox[3]) 
                                    stat_file[17] = str(new_sum_y_del_box_cat_1) + "\n"

                                elif anno["category_id"] == 2:
                                    #19
                                    sum_x_del_box_cat_2 = float(stat_file[18])
                                    new_sum_x_del_box_cat_2 = (sum_x_del_box_cat_2 + bbox[2]) 
                                    stat_file[18] = str(new_sum_x_del_box_cat_2) + "\n"
                                    #20
                                    sum_y_del_box_cat_2 = float(stat_file[19])
                                    new_sum_y_del_box_cat_2 = (sum_y_del_box_cat_2 + bbox[3]) 
                                    stat_file[19] = str(new_sum_y_del_box_cat_2) + "\n"

                                f.seek(0)
                                f.writelines(stat_file)
                                f.truncate() 
                        #######

                        rm.append(anno["id"]) 
                        new_rect.clear()
                        continue

                cv2.rectangle(frame, p1, p2, color=color, thickness=2)
                cv2.putText(frame, str(anno["category_id"]), (int(bbox[0]), int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=color, thickness=2)
                cv2.putText(frame, str(anno["id"]), (int(bbox[0]+50), int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=color, thickness=2)
                cv2.putText(frame, str(anno["track_id"]), (int(bbox[0]+50), int(bbox[1]-30)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=color, thickness=2)

            for future_bbox in future_bbox_list:
                p1 = (int(future_bbox[0]), int(future_bbox[1]))
                p2 = (int(future_bbox[0] + future_bbox[2]), int(future_bbox[1] + future_bbox[3]))
                color = (200, 200, 0)
                cv2.rectangle(frame, p1, p2, color=color, thickness=2)

            if rm: #there is something to remove
                print("removing annotation "+str(rm))
                new_data = dict()
                new_data['images'] = []
                new_data['annotations'] = []
                new_data['categories'] = []

                new_data['images'] = data['images']
                new_data['categories'] = data['categories']
                new_data['annotations'] = [obj for obj in data['annotations'] if obj['id'] not in rm] #everything but the annotation to be removed

                with open(json_file, 'w') as f:
                    json.dump(new_data, f, indent=4)

                with open(json_file) as f:
                    data = json.load(f)

                new_rect.clear() #if we remove something, we dont need to draw the rectangle or insert a new annotation
                rm.clear()              


            if len(new_rect) == 2: #there was a mouse event (rect has been drawn)
                rect_flag = 1
                cv2.rectangle(frame,new_rect[0], new_rect[1], (0, 255, 0), thickness=2)

            cv2.imshow("frame", cv2.resize(frame, (1024, 1024)))

            if rect_flag == 1: #add rect
                bbox_arr = []
                for section in data:
                    if section == "annotations":
                        if(new_rect[0][0] < new_rect[1][0]):
                            bbox_arr = [new_rect[0][0],new_rect[0][1],new_rect[1][0] - new_rect[0][0],new_rect[1][1] - new_rect[0][1]]
                            cat_id = 1 #left to right is hektometersign
                        elif(new_rect[0][0] > new_rect[1][0]):
                            bbox_arr = [new_rect[1][0],new_rect[1][1],new_rect[0][0] - new_rect[1][0],new_rect[0][1] - new_rect[1][1]]
                            cat_id = 2 #right to left is signalschirm

                        if not correction_run: #5-6, 11-14
                            with open(statistics_file, 'r+') as f:
                                stat_file = f.readlines()
                                
                                if cat_id == 1:
                                    #5
                                    total_added_box_cat_1 = int(stat_file[4])
                                    total_added_box_cat_1 += 1
                                    stat_file[4] = str(total_added_box_cat_1) + "\n"
                                    #11
                                    sum_x_total_added_box_cat_1 = float(stat_file[10])
                                    sum_x_total_added_box_cat_1 += bbox_arr[2]
                                    stat_file[10] = str(sum_x_total_added_box_cat_1) + "\n"
                                    #12
                                    sum_y_total_added_box_cat_1 = float(stat_file[11])
                                    sum_y_total_added_box_cat_1 += bbox_arr[3]
                                    stat_file[11] = str(sum_y_total_added_box_cat_1) + "\n"
                                
                                elif cat_id == 2:
                                    #6
                                    total_added_box_cat_2 = int(stat_file[5])
                                    total_added_box_cat_2 += 1
                                    stat_file[5] = str(total_added_box_cat_2) + "\n"
                                    #13
                                    sum_x_total_added_box_cat_2 = float(stat_file[12])
                                    sum_x_total_added_box_cat_2 += bbox_arr[2]
                                    stat_file[12] = str(sum_x_total_added_box_cat_2) + "\n"
                                    #14
                                    sum_y_total_added_box_cat_2 = float(stat_file[13])
                                    sum_y_total_added_box_cat_2 += bbox_arr[3]
                                    stat_file[13] = str(sum_y_total_added_box_cat_2) + "\n"

                                f.seek(0)
                                f.writelines(stat_file)
                                f.truncate() 

                        if correction_run: #21-24
                            with open(statistics_file, 'r+') as f:
                                stat_file = f.readlines()
                                if cat_id == 1:
                                    #21
                                    sum_x_added_box_cat_1 = float(stat_file[20])
                                    new_sum_x_added_box_cat_1 = (sum_x_added_box_cat_1 + bbox_arr[2]) 
                                    stat_file[20] = str(new_sum_x_added_box_cat_1) + "\n"
                                    #22
                                    sum_y_added_box_cat_1 = float(stat_file[21])
                                    new_sum_y_added_box_cat_1 = (sum_y_added_box_cat_1 + bbox_arr[3]) 
                                    stat_file[21] = str(new_sum_y_added_box_cat_1) + "\n"

                                elif cat_id == 2:
                                    #23
                                    sum_x_added_box_cat_2 = float(stat_file[22])
                                    new_sum_x_added_box_cat_2 = (sum_x_added_box_cat_2 + bbox_arr[2]) 
                                    stat_file[22] = str(new_sum_x_added_box_cat_2) + "\n"
                                    #24
                                    sum_y_added_box_cat_2 = float(stat_file[23])
                                    new_sum_y_added_box_cat_2 = (sum_y_added_box_cat_2 + bbox_arr[3]) 
                                    stat_file[23] = str(new_sum_y_added_box_cat_2) + "\n"

                                f.seek(0)
                                f.writelines(stat_file) 
                                f.truncate()
                            #end


                        print("ann_id "+str(ann_id)+"cat_id "+str(cat_id))
                        new_ann = {"category_id": cat_id,
                        "image_id": id,
                        "id": ann_id,
                        "iscrowd": 0,
                        "bbox": bbox_arr,  
                        "track_id": -1}

                        ann_id += 1

                        data[section].append(new_ann)

                new_rect.clear()
                rect_flag = 0

                with open(json_file, 'w') as f:
                    json.dump(data, f, indent=4)

                with open(last_used_ann_id_file, 'w') as f:
                    f.write(str(ann_id))

            if cv2.waitKey(1) == ord('q') and k > 999:
                break
        

        if cv2.waitKey(20) == ord('x'):
            break

    cv2.destroyAllWindows()







