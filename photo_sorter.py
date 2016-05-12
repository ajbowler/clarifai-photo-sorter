from clarifai.client import ClarifaiApi
from shutil import copy
import json
import operator
import os

tag_histogram = {}
image_tag_lists = []
clarifai_api = ClarifaiApi() # assumes environment variables are set.

user_path = raw_input("Please enter path of photo library: ")
print '\n'

if not os.path.exists(user_path):
    print("Path does not exist")
    exit()

image_paths = os.listdir(user_path)

print 'Begin processing images...\n'
for path in range(0, len(image_paths)):
    result = clarifai_api.tag_images(open(user_path + image_paths[path], 'rb'))['results'][0]['result']['tag']['classes']
    image_tag_lists.append(result)
    for tag in result:
        if (tag in tag_histogram):
            tag_histogram[tag] += 1
        else:
            tag_histogram[tag] = 1
    cur = str(path + 1)
    print cur + ' out of ' + str(len(image_paths)) + ' images processed...' 

print '\n'
tag_tuples = sorted(tag_histogram.items(), key=operator.itemgetter(1))
top_five_tuples = tag_tuples[len(tag_tuples) - 5:len(tag_tuples)]
top_five_tags = []
print 'The top 5 tags from your photos are:\n'
for i in top_five_tuples:
    print i[0]
    top_five_tags.append(i[0])

if not os.path.exists('album/misc/'):
    os.makedirs('album/misc/')

print '\nCreating directories for each tag...\n'
for tag in top_five_tags:
    dir_name = 'album/' + tag + '/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

found_dir = False
for i in range(0, len(image_tag_lists)):
    for tag in image_tag_lists[i]:
        if tag in top_five_tags:
            src = user_path + image_paths[i]
            dst = "album/" + tag + '/'
            copy(str(src), str(dst))
            found_dir = True
            break;
    if not found_dir:
        copy(str(src), str('album/misc/'))
    cur = str(i + 1)
    print cur + ' out of ' + str(len(image_tag_lists)) + ' images sorted...'

print '\nAll images sorted. Check the album directory for your newly sorted images!\n'