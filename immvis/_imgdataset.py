import pandas as pd
from PIL import Image
import numpy as np

_X_COLUMN = 'x'
_Y_COLUMN = 'y'
_R_COLUMN = 'r'
_G_COLUMN = 'g'
_B_COLUMN = 'b'
_A_COLUMN = 'a'
_C_COLUMN = 'c'
_M_COLUMN = 'm'
_K_COLUMN = 'k'
_Y_COLUMN = 'y'
_CB_COLUMN = 'cb'
_CR_COLUMN = 'cr'
_L_COLUMN = 'l'
_H_COLUMN = 'h'
_S_COLUMN = 's'
_V_COLUMN = 'v'
_PIXEL_COLUMN = 'value'

_BASE_COLUMNS = [_Y_COLUMN, _X_COLUMN]

def _get_column_names(image_mode):
    return {
        '1': [_PIXEL_COLUMN],
        'L': [_PIXEL_COLUMN],
        'P': [_PIXEL_COLUMN],
        'RGB': [_R_COLUMN, _G_COLUMN, _B_COLUMN],
        'RGBA': [_R_COLUMN, _G_COLUMN, _B_COLUMN, _A_COLUMN],
        'CMYK': [_C_COLUMN, _M_COLUMN, _Y_COLUMN, _K_COLUMN],
        'YCbCr': [_Y_COLUMN, _CB_COLUMN, _CR_COLUMN],
        'LAB': [_L_COLUMN, _A_COLUMN, _B_COLUMN],
        'HSV': [_H_COLUMN, _S_COLUMN, _V_COLUMN],
        'I': [_PIXEL_COLUMN],
        'F': [_PIXEL_COLUMN],
    }[image_mode]


def read_image_as_dataframe(file_path):
    img = Image.open(file_path)

    img_mode = img.mode

    columns = _get_column_names(img_mode)

    dimensions_count_per_pixel = len(columns)

    colour_array = np.array(img.getdata()).reshape(
        img.size + (dimensions_count_per_pixel,))

    indices_array = np.moveaxis(np.indices(img.size), 0, 2)

    all_array = np.dstack((indices_array, colour_array)).reshape(
        (-1, dimensions_count_per_pixel + 2))

    dataframe = pd.DataFrame(all_array, columns=_BASE_COLUMNS + columns)

    dataframe[_BASE_COLUMNS] = dataframe[_BASE_COLUMNS].applymap(np.int32)

    return dataframe
