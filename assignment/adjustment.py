# import numpy as np
from skimage.color import rgb2hsv, hsv2rgb
from skimage.util import img_as_float


def adjust_saturation(img, amount):

    if img.ndim != 3 or amount > 1 or amount < -1:
        raise ValueError("The input image isn't 3 channel or amount is not on [-1, 1].")

    img_hsv = rgb2hsv(img_as_float(img))
    img_hsv[:, :, 1] = img_hsv[:, :, 1] + amount*img_hsv[:, :, 1]

    return img_as_float(hsv2rgb(img_hsv)).clip(-1, 1)


def adjust_hue(img, amount):

    if img.ndim != 3:
        raise ValueError("The image isn't a 3 channel.")

    img_hsv = rgb2hsv(img_as_float(img))
    img_hsv[:, :, 0] = img_hsv[:, :, 0] + (amount / 360)

    return img_as_float(hsv2rgb(img_hsv) % 1)


def to_monochrome(img, wr, wg, wb):

    if img.ndim != 3 or wr < 0 or wg < 0 or wb < 0:
        raise ValueError("Image is not colour or weights are negative.")

    img = img_as_float(img)

    return img_as_float(wr*img[:, :, 0] + wg*img[:, :, 1] + wb*img[:, :, 2]).clip(-1, 1)
