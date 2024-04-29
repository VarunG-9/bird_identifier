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
def load_images(max_images=30, folder_name='data'):
    """ Loads images into the folder 'folder_name' with 'max_images' images per query (there are 3 queries)
    """ 

    searches = 'forest','bird'
    path = Path(folder_name)

    for o in searches:
        # Define destination
        dest = (path/o)
        print(dest)
        dest.mkdir(exist_ok=True, parents=True)

        download_images(search_images(f'{o} photo with background direct link', max_images=max_images), dest=dest)
        print('Pausing')
        sleep(10)  # Pause between searches to avoid over-loading server
        download_images(search_images(f'{o} sun photo direct link ', max_images=max_images), dest=dest)
        print('Pausing')
        sleep(10)
        download_images(search_images(f'{o} shade photo direct link', max_images=max_images), dest=dest)
        print('Finished Downloading Images. Resizing')
        resize_images(path/o, max_size=400)

def get_files(path, extensions=None, recurse=True, folders=None, followlinks=True):
    "Get all the files in `path` with optional `extensions`, optionally with `recurse`, only in `folders`, if specified."
    path = Path(path)
    folders=L(folders)
    extensions = setify(extensions)
    extensions = {e.lower() for e in extensions}
    if recurse:
        res = []
        for i,(p,d,f) in enumerate(os.walk(path, followlinks=followlinks)): # returns (dirpath, dirnames, filenames)
            if len(folders) !=0 and i==0: d[:] = [o for o in d if o in folders]
            else:                         d[:] = [o for o in d if not o.startswith('.')]
            if len(folders) !=0 and i==0 and '.' not in folders: continue
            res += _get_files(p, f, extensions)
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        res = _get_files(path, f, extensions)
    return L(res)

def get_image_files(path, recurse=True, folders=None):
    "Get image files in `path` recursively, only in `folders`, if specified."
    return get_files(path, extensions=image_extensions, recurse=recurse, folders=folders)




