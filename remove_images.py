#author: Laurids Radtke
#date: 20.01.2022
#remove unwanted images and their annotations

import json

if __name__ == '__main__':

    inp = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Eval 2\\start-6109-4.json'
    outp = 'D:\\UserData\\z004d1kc\\OneDrive - Siemens AG\\BA\\Datasets\\WittstockBerlin\\annotations\\Eval 2\\start-6109-4.json'

    with open(inp) as r:
        data = json.load(r)

    remove_id = []

    for ind,image in enumerate(data['images']):
        if ind > 2300:
            remove_id.append(image['frame_id']) #safe ids of images we want to remove so we can remove the associated annotations

    new_data = dict()
    new_data['images'] = []
    new_data['annotations'] = []
    new_data['categories'] = []

    new_data['images'] = [img for img in data['images'] if img['frame_id'] < 2301]

    #new_data['annotations'] = [obj for obj in data['annotations'] if obj['image_id'] not in remove_id]
    new_data['categories'] = data['categories']
    new_data['videos'] = [vid for vid in data['videos'] if vid['id'] == 3]

    with open(outp, 'w') as w:
        json.dump(new_data, w, indent=4)

