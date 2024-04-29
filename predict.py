from fastcore.all import *
from fastbook import search_images_ddg as search_images
from fastdownload import download_url
from time import sleep
from PIL import Image
from urllib.parse import urlparse
from fastai.vision.all import *
import sys

path_input = str(sys.argv[1])
try:
    model = sys.argv[2]
except:
    model = 'Model.pkl'


learn = load_learner(model)
is_bird,_,probs = learn.predict(PILImage.create(path_input))
print(f"This is a: {is_bird}.")
print(f"Probability it's a bird: {probs[0]:.4f}")