#author: Laurids Radtke 
#date: 17.12.21
#this tool removes everything which has not the right category id from a coco json file
import json

if __name__ == '__main__':

    top_cats = [70,89]
    inp = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\Falkensee\\topodot_corrected_landmarks_new.json'
    outp = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\Falkensee\\falkensee_imperfect_track_ids_2categories_imperfect_bbox.json'

    with open(inp) as r:
        data = json.load(r)
    
    new_data = dict()
    new_data['images'] = []
    new_data['annotations'] = []
    new_data['categories'] = []
    #new_data['landmarks'] = []

    new_data['images'] = data['images']

    new_data['annotations'] = [obj for obj in data['annotations'] if obj['category_id'] in top_cats]
    new_data['categories'] = [obj for obj in data['categories'] if obj['id'] in top_cats]
    #new_data['landmarks'] = [obj for obj in data['landmarks'] if obj['category_ids'][0] in top_cats]

    for annotation in data['annotations']:
        if annotation['category_id'] == 70:
            annotation['category_id'] = 1
        if annotation['category_id'] == 89:
            annotation['category_id'] = 2
    
    for category in data['categories']:
        if category['id'] == 70:
            category['id'] = 1
        if category['id'] == 89:
            category['id'] = 2
    

    with open(outp, 'w') as w:
        json.dump(new_data, w, indent=4)
