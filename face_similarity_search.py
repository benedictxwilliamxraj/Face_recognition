import argparse
import face_recognition
import cv2
import json
import codecs
import numpy as np
import math
from sklearn.metrics.pairwise import cosine_similarity

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


# ap = argparse.ArgumentParser()
# ap.add_argument("-i","--image",required=True,help="path of the image directory")
# args = vars(ap.parse_args())

# #loading the given json file
# print('[INFO]loading the json face_encodings...')
# json_dict_file = 'encoding.json'
# json_dict_dump = []
# json_obj_text = codecs.open(json_dict_file,'r',encoding='utf-8').read()
# json_dict_dump = json.loads(json_obj_text)

# #print(json_dict_dump)

# img = cv2.imread(args['image'])
# rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# #identify face in a given image
# box = face_recognition.face_locations(rgb, model= "hog") # try model using cnn also

# #encode the given image 
# print('[INFO]encoding the given image.....')
# query_encoding = face_recognition.face_encodings(rgb,box)

# query_encoding_1 = np.array(query_encoding)

# print(query_encoding_1.shape)





# face_encoding_x = json_dict_dump[0]['encodings']
# face_encoding_x1 = np.array(face_encoding_x)
# face =face_encoding_x1.reshape(1,128)

# # print(face_encoding_x)
# min1 = cosine_similarity(face,query_encoding)

	
# print("Cosine similarity: ", min1 ,"name: ", json_dict_dump[0]['names'])


# # loop over the recognized faces
# for ((top, right, bottom, left),name) in zip(box,json_dict_dump[0]['names']):
# 	# draw the predicted face name on the image
# 	cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
# 	y = top - 15 if top - 15 > 15 else top + 15
# 	cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
# 		0.75, (0, 255, 0), 2)

# # show the output image
# cv2.imshow("Image", img)
# cv2.waitKey(0)

################################################################

def Insert_Encodetag():
	#initialize an array of encodings with names
	known_names = []
	known_encoding = []

	#load the json folder and load into a list
	f = open('encoding.json')
	json_dict_dump = json.load(f)
	f.close()

	#read the image and get the encodings
	img = cv2.imread(args['img'])
	rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	box = face_recognition.face_locations(rgb, model= "hog") # try model using cnn also
	encoding = face_recognition.face_encodings(rgb,box)

	known_encoding.append(encoding[0])
	#if no name is given in arguments
	# if(args['name'] == None):
	# 	name = input()
	# 	known_names.append(name)
	#################################
	known_names.append(args['name'])

	#python dictonary
	data = {
		'names': known_names,
		'encodings': known_encoding[0]
		}

	dict_list=[]
	dict_list.append(data)
	json_dict_dump = dict_list + json_dict_dump
	#appending to encodings.json file
	with open('encoding.json','w') as json_file:							
		test_json = json.dump(json_dict_dump, json_file, cls=MyEncoder,indent = 4) 




print('[INFO]Loadig encodings in a list...')
img_encodings_json = open('encoding.json')
json_list_dump = json.load(img_encodings_json)
print(json_list_dump)
img_encodings_json.close()
	# load the input image and convert it from BGR to RGB
image = cv2.imread(args["img"])
img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

print("[INFO] recognizing faces...")
boxes = face_recognition.face_locations(img_rgb, model='hog')
print(boxes)

query_encodings = face_recognition.face_encodings(img_rgb, boxes)
#print(query_encodings)

#initiliaze the list of names for each face detected
disp_names = []
print(disp_names)
# loop over facial embeddings 
json_list_len = len(json_list_dump)
for encoding in query_encodings:
	for each_dict in json_list_dump:
		# matches = face_recognition.compare_faces(json_list_dump['encodings'],encoding)
		flag_threshold = 'X'
		flag_in_dict= 'X'
		flag_new = 'X'
		#Resize the two encodings
		img_db_encodings = np.asarray(each_dict['encodings'], np.float32)
		img_db_encodings = img_db_encodings.reshape(1,128)
		
		img_query_encodings = np.array(encoding)
		img_query_encodings = img_query_encodings.reshape(1,128)
		
		# dot product of two vecs with cosine_similarity()
		matches_accuracy = cosine_similarity(img_db_encodings,img_query_encodings)

		# print(matches_accuracy[0][0])
		face_match_score = matches_accuracy[0][0]
		face_match_threshold = 0.91

		# face similarity matching with threshold
		if face_match_score > face_match_threshold:
			print("Face found")
			name = each_dict['names']
			flag_threshold = 'Y'
			disp_names.append(name[0])
		elif face_match_score <= face_match_threshold:
			for each_dict in  json_list_dump:											#to check if its in dictionary or not
				if flag_threshold == 'X':
					print(each_dict['encodings'])
					img_db_encodings_1 = np.asarray(each_dict['encodings'], np.float32)
					img_db_encodings_1 = img_db_encodings_1.reshape(1,128)

					img_query_encodings_1 = np.array(encoding)
					img_query_encodings_1 = img_query_encodings.reshape(1,128)
					if (img_db_encodings_1 == img_query_encodings_1).all():
						flag_in_dict = 'Y'  # Flag: present in dictionary

				else:
					flag_new = 'A'   # Flag: add in dictionary
					break
		
		if ((flag_threshold == 'X' and flag_in_dict == 'X' and flag_new == 'A') or (flag_threshold == 'X' and flag_in_dict == 'X' and flag_new == 'X')) :
			print("face not found")
			disp_names.append('Unknown_Face')

print(disp_names)




for disp_name in disp_names:
	if disp_name == 'Unknown_Face':
		Insert_Encodetag()
	# disp_names.append('Unknown_Face')

#disp_names.append('Unknown_Face')
# for disp_name in disp_names:
# 	if(disp_name == 'Unknown_Face'):
# 		Insert_Encodetag()	
print(disp_names)

actual_name_input = args['name']
print(actual_name_input)

# to display the imgs actual and predicted
for((top, right, bottom, left), name) in zip(boxes, disp_names):
	# draw the predicted face name on the ima
	cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
	y = top - 15 if top - 15 > 15 else top + 15
	cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
		0.75, (0, 255, 0), 2)
	
cv2.imshow("Image", image)
cv2.waitKey(0)

