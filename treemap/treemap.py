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

class Treemap(object):

    """
    Squarified treemap implementation based upon the following paper:

        Bruls, M., Huizing, K., van Wijk, J. (1999) Squarified Treemaps
        In Proceedings of the Joint Eurographics and IEEE TCVP Symposium on
        Visualization, pp. 33--42

    """

    def __init__(self, items):
        """
            Initialize the treemap.

            items is an array of tuples, where the first component of the
            tuple is a label and the second is a normalized weight.
        """
        self.items = items

    def render(self, fn):

        """
            Render the treemap using the specified callback function.
            The function should take two arguments:

            The first is an tuple specifying a rectangle to render as
            (x0, y0, x1, y1) in normalized coordinates.

            The second is the label component of an item, as passed in to the
            constructor.
        """

        class Rect:
            """
                This class keeps track of the remaining area available in which
                to render rectangles.
            """

            def __init__(self, x, y, width, height):
                self.x = x
                self.y = y
                self.width = width
                self.height = height

            def side(self):
                return min(self.width, self.height)

        rect = Rect(0.0, 0.0, 1.0, 1.0)
        self.squarify(rect, fn)

    def layoutrow(self, rect, row, renderfn):

        """
            Layout a completed row, calling the renderfn callback to handle
            rendering it. Update the rect with the remaining area available
            to which to render.
        """

        area = sum([x[1] for x in row])

        if rect.width > rect.height:
            width = area / rect.height

            y = rect.y
            for item in row:
                height = item[1] / area * rect.height
                renderfn((rect.x, y, rect.x + width, y + height), item[0])
                y += height

            rect.width -= width
            rect.x += width
        else:
            height = area / rect.width

            x = rect.x
            for item in row:
                width = item[1] / area * rect.width
                renderfn((x, rect.y, x + width, rect.y + height), item[0])
                x += width

            rect.height -= height
            rect.y += height

    def squarify(self, rect, renderfn):

        """
            Iterate through all items, adding them to the current row until
            adding an item will cause the aspect ratio to become worse, in
            which case the item is added to a new row.
        """

        row = []

        for item in self.items:
            if self.improvesRatio(row, item, rect.side()):
                row.append(item)
            else:
                self.layoutrow(rect, row, renderfn)
                row = [item]

        if len(row):
            self.layoutrow(rect, row, renderfn)


    def improvesRatio(self, row, item, width):

        """
            Return true if adding the item to the row does not cause the
            aspect ratio of the row to become worse.
        """

        if len(row) == 0:
            return True
        else:
            areas = [x[1] for x in row]
            sm = sum(areas)
            mn = min(areas)
            mx = max(areas)

            current = max(width*width*mx/(sm*sm), sm*sm/(width*width*mn))

            sm += item[1]
            mn = min(mn, item[1])
            mx = max(mn, item[1])
            new = max(width*width*mx/(sm*sm), sm*sm/(width*width*mn))

            #Note: this inequality was wrong in the original paper
            return current >= new
