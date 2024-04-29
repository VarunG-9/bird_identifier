# imports
from fastcore.all import *
from fastbook import search_images_ddg as search_images
from fastdownload import download_url
from time import sleep
from PIL import Image
from urllib.parse import urlparse
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
        if os.path.isfile(f) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            try:
                image = Image.open(f) # Checks if it is a file
                new_image = image.resize((max_size, max_size)) # Resizing Image
                os.remove(f) # Deleting old image
                print(f'Resizing: {dir}{os.sep}{filename}')
                new_image.save(f'{dir}{os.sep}{filename}') # Saving new Image
            except IOError:
                os.remove(f)
                print(f"Image was removed as it was invalid. {filename}")
        else:
            os.remove(f)


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

