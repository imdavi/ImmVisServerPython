import pandas as pd
from PIL import Image
import numpy as np

_X_COLUMN = 'x'
_Y_COLUMN = 'y'
_R_COLUMN = 'r'
_G_COLUMN = 'g'
_B_COLUMN = 'b'

def read_image_as_dataframe(file_path):
    img = Image.open(file_path)
    pixels = img.convert('RGB')
    colour_array = np.array(pixels.getdata()).reshape(img.size + (3,))
    indices_array = np.moveaxis(np.indices(img.size), 0, 2)
    all_array = np.dstack((indices_array, colour_array)).reshape((-1, 5))
    return pd.DataFrame(all_array, columns=[_Y_COLUMN, _X_COLUMN, _R_COLUMN, _G_COLUMN, _B_COLUMN])
