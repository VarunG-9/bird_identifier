# imports
from fastcore.all import *
from fastbook import search_images_ddg as search_images
from fastdownload import download_url
from time import sleep
from PIL import Image
from urllib.parse import urlparse
from functions import *
from fastai.vision.all import *

load_images()
path = 'data'

dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files(path),
    splitter=RandomSplitter(valid_pct=0.2,seed=None),
    get_y=parent_label,
    item_tfms=[Resize(192, method='squish')]
).dataloaders(path, bs=8)

dls.show_batch(max_n=6)


