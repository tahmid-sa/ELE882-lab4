import numpy as np
from skimage.transform import rescale, resize
from skimage.util import img_as_float


class YCbCrColourSpace:
    '''Convert an image between the YCbCr and RGB colour spaces.

    The class implements the JPEG varient of YCbCr with support for optional
    chroma subsampling.  The subsampling is represented as a positive integer,
    so a subsampling factor of '2' means the dimensions of the chroma channels
    are half of the luma channel.

    Attributes
    ----------
    sampling : int
        subsampling factor
    '''
    def __init__(self, sampling=1):
        '''Initialize the YCbCr to RGB converter.

        Parameters
        ----------
        sampling : int, optional
            the YCbCr chroma subsampling factor; defaults to '1' or no
            subsampling

        Raises
        ------
        ValueError
            if the sampling factor is less than '1'
        '''
        if sampling < 1:
            raise ValueError('Sampling factor must be larger than "1".')
        self.sampling = sampling

    def to_ycbcr(self, img):

        if img.ndim != 3:
            raise ValueError("The image must be a 3-channel colour image.")

        height, width, ch = img.shape
        out = np.zeros((height, width, ch))

        for h in range(height):
            for w in range(width):
                for c in range(ch):
                    if c == 0:
                        out[h, w, c] = 0.299*img[h, w, 0] + 0.587*img[h, w, 1] + 0.114*img[h, w, 2]
                    if c == 1:
                        out[h, w, c] = -0.1687*img[h, w, 0] - 0.3313*img[h, w, 1] + 0.5*img[h, w, 2]
                    if c == 2:
                        out[h, w, c] = 0.5*img[h, w, 0] - 0.4187*img[h, w, 1] - 0.0813*img[h, w, 2]

        y = out[:, :, 0]
        cbcr = out[:, :, 1:3]

        if img.dtype == np.uint8:
            y = img_as_float(y) / 255.0
            cbcr = img_as_float(cbcr) / 255.0

        return y, cbcr

    def to_rgb(self, Y, CbCr):

        if Y.ndim != 2:
            raise ValueError('Y must be a single channel image.')
        if CbCr.shape[2] != 2 or np.any(CbCr) < np.any(Y):
            raise ValueError('uv must be a two channel image and smaller than Y.')

        height, width = Y.shape

        CbCr = YCbCrColourSpace._upsample(self, CbCr, (height, width))
        rgb = np.zeros((height, width, 3))

        for h in range(height):
            for w in range(width):
                for c in range(3):
                    if c == 0:
                        rgb[h, w, c] = 1*Y[h, w] + 0*CbCr[h, w, 0] + 1.402*CbCr[h, w, 1]
                    if c == 1:
                        rgb[h, w, c] = 1*Y[h, w] - 0.34414*CbCr[h, w, 0] - 0.71414*CbCr[h, w, 1]
                    if c == 2:
                        rgb[h, w, c] = 1*Y[h, w] + 1.772*CbCr[h, w, 0] + 0*CbCr[h, w, 1]

        if np.average(rgb) > 1 or np.average(rgb) < -1:
            rgb = img_as_float(rgb) / 255.0

        return img_as_float(rgb).clip(-1, 1)

    def _downsample(self, c):
        '''Downsample a single-channel image.

        Parameters
        ----------
        c : numpy.ndarray
            input image
        '''
        return rescale(c, 1 / self.sampling, mode='edge', anti_aliasing=True)

    def _upsample(self, c, outsz):
        '''Upsample a single-channel image to match a specified output size.

        Parameters
        ----------
        c : numpy.ndarray
            input image
        outsz : tuple of ``(height, width)``
            the expected output size
        '''
        return resize(c, outsz, mode='edge', anti_aliasing=True)
