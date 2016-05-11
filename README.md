# clarifai-photo-sorter
Photo Sorter using the Clarifai Python API

This command line tool detects the top 5 image tags using the Clarifai API for an image folder and sorts the images into their own album folders depending on their tags.

## Usage

1. Obtain Clarifai credentials and set them up on your machine's environment as dictated on their website.
2. Run `python photo_sorter.py`
2. Input the image folder you want to sort. Make sure you add a `/` at the end if you haven't done so already.
3. Check the newly created `albums/` directory
