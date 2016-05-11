from clarifai.client import ClarifaiApi
import json
import operator
import os

all_tags = {}
clarifai_api = ClarifaiApi() # assumes environment variables are set.

user_path = raw_input("Please enter path of photo library: ")

if not os.path.exists(user_path):
    print("Path does not exist")

for i in os.listdir(user_path):
    result = clarifai_api.tag_images(open(user_path + i, 'rb'))['results'][0]['result']['tag']['classes']
    for j in result:
        if (j in all_tags):
            all_tags[j] += 1
        else:
            all_tags[j] = 1
    print '\n'

tag_tuples = sorted(all_tags.items(), key=operator.itemgetter(1))
for i in range(len(tag_tuples) - 5, len(tag_tuples)):
    dir_name = 'album/' + tag_tuples[i][0] + '/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)