""" simple image utils used across the app """

import random


try:
    import PIL
    del PIL
    from PIL import Image
except ImportError:
    raise ImportError("Python Imaigng Library (PIL) is required.")


def is_animated(infile):
    """ Checks if an image is animated (contains frames). """
    assert infile.tell() == 0
    try:
        infile.seek(1)
        infile.seek(0)
    except EOFError:
        return False
    return True


def random_line(afile):
    """Randomly chooses a line from a text file."""
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line
