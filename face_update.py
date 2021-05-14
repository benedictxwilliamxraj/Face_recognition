import argparse
import face_recognition
import cv2
import json
import codecs
import numpy as np
import math
#from sklearn.metrics.pairwise import cosine_similarity

ap = argparse.ArgumentParser()
ap.add_argument("-i","--img",required=True,help="path of the image directory")
ap.add_argument("-n","--name",default=None,help="name of the tag given")
args = vars(ap.parse_args())


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

img_name = args['name']
#read the image and get the encodings
image = cv2.imread(args["img"])
img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
face_box = face_recognition.face_locations(img_rgb, model= "hog") # try model using cnn also
query_encodings = face_recognition.face_encodings(img_rgb, face_box)

encoding_dict_dump = list()


#load the json folder and load into a list
img_encodings_json = open('encoding.json')
json_dict_dump = json.load(img_encodings_json)
img_encodings_json.close()
encoding_dict_dump.append(json_dict_dump)

json_list_len = len(json_dict_dump)
# print(encoding_dict_dump)
# print(json_dict_dump)

known_names = []
known_encoding = []

if __name__ == "__main__":
	face_update_name = update_name()



def update_name(){
    for encoding in query_encodings:

        # face similarity from face encodings DB
        for each_dict in range(json_list_len):

            #Resize the two encodings
            img_db_encodings = np.asarray(json_dict_dump[each_dict]['encodings'], np.float32)
            img_db_encodings = img_db_encodings.reshape(1,128)
            
            img_query_encodings = np.array(encoding)
            img_query_encodings = img_query_encodings.reshape(1,128)
            
            # dot product of two vecs with cosine_similarity()
            matches_accuracy = cosine_similarity(img_db_encodings,img_query_encodings)	
            if ((img_db_encodings_1 == img_query_encodings_1).all() || matches_accuracy>0.959):
                json_dict_dump[each_dict]['names'] = args['name']
            
                
}	