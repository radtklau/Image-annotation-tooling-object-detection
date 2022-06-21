#author: Laurids Radtke
#date: 12.01.2022
#This tool is written to help manually remove errors the auto annotation did and make the annotation perfect so it can be used for machine learning
#Navigation: p = forward, ö = backward, ä = next annotation, l = previous annotation, ü = exit, k = insert new track id

import json
import cv2
import keyboard

if __name__ == '__main__':

    total_track_ids = 0
    highest_track_id = 0
    individual_track_ids = 0
    pre_track_id_list = []
    post_track_id_list = []
    added_track_id_list = []
    corrected_track_id_list = []
    total_track_ids_corrected = 0
    total_track_ids_added = 0
    individual_track_ids_added = 0
    individual_track_ids_corrected = 0
    total_track_ids_post = 0
    individual_track_ids_post = 0
    new_track_id = 1

    json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Iteration 1\\6109_imperf_track_ids_2cats_perf_bbox_vid_2 copy.json'
    images_directory = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\images\\'


    with open(json_file) as f:
        data = json.load(f)

    file_name_arr = []
    for image in data['images']:
        file_name = image['file_name']
        id = image['id']
        file_name_arr.append((file_name,id))
        
    img_index = 0
    aux = 0
    forward_flag = 0
    backward_flag = 0
    exit_flag = 0

####### 30,31,35
    for anno in data['annotations']:
        if anno['track_id'] >= 0:
            total_track_ids += 1
            if anno['track_id'] > highest_track_id:
                highest_track_id = anno['track_id']

    for i in range(highest_track_id + 1):
        pre_track_id_list.append(0)
    
    for anno in data['annotations']:
        if anno['track_id'] >= 0:
            track_id = anno['track_id']
            pre_track_id_list[track_id] += 1

    for i in pre_track_id_list:
        if i > 0:
            individual_track_ids += 1
    
    with open('D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Iteration 1\\stats_iteration_1 copy.txt', 'r+') as f:
        stat_file = f.readlines()
        stat_file[29] = str(total_track_ids) + "\n"
        stat_file[30] = str(individual_track_ids) + "\n"
        stat_file[34] = str(pre_track_id_list) + "\n"

        f.seek(0)
        f.writelines(stat_file) 
        f.truncate()
#######

    while True:
        if aux == 0:
            frame = cv2.imread(images_directory + file_name_arr[0][0])
        else:
            if cv2.waitKey(0) == ord('p') or forward_flag == 1:
                if forward_flag == 1:
                    forward_flag = 0
                img_index += 1
                frame = cv2.imread(images_directory + file_name_arr[img_index][0])
            elif cv2.waitKey(0) == ord('ö') or backward_flag == 1:
                if backward_flag == 1:
                    backward_flag = 0
                img_index -= 1
                frame = cv2.imread(images_directory + file_name_arr[img_index][0])
            elif cv2.waitKey(0) == ord('ü') or exit_flag == 1:
                if exit_flag == 1:
                    exit_flag = 0
                break
            else:
                continue

        annotations_current_img  = list(filter(lambda annotation: annotation['image_id'] == file_name_arr[img_index][1], data['annotations']))

        selected_ann = 0

        if annotations_current_img:

            while True:
                
                selected_ann = selected_ann % len(annotations_current_img)

                for ind,anno in enumerate(annotations_current_img): #show selected annotation to user
                    bbox = anno['bbox']
                    if 'track_id' in anno:
                        track_id = anno['track_id']
                    
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    
                    if ind == selected_ann: #change color
                        color = (255, 0, 0)
                        cv2.rectangle(frame, p1, p2, color=color, thickness=2)
                        cv2.putText(frame, 'track_id: ' + str(track_id), (int(bbox[0]), int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=color, thickness=2)
                    else:
                        color = (0, 255, 0)
                        cv2.rectangle(frame, p1, p2, color=color, thickness=2)
                        cv2.putText(frame, 'track_id: ' + str(track_id), (int(bbox[0]), int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=color, thickness=2) 
                

                cv2.imshow('frame', cv2.resize(frame, (800, 800)))
                if cv2.waitKey(20) == ord('q'):
                    break
                

                if cv2.waitKey(0) == ord('k'):
                    new_track_id = int(input("enter new track id: "))
                for ind,anno in enumerate(annotations_current_img): #edit track_id
                    if ind == selected_ann:
                        current_ann = annotations_current_img[selected_ann]
                        correction = True
                        if current_ann['track_id'] < 0:
                            correction = False
                        
                        #new_track_id = int(input("enter new track id: "))
                        anno['track_id'] = new_track_id

                    ####### 26,27,37,38,28,29
                        if correction:
                            total_track_ids_corrected += 1
                            if new_track_id >= len(corrected_track_id_list):
                                for i in range(1 + new_track_id - len(corrected_track_id_list)):
                                    corrected_track_id_list.append(0)
                            corrected_track_id_list[new_track_id] += 1

                            indiv_track_id = 0
                            for j in corrected_track_id_list:
                                if j > 0:
                                    indiv_track_id += 1
                        
                            if indiv_track_id > individual_track_ids_corrected:
                                    individual_track_ids_corrected = indiv_track_id

                        if not correction:
                            total_track_ids_added += 1

                            if new_track_id >= len(added_track_id_list):
                                for i in range(1 + new_track_id - len(added_track_id_list)):
                                    added_track_id_list.append(0)
                            added_track_id_list[new_track_id] += 1

                            indiv_track_id = 0
                            for j in added_track_id_list:
                                if j > 0:
                                    indiv_track_id += 1
                            
                            if indiv_track_id > individual_track_ids_added:
                                individual_track_ids_added = indiv_track_id
                            

                        with open('D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Iteration 1\\stats_iteration_1 copy.txt', 'r+') as f:
                            stat_file = f.readlines()

                            stat_file[25] = str(total_track_ids_added) + "\n"
                            stat_file[26] = str(total_track_ids_corrected) + "\n"
                            stat_file[36] = str(added_track_id_list) + "\n"
                            stat_file[37] = str(corrected_track_id_list) + "\n"
                            stat_file[27] = str(individual_track_ids_added) + "\n"
                            stat_file[28] = str(individual_track_ids_corrected) + "\n"

                            f.seek(0)
                            f.writelines(stat_file) 
                            f.truncate()
                    #######
                            
                        with open(json_file, 'w') as f:
                            json.dump(data, f, indent=4)

                if cv2.waitKey(0) == ord('ä'):
                    selected_ann += 1
                    continue
                elif cv2.waitKey(0) == ord('l'):
                    selected_ann -= 1
                    continue
                elif cv2.waitKey(0) == ord('p'):
                    forward_flag = 1
                    break
                elif cv2.waitKey(0) == ord('ö'):
                    backward_flag = 1
                    break
                elif cv2.waitKey(0) == ord('ü'):
                    exit_flag = 1
                    break
                else:
                    continue

        else:
            print(img_index)
            cv2.imshow('frame', cv2.resize(frame, (800, 800)))
            if cv2.waitKey(20) == ord('q'):
                    break

        aux += 1

    print("x")
    cv2.destroyAllWindows()

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

######## 36,39,40
    for anno in data['annotations']:
        if anno['track_id'] >= 0:
            total_track_ids_post += 1
            if anno['track_id'] > highest_track_id:
                highest_track_id = anno['track_id']

    for i in range(highest_track_id + 1):
        post_track_id_list.append(0)
    
    for anno in data['annotations']:
        if anno['track_id'] >= 0:
            track_id = anno['track_id']
            post_track_id_list[track_id] += 1

    for i in pre_track_id_list:
        if i > 0:
            individual_track_ids_post += 1

    with open('D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Iteration 1\\stats_iteration_1 copy.txt', 'r+') as f:
        stat_file = f.readlines()
        stat_file[38] = str(total_track_ids_post) + "\n"
        stat_file[39] = str(individual_track_ids_post) + "\n"
        stat_file[35] = str(post_track_id_list) + "\n"

        f.seek(0)
        f.writelines(stat_file) 
        f.truncate()
#######