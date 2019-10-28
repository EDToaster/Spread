import json
import math
from PIL import Image

class JSONObject:
  def __init__( self, dict ):
      vars(self).update( dict )

def lerp(v, dl, dh, rl, rh):
    factor = (v - dl) / (dh - dl)
    return rl + (rh - rl) * factor

def get_config(config_file):
    with open(config_file, "r") as fp:
        file_contents = fp.read()

    monitors = json.loads(file_contents, object_hook=JSONObject)
    return monitors


def construct_bounds(monitors):
    minx = math.inf
    miny = math.inf

    maxx = -math.inf
    maxy = -math.inf

    for bound in [m.dimensions for m in monitors]:
        [x, y, w, h] = bound

        minx = min(x, minx)
        miny = min(y, miny)
        maxx = max(x + w, maxx)
        maxy = max(y + h, maxy)

    return (minx, miny, maxx, maxy)


def convert_image_true_bounds(image_size, g_dimensions):
    (gminx, gminy, gmaxx, gmaxy) = g_dimensions
    iw, ih = image_size

    wr = iw / (gmaxx - gminx)
    hr = ih / (gmaxy - gminy)

    if hr > wr:
        # if hr > wr, we know that our image is "too tall", shrink image height
        return (iw, (gmaxy - gminy) * wr)
    else:
        # otherwise, "too wide", shrink image width
        return ((gmaxx - gminx) * hr, ih)

def convert_to_pixel_bounds(image_size, g_dimensions, dimensions):
    (gminx, gminy, gmaxx, gmaxy) = g_dimensions
    [x, y, w, h] = dimensions
    iw, ih = image_size

    iminx = lerp(x, gminx, gmaxx, 0, iw)
    iminy = lerp(y, gminy, gmaxy, 0, ih)
    imaxx = lerp(x + w, gminx, gmaxx, 0, iw)
    imaxy = lerp(y + h, gminy, gmaxy, 0, ih)

    return (iminx, iminy, imaxx, imaxy)



CONFIG_FILENAME = "config.json"
FOLDER = "out/"
EXTENSION = ".png"

def main():
    config = get_config(CONFIG_FILENAME)
    global_dimensions = construct_bounds(config.monitors)

    image = Image.open(config.image)

    true_image_bounds = convert_image_true_bounds(image.size, global_dimensions)
    
    for monitor in config.monitors:
        bounds = convert_to_pixel_bounds(true_image_bounds, global_dimensions, monitor.dimensions)
        image.crop(bounds).save(FOLDER + monitor.name + EXTENSION)


if __name__ == "__main__":
    main()
