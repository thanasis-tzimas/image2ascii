from sys import argv
from PIL import Image
import numpy as np

if len(argv) < 2:
    print('No file was supplied')
    exit(-1)
elif len(argv) > 2:
    print('More than one file were supplied')
    exit(-1)

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


with Image.open(fp=argv[1]) as im:
    im = im.resize(size=ratio_fit(im.width, im.height, 84, 48))
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
