# imports
from fastcore.all import *
from fastbook import search_images_ddg as search_images
from fastdownload import download_url
from time import sleep
from PIL import Image
from urllib.parse import urlparse
from fastai.vision.all import *

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

def main():
    path = Path('data')

    dls = DataBlock(
        blocks=(ImageBlock, CategoryBlock),
        get_items=get_image_files,
        splitter=RandomSplitter(valid_pct=0.2,seed=None),
        get_y=parent_label,
        item_tfms=[Resize(192, method='squish')]
    ).dataloaders(path, bs=8)

    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.fine_tune(3) # Training with 3 epochs
    learn.export('Model.pkl')

if __name__ == '__main__':
    main()





