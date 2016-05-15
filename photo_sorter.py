from clarifai.client import ClarifaiApi
from shutil import copy
import json
import operator
import os
import sys

# histogram that records how many instances of each tag there are
tag_histogram = {}
# a list of list of the tags each image has
image_tag_lists = []
clarifai_api = ClarifaiApi()

# improper usage
if len(sys.argv) < 2:
    print '\nUsage:\n\t python photo_sorter.py <original photo directory>'
    exit()

orig_photo_dir = sys.argv[1]
if orig_photo_dir[len(orig_photo_dir) - 1] != '/':
    orig_photo_dir += '/'

# safe gaurd for if we can't find the album
if not os.path.exists(orig_photo_dir):
    print "\nPath does not exist"
    exit()

# list of all of the files stored in the user's given path
image_paths = os.listdir(orig_photo_dir)

print 'Begin processing images...\n'
# iterates through each file in the user's given path
for path in range(0, len(image_paths)):
    # a list of all of the tags in the current file we are in
    result = clarifai_api.tag_images(open(orig_photo_dir + image_paths[path], 'rb'))['results'][0]['result']['tag']['classes']
    # add this list to or lists of tag lists
    image_tag_lists.append(result)
    # add the tag to our histogram if it isn't there or increment it by one if it is
    for tag in result:
        if (tag in tag_histogram):
            tag_histogram[tag] += 1
        else:
            tag_histogram[tag] = 1
    cur = str(path + 1)
    print cur + ' out of ' + str(len(image_paths)) + ' images processed...' 

print '\n'
# same as tag_histogram but sorted
tag_tuples = sorted(tag_histogram.items(), key=operator.itemgetter(1))
# the five tags that had the highest usage
top_five_tuples = tag_tuples[len(tag_tuples) - 5:len(tag_tuples)]
# creates a list of the top five tags instead of having a list of tuples
top_five_tags = []
print 'The top 5 tags from your photos are:\n'
for i in top_five_tuples:
    print i[0]
    top_five_tags.append(i[0])

# create a misc directory for files that do not fit into any of our tags
if not os.path.exists('album/misc/'):
    os.makedirs('album/misc/')

print '\nCreating directories for each tag...\n'
for tag in top_five_tags:
    dir_name = 'album/' + tag + '/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# a boolean that is set to true when it fits into one of our tag folders.
# At the end of checking all folders, we will check found_dir, if it is still
# false (meaning the image could not fit), the image will be sent to misc.
found_dir = False
# goes through each image and checks all of our top five tags. If the images
# tags contain one of the top five tags, it will be sent to that 
# folder or 'ablum'
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
    found_dir = false
    print cur + ' out of ' + str(len(image_tag_lists)) + ' images sorted...'

# earses albums we didn't use
print '\nCleaning empty directories...\n'
album_dir_list = os.listdir('album/')
for directory in album_dir_list:
    sub_dir = 'album/' + directory + '/'
    if len(os.listdir(sub_dir)) == 0:
        os.rmdir(sub_dir)

print '\nAll images sorted. Check the album directory for your newly sorted images!\n'