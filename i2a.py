from PIL import Image
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser(
    prog='image2ascii',
    description='A simple and dumb image-to-ASCII converter'
)
parser.add_argument('filename', metavar='FILENAME', type=str)
parser.add_argument('target_width', metavar='WIDTH', type=int)
parser.add_argument('target_height', metavar='HEIGHT', type=int)
args = parser.parse_args()

char_ramp = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."


def ratio_fit(width, height, maxw, maxh):
    ratio = (maxw / width, maxh / height)
    ratio = min(ratio[0], ratio[1])
    return (int(width * ratio), int(height * ratio))


def normalize(arr):
    arr = arr.astype('float')
    for i in range(3):
        min = arr[..., i].min()
        max = arr[..., i].max()
        if min != max:
            arr[..., i] -= min
            arr[..., i] *= ((len(char_ramp)-1) / (max - min))
    return arr


with Image.open(fp=args.filename) as im:
    width, height = args.target_width, args.target_height
    im = im.resize(size=ratio_fit(im.width, im.height, width, height))
    im = im.convert(mode='RGBA')
    arr = np.array(im)
    im = Image.fromarray(normalize(arr).astype('uint8'), 'RGBA')
    im = im.convert(mode='L')
    with open('out.txt', 'w') as out:
        for h in range(im.height):
            for w in range(im.width):
                xy = w, h
                out.write(char_ramp[im.getpixel(xy)])
            out.write('\n')
