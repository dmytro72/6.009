#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

# NO ADDITIONAL IMPORTS ALLOWED!


def create_blur_kernel(n, c=1):
    """
    Create kernel for box blur
    """
    val = c / n ** 2
    return [[val] * n for _ in range(n)]


class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def _get_index(self, x, y):
        """
        Compute index of the pixel in a row-major list of pixels
        """
        return y * self.width + x

    def get_pixel(self, x, y):
        """
        Return a value of the pixel
        """
        return self.pixels[self._get_index(x, y)]

    @staticmethod
    def _transform_coordinate(x, max_x):
        """
        If coordinate is not in domain, return correct coordinate in domain
        """
        return min(max(0, x), max_x-1)

    def get_unbounded_pixel(self, x, y):
        """
        Can return a value of the pixel for coordinates, which not in domain
        """
        x_transformed = self._transform_coordinate(x, self.width)
        y_transformed = self._transform_coordinate(y, self.height)
        return self.get_pixel(x_transformed, y_transformed)

    def set_pixel(self, x, y, c):
        """
        Change a value of the pixel
        """
        self.pixels[self._get_index(x, y)] = c

    def apply_per_pixel(self, func):
        """
        Apply function to the every pixel
        """
        result = Image.new(self.width, self.height)
        for x in range(result.width):
            for y in range(result.height):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor)
        return result

    def inverted(self):
        """
        Invert value of pixels
        """
        return self.apply_per_pixel(lambda c: 255-c)

    def correlate(self, kernel):
        """
        Apply kernel to image and yield a new image
        """
        result = Image.new(self.width, self.height)
        kern_size = len(kernel)
        center = kern_size // 2
        for base_x in range(self.width):
            x = base_x - center
            for base_y in range(self.height):
                y = base_y - center
                c = 0
                for dx in range(kern_size):
                    for dy in range(kern_size):
                        c += self.get_unbounded_pixel(x+dx, y+dy) * kernel[dy][dx]
                result.set_pixel(base_x, base_y, c)
        return result

    def _clip(self):
        """
        Correct pixels value in the image. Result is a new image
        """
        min_val = 0
        max_val = 255
        return Image(self.width,
                     self.height,
                     [min(max_val, max(min_val, round(c))) for c in self.pixels])

    def blurred(self, n):
        """
        Apply box blur to the image. Result is a new image
        """
        kernel = create_blur_kernel(n)
        return self.correlate(kernel)._clip()

    def sharpened(self, n):
        """
        Apply unsharp mask filter to the image. Result is a new image
        """
        kernel = create_blur_kernel(n, -1)
        center = n // 2
        kernel[center][center] += 2
        return self.correlate(kernel)._clip()

    def edges(self):
        """
        Apply Sobel operator to te image. Result is a new image
        """
        kx = ((-1, 0, 1),
              (-2, 0, 2),
              (-1, 0, 1))
        ky = ((-1, -2, -1),
              (0, 0, 0),
              (1, 2, 1))
        ox = self.correlate(kx)
        oy = self.correlate(ky)
        return Image(self.width,
                     self.height,
                     [math.sqrt(a**2 + b**2)
                      for a, b in zip(ox.pixels, oy.pixels)])._clip()

    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    def __repr__(self):
        return "Image(%s, %s, %s)" % (self.width, self.height, self.pixels)

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for _ in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)

        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()

    def reafter():
        tcl.after(500, reafter)
    tcl.after(500, reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
