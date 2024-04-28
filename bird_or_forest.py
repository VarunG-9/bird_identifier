# imports
from fastcore.all import *
from fastbook import search_images_ddg as search_images
from fastdownload import download_url
from time import sleep
from PIL import Image

def resize_images(dir, max_size):
    for filename in os.listdir(dir): # Looping through directory
        f = os.path.join(dir, filename) # Finding path of file
        if os.path.isfile(f): # Checks if it is a file
            image = Image.open(f) # Opens image
            new_image = image.resize((max_size, max_size)) # Resizing Image
            os.remove(f) # Deleting old image
            new_image.save(f'{dir}{os.sep}{filename}') # Saving new Image
            
# Simplified Download Function
def download_images(urls, dest):
    for index in range(len(urls)):
        download_url(urls[index], dest, show_progress=False)
        print(f'Downloaded URL: {index}')

# Defining function to save pics in respective folders
def load_images():
    searches = 'forest','bird'
    path = Path('bird_or_not')

    for o in searches:
        # Define destination
        dest = (path/o)
        print(dest)
        dest.mkdir(exist_ok=True, parents=True)

        download_images(search_images(f'{o} photo png', max_images=7), dest=dest)
        print('Pausing')
        sleep(10)  # Pause between searches to avoid over-loading server
        download_images(search_images(f'{o} sun photo png', max_images=7), dest=dest)
        print('Pausing')
        sleep(10)
        download_images(search_images(f'{o} shade photo png', max_images=7), dest=dest)
        print('Finished Downloading Images. Resizing')
        resize_images(path/o, max_size=400)

load_images()
