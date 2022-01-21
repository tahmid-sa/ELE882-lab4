import argparse

from skimage import io
from assignment.colour_space import YCbCrColourSpace

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_image', type=str)
    parser.add_argument('output_image', type=str)
    parser.add_argument('sampling_factor', type=float)

    return parser.parse_args()

def perform_chroma_resample(input_image, output_image, sampling_factor):

    img = io.imread(input_image)
    converter = YCbCrColourSpace(sampling_factor)

    y, cbcr = converter.to_ycbcr(img)

    height, width = y.shape
    cbcr = converter._upsample(cbcr, (height, width))
    rgb = converter.to_rgb(y, cbcr)

    io.imsave(output_image, rgb)

def main():

    args = get_args()

    print(f'Input filename: {args.input_image}')
    input_image = f'{args.input_image}'

    print(f'Output filename: {args.output_image}')
    output_image = f'{args.output_image}'

    print(f'Sampling factor: {args.sampling_factor}')
    sampling_factor = float(f'{args.sampling_factor}')

    perform_chroma_resample(input_image, output_image, sampling_factor)

if __name__ == "__main__":
    main()