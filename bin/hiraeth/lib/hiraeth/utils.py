#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import contextlib
import errno
import subprocess

from PIL import Image
from pilkit import processors, utils

@contextlib.contextmanager
def cd(path):
    """Context manger. cds to path, cds back at end of context

    :param path: path into which context should change
    """
    old_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_path)


def is_jpeg(filename):
    try:
        i = Image.open(filename)
        return i.format == 'JPEG'
    except IOError:
        return False


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def resize_gif(img, output, width, height):
    """DUMB."""
    size = '{}x{}'.format(width, height)

    resize_cmd = ['gifsicle', '-i', img.src_path, '--resize', size]
    with open(output, 'wb+') as f:
        subprocess.Popen(resize_cmd, stdout=f)


def resize_image(img, output, side=360):
    ow, oh = img.image.size

    if ow > oh:
        h = int(float(side) / float(ow) * float(oh))
        w = side
    else:
        h = side
        w = int(float(side) / float(oh) * float(ow))

    if img.image.format.lower() == 'gif':
        resize_gif(img, output, w, h)
        return

    processor = processors.SmartResize(w, h)
    new_img = processor.process(img.image)

    utils.save_image(new_img, output, img.image.format)
