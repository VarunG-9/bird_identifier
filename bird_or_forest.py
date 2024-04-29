# imports
from fastcore.all import *
from fastbook import search_images_ddg as search_images
from fastdownload import download_url
from time import sleep
from PIL import Image
from urllib.parse import urlparse


def download_url(url, dest=None, filename=None, timeout=None, show_progress=True):
    "Download `url` to `dest` with optional filename and show progress"
    if filename is None:
        filename = os.path.basename(urlparse(url).path)
    if dest is None:
        dest = filename
    else:
        dest = str(dest) + str(os.sep) + list(os.path.basename(urlparse(url).path))[0] + list(os.path.basename(urlparse(url).path))[1] +  os.path.basename(urlparse(url).path[-5:])
    return urlsave(url, dest, None, timeout=timeout)

# Simplified Download Function
def download_images(urls, dest):
    for index in range(len(urls)):
        print(f'Attempting to download URL {urls[index]}')
        try:
            download_url(urls[index], dest, show_progress=False, filename=f'{index}')
        except:
            print('Downloaded excepted')
        sleep(0.5)
        print(f'Downloaded URL {index}: {urls[index]}')


def resize_images(dir, max_size):
    num = 0
    for filename in os.listdir(dir): # Looping through directory
        num+=1
        f = os.path.join(dir, filename) # Finding path of file
        if os.path.isfile(f): # Checks if it is a file
            image = Image.open(f) # Opens image
            new_image = image.resize((max_size, max_size)) # Resizing Image
            os.remove(f) # Deleting old image
            new_image.save(f'{dir}{os.sep}{num}{filename[-5:]}') # Saving new Image
            


# Defining function to save pics in respective folders
def load_images():
    searches = 'forest','bird'
    path = Path('data')

    for o in searches:
        # Define destination
        dest = (path/o)
        print(dest)
        dest.mkdir(exist_ok=True, parents=True)

        download_images(search_images(f'{o} photo with background direct link', max_images=7), dest=dest)
        print('Pausing')
        sleep(10)  # Pause between searches to avoid over-loading server
        download_images(search_images(f'{o} sun photo direct link ', max_images=7), dest=dest)
        print('Pausing')
        sleep(10)
        download_images(search_images(f'{o} shade photo direct link', max_images=7), dest=dest)
        print('Finished Downloading Images. Resizing')
        resize_images(path/o, max_size=400)


load_images()

