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
    total_track_ids_corrected = 0
    total_track_ids_post = 0
    individual_track_ids_post = 0
    prev_corr_track_id = -2
    
    json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\annotations\Iteration 4\\6401_almost_perf_track_ids_perf_bbox_vid_5_it_4.json'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Eval 2\\6109_perf_track_ids_perf_bbox_vid_4_eval_2.json'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Iteration 3\\6109_perf_track_ids_perf_bbox_vid_3_it_3.json'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Iteration 1\\second run\\6109_perf_track_ids_2cats_perf_bbox_vid_2.json'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Eval 2\\6109_imperf_track_ids_perf_bbox_vid_4_eval_2.json'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Iteration 2\\new model\\6109_perf_track_ids_perf_bbox_vid_1_it_2_new_model.json'
    images_directory = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\images\\'
    statistics_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\annotations\\Iteration 4\\stats_iteration_4.txt'


    with open(json_file) as f:
        data = json.load(f)

    file_name_arr = []
    c = 0
    for image in data['images']:
        c += 1
        file_name = image['file_name']
        id = image['id']
        file_name_arr.append((file_name,id))
        
    img_index = 0
    aux = 0
    forward_flag = 0
    backward_flag = 0
    exit_flag = 0

####### 31,32,33
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
    
    with open(statistics_file, 'r+') as f:
        stat_file = f.readlines()
        stat_file[27] = str(total_track_ids) + "\n"
        stat_file[28] = str(individual_track_ids) + "\n"
        stat_file[29] = str(pre_track_id_list) + "\n"

        f.seek(0)
        f.writelines(stat_file) 
        f.truncate()
#######

    while True:
        if img_index >= len(file_name_arr) - 1:
            highest_track_id = 0
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

            for i in post_track_id_list:
                if i > 0:
                    individual_track_ids_post += 1

            with open(statistics_file, 'r+') as f:
                stat_file = f.readlines()
                stat_file[32] = str(total_track_ids_post) + "\n"
                stat_file[33] = str(individual_track_ids_post) + "\n"
                stat_file[34] = str(post_track_id_list) + "\n"

                f.seek(0)
                f.writelines(stat_file) 
                f.truncate()
            #######

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
            print(str(img_index)+"/"+str(c))
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
                    for ind,anno in enumerate(annotations_current_img): #edit track_id
                        if ind == selected_ann:
                            current_ann = annotations_current_img[selected_ann]
                            new_track_id = int(input("enter new track id: "))
                            corr_track_id = anno['track_id']
                            anno['track_id'] = new_track_id
                            with open(json_file, 'w') as f:
                                json.dump(data, f, indent=4)

                            ####### 
                            with open(statistics_file, 'r+') as f:
                                stat_file = f.readlines()
                                total_track_ids_corrected = int(stat_file[30])
                                indiv_track_ids_corrected = int(stat_file[31])

                                if corr_track_id != prev_corr_track_id:
                                    indiv_track_ids_corrected += 1
                                prev_corr_track_id = corr_track_id

                                total_track_ids_corrected += 1
                                
                                stat_file[30] = str(total_track_ids_corrected) + "\n"
                                stat_file[31] = str(indiv_track_ids_corrected) + "\n"

                                f.seek(0)
                                f.writelines(stat_file) 
                                f.truncate()
                            #######

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
            print(str(img_index)+"/"+str(c))
            cv2.imshow('frame', cv2.resize(frame, (800, 800)))
            if cv2.waitKey(20) == ord('q'):
                break

        aux += 1

    print("x")
    cv2.destroyAllWindows()

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

   