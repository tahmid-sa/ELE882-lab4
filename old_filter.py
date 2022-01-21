<<<<<<< HEAD
import argparse
import numpy as np
from skimage import io
from assignment.adjustment import to_monochrome
from assignment.toning import split_tone

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_image', type=str)
    parser.add_argument('output_image', type=str)
    return parser.parse_args()

def perform_filter(input_image, output_image):

    img = io.imread(input_image, as_gray=False)
    
    highlight = (45/360, 15/100)
    shadow = (0/360, 10/100)
    img_split = split_tone(img, highlight, shadow)
    
    height, width, ch = img.shape
    gauss = np.random.randn(height, width, ch)
    gauss = gauss.reshape(height, width, ch)
    noisy = img_split + (img_split * (gauss / 400))

    img_old = (noisy * 255.0).astype(np.uint8)
    io.imsave(output_image, img_old)

def main():

    args = get_args()
    
    print(f'Input image filename: {args.input_image}')
    input_image = f'{args.input_image}'

    print(f'Output image filename: {args.output_image}')
    output_image = f'{args.output_image}'

    perform_filter(input_image, output_image)

if __name__ == "__main__":
=======
import argparse
import numpy as np
from skimage import io
from assignment.adjustment import to_monochrome
from assignment.toning import split_tone

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_image', type=str)
    parser.add_argument('output_image', type=str)
    return parser.parse_args()

def perform_filter(input_image, output_image):

    img = io.imread(input_image, as_gray=False)
    
    highlight = (45/360, 15/100)
    shadow = (0/360, 10/100)
    img_split = split_tone(img, highlight, shadow)
    
    height, width, ch = img.shape
    gauss = np.random.randn(height, width, ch)
    gauss = gauss.reshape(height, width, ch)
    noisy = img_split + (img_split * (gauss / 400))

    img_old = (noisy * 255.0).astype(np.uint8)
    io.imsave(output_image, img_old)

def main():

    args = get_args()
    
    print(f'Input image filename: {args.input_image}')
    input_image = f'{args.input_image}'

    print(f'Output image filename: {args.output_image}')
    output_image = f'{args.output_image}'

    perform_filter(input_image, output_image)

if __name__ == "__main__":
>>>>>>> 4a41c02b0a7f0f026da044dab6a338438c8681a2
    main()