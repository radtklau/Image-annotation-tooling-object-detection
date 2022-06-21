import json
import cv2

if __name__ == '__main__':

    json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Iteration 3\\start-6109-3.json'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\annotations\\Iteration 4\\start-6401-5.json'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Eval 2\\6109_perf_track_ids_perf_bbox_vid_4_eval_2.json'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Iteration 2\\new model\\start-6109-1.json'
    #images_directory = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6401\\images\\'
    images_directory = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\images\\'
    #images_directory = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6098\\images\\'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\6098\\annotations\\Iteration 0\\6098_imperf_track_ids_2categories_imperf_bbox.json'
    #json_file = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\topodot_corrected_landmarks_new.json'

    with open(json_file) as f:
        data = json.load(f)

    aux = 0
    for ind,image in enumerate(data['images']):
        if ind < 277:
            continue
        print(str(ind)+"/"+str(len(data['images'])))
        file_name = image['file_name']
        id = image['id']

        annotations_current_img  = list(filter(lambda annotation: annotation['image_id'] == id, data['annotations']))

        frame = cv2.imread(images_directory + file_name)
        
        for anno in annotations_current_img:
            bbox = anno['bbox']
            cat_id = anno['category_id']
            track_id = anno['track_id']
            id = anno['id']
            
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            color = (0, 255, 0)

            cv2.rectangle(frame, p1, p2, color=color, thickness=2)
            cv2.putText(frame, 'track_id: ' + str(track_id), (int(bbox[0]), int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=color, thickness=2)
            cv2.putText(frame, 'id: ' + str(id), (int(bbox[0]), int(bbox[1]-30)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=color, thickness=2)

        cv2.imshow('frame', cv2.resize(frame, (1300,1300)))
        
        if cv2.waitKey(20) == ord('q'):
            break
        input("")

    cv2.destroyAllWindows()
    print(aux)