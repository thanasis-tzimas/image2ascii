from argparse import ArgumentParser
from PIL import Image

parser = ArgumentParser(
    prog='ascii2image',
    description='A simple and dumb ASCII-to-image converter'
)
parser.add_argument('filename', metavar='FILENAME', type=str)
args = parser.parse_args()

char_ramp = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."

with open(args.filename) as fp:
    out = Image.new(mode='L', size=(84, 48))
    txt = fp.readlines()
    x, y = 0, 0
    for line in txt:
        for char in line.strip('\n'):
            xy = x, y
            color_index = char_ramp.find(char)
            out.putpixel(xy, color_index)
            x += 1
        x = 0
        y += 1
    out.show()