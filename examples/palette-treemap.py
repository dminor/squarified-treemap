#
# Copyright (c) 2013 Daniel Minor
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

#
# Create a treemap of the colours used in a image.
#

import Image
import ImageDraw
import math
import random
import sys

# Modify path so we can find treemap
sys.path.append('..')

import treemap.treemap as treemap

# output image dimension
DIM = 250

if len(sys.argv) < 2:
    print('usage: %s <file> ...' % sys.argv[0])
    sys.exit()

# get list of image filenames to process
images = sys.argv[1:]

# iterate through each image specified, and count the number of pixels of
# each colour
colours = {}
for image in images:
    im = Image.open(image)
    width, height = im.size
    data = im.getdata()

    palette = im.getpalette()

    for datum in data:
        if palette:
            key = (palette[datum*3], palette[datum*3 + 1], palette[datum*3 + 2])
        else:
            key = datum

        if colours.has_key(key):
            colours[key] += 1
        else:
            colours[key] = 1

#we take at most the 20 most commonly used colours, then normalize the areas
values = sorted(colours.iteritems(), key=lambda x: x[1], reverse=True)[:20]
area = sum(map(lambda x: float(x[1]), values))
values = map(lambda x: (x[0], float(x[1])/area), values)

# create output file
out = Image.new(mode='RGB', size=(DIM, DIM))
draw = ImageDraw.ImageDraw(out)

def renderfn(pos, col):
    #convert from normalized coordinates back to image coordinates
    draw.rectangle((2+pos[0]*(DIM-4), 2+pos[1]*(DIM-4),math.ceil(2+pos[2]*(DIM-4)), math.ceil(2+pos[3]*(DIM-4))), col)

treemap = treemap.Treemap(values)
treemap.render(renderfn)

out.save('treemap.jpg')
