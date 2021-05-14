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
ap.add_argument("-n","--name",required=True,help="name of the tag given")
ap.add_argument("-u","--update",default=None,help="updating a false postive case")
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
common_dict_json_file = 'encoding.json'


#load the json folder and load into a list
img_encodings_json = open(common_dict_json_file)
json_dict_dump = json.load(img_encodings_json)
img_encodings_json.close()
encoding_dict_dump.append(json_dict_dump)
##########################################
# json_dict_dump = []
# json_obj_text = codecs.open(common_dict_json_file,'r',encoding='utf-8').read()
# json_dict_dump = json.loads(json_obj_text)
# encoding_dict_dump.append(json_dict_dump)

# print(encoding_dict_dump[0])
# exit()

################################################################

known_names = []
known_encoding = []

def Insert_Encodetag(img_name, encoding):

	known_names.append(img_name)
	# print(known_names)
	known_encoding.append(encoding[0])
	#if no name is given in arguments
	# if(args['name'] == None):
	# 	name = input()
	# 	known_names.append(name)
	#################################
	

	#python dictonary
	data = {
		'names': known_names,
		'encodings': known_encoding[0]
		}

	dict_list=[]
	dict_list.append(data)
	# json_dict_dump = dict_list + encoding_dict_dump[0]

	json_dict_dump = dict_list + encoding_dict_dump[0]
	# print(json_dict_dump)

	#appending to encodings.json file
	with open(common_dict_json_file, 'w') as json_file:
		test_json = json.dump(json_dict_dump, json_file, cls=MyEncoder, indent = 4)


json_list_len = len(json_dict_dump)


def face_in_db(check_encoding):
	for each_dict in range(json_list_len):
		img_db_encodings_1 = np.asarray(json_dict_dump[each_dict]['encodings'], np.float32)
		img_db_encodings_1 = img_db_encodings_1.reshape(1,128)

		img_query_encodings_1 = np.array(check_encoding)
		img_query_encodings_1 = img_query_encodings_1.reshape(1,128)
		if(img_db_encodings_1 == img_query_encodings_1).all():
			return True

	return False


# print('[INFO]Loadig encodings in a list...')
# img_encodings_json = open('encoding.json')
# json_list_dump = json.load(img_encodings_json)
# #print(json_list_dump)
# img_encodings_json.close()
# load the input image and convert it from BGR to RGB
# image = cv2.imread(args["img"])
# img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# print("[INFO] recognizing faces...")
# boxes = face_recognition.face_locations(img_rgb, model='hog')
# print(boxes)

# query_encodings = face_recognition.face_encodings(img_rgb, boxes)
# #print(query_encodings)

#initiliaze the list of names for each face detected

#print(disp_names)
# loop over facial embeddings 
face_found_name = []
face_found_name_encoding = []

def face_sim_search():
	for encoding in query_encodings:

		# face similarity from face encodings DB
		for each_dict in range(json_list_len):
			# face_found_name = []
			# matches = face_recognition.compare_faces(json_list_dump['encodings'],encoding)
			# flag_in_db = 'X'
			# flag_in_db_not_match = 'X'
			# flag_new = 'X'

			#Resize the two encodings
			img_db_encodings = np.asarray(json_dict_dump[each_dict]['encodings'], np.float32)
			img_db_encodings = img_db_encodings.reshape(1,128)
			
			img_query_encodings = np.array(encoding)
			img_query_encodings = img_query_encodings.reshape(1,128)
			
			# dot product of two vecs with cosine_similarity()
			matches_accuracy = cosine_similarity(img_db_encodings,img_query_encodings)

			# print(matches_accuracy[0][0])
			face_match_score = matches_accuracy[0][0]
			face_match_threshold = 0.93
			face_found_name_encoding.append(face_match_score)

			# face similarity matching with threshold

			if face_match_score > face_match_threshold:
				#print("Face found")
				name = json_dict_dump[each_dict]['names']
				face_found_name.append(name[0])
				
				print(face_match_score)
				# print(face_found_name[0])
				
			elif face_match_score <= face_match_threshold:
				flag_in_db = face_in_db(encoding)
				if(flag_in_db == True):
					continue
				else:
					#print("face not found")
					face_found_name.append('Unknown_Face')
			else:
				break

	
	print(face_found_name)
	# print(face_found_name_encoding)	
	return_name = 'Unknown_Face'
	maximum_matchscore = 0.0
	j =0

	for i in face_found_name:
		if(i != 'Unknown_Face'):
			if(face_found_name_encoding[j] > maximum_matchscore):
				maximum_matchscore = face_found_name_encoding[j]
				return_name = i
		j = j+1

	if(return_name != 'Unknown_Face'):
		return return_name
		
	else:
		return "Unknown_Face"

	#return face_found_name[0]


if __name__ == "__main__":
	# print('its working')
	face_sim_result = face_sim_search()

	if(args['name']!='Unknown Person' and args['name'] != args['update'] and args['update'] != 'Unknown Person'):
		#print(args['name'])
		Insert_Encodetag(args['name'],query_encodings)
	# if(args['name'] != 'Unknown Person' and face_sim_result != "Unknown_Face"):
	# 	Insert_Encodetag(img_name, query_encodings)
	# 	face_sim_result = face_sim_search()
	# 	print(face_sim_result,'from first if')
	# 	exit()
	# face_sim_result = face_sim_search()
	
	if face_sim_result == "Unknown_Face":
		# Insert_Encodetag(img_name, query_encodings)

		if(args['name']!='Unknown Person'):
			Insert_Encodetag(img_name, query_encodings)
			print(args['name'])
			# face_sim_result = face_sim_search()
			# print(face_sim_result)
		else:
			print('Unknown Person')
	else:
		print('working')
		print(face_sim_result)








# disp_names.append('Unknown_Face')

#disp_names.append('Unknown_Face')
# for disp_name in disp_names:
# 	if(disp_name == 'Unknown_Face'):
# 		Insert_Encodetag()	
# print(disp_names)

# actual_name_input = args['name']
# print(actual_name_input)

# # to display the imgs actual and predicted
# for((top, right, bottom, left), name) in zip(boxes, disp_names):
# 	# draw the predicted face name on the ima
# 	cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
# 	y = top - 15 if top - 15 > 15 else top + 15
# 	cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
# 		0.75, (0, 255, 0), 2)
	
# cv2.imshow("Image", image)
# cv2.waitKey(0)

