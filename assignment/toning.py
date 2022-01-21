import numpy as np
from skimage.color import hsv2rgb, rgb2hsv
from skimage.util import img_as_float

from assignment.adjustment import to_monochrome


def single_tone(img, hue, saturation, amount=1.0):

    if hue > 360 or hue < 0:
        raise ValueError("The hue must be in the range [0, 360].")
    if saturation > 1 or saturation < 0 or amount > 1 or amount < 0:
        raise ValueError("The saturation and amount must be in the range [0, 1].")
    img = img_as_float(img)
    if img.ndim == 3:
        img_hsv = rgb2hsv(img)
        img_hsv[:, :, 0] = hue / 360
        img_hsv[:, :, 1] = saturation

        return img_as_float(hsv2rgb(img_hsv)).clip(-1, 1)
    if img.ndim == 2:
        height, width = img.shape
        img_rgb = np.zeros((height, width, 3))

        for h in range(height):
            for w in range(width):
                for c in range(3):
                    img_rgb[h][w][c] = img[h][w]

        img_hsv = rgb2hsv(img_rgb)
        img_hsv[:, :, 0] = hue / 360
        img_hsv[:, :, 1] = saturation

        return img_as_float(hsv2rgb(img_hsv)).clip(-1, 1)


def split_tone(img, highlight, shadow):

    img = img_as_float(img)

    iH = single_tone(img, highlight[0] * 360, highlight[1])
    iS = single_tone(img, shadow[0] * 360, shadow[1])

    gR = to_monochrome(img, 0.299, 0.587, 0.114)
    gR = np.array(np.stack((gR, gR, gR), axis=2))
    m = gR / np.max(gR)

    return img_as_float(m * iH + ((1 - m) * iS)).clip(-1, 1)
