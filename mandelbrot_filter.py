from PIL import Image
import numpy as np
import colour_map

def _map(val, r1, r2, nr1, nr2):
    return ((val - r1) / (r2 - r1) ) * (nr2 - nr1) + nr1

def colour_maths(_z, _z_count):    
    smoothed = np.log2( np.log2(_z.real**2 + _z.imag**2) / 2)
    colourI = int(np.sqrt(_z_count + 10 - smoothed) * 256) % len(colour_map.red)
    colour = (int(colour_map.red[colourI]), int(colour_map.green[colourI]), int(colour_map.blue[colourI]))
    
    return colour

while True:
    while True:
        img_input = input("Image: ")
        try:
            img = Image.open(rf"Pictures\{img_input}")
            break
        except FileNotFoundError:
            print("File not found.")

    # while True:
    #     try:
    #         strength = int(input("Strength: (0-10)"))
    #         break
    #     except ValueError:
    #         print("Please enter a valid value.")
        

    pixels = img.load()
    num_pixels = list(img.size)
    img_x = num_pixels[0]
    img_y = num_pixels[1]

    for x in range(img_x):
        for y in range(img_y):
            try:
                pixel_rgb = list(img.getpixel((x, y)))
                r = pixel_rgb[0]
                g = pixel_rgb[1]
                b = pixel_rgb[2]

                hex = '%02x%02x%02x' % (r, g, b)
                num = int(hex, 16)
                mono = np.ceil(_map(num, 0, 16777215, 0, 255))

                
                mapped_x = _map(x, 0, img_x-1, 4, 10)
                mapped_y = _map(x, 0, img_y-1, 4, 10)

                xy = complex(mapped_x, mapped_y)
                filter = colour_maths(xy, mono)
                
                pixel_rgb[0] = filter[0]
                pixel_rgb[1] = filter[1]
                pixel_rgb[2] = filter[2]
                # print(mono, filter)

                pixels[x, y] = tuple(pixel_rgb)
            except IndexError:
                continue

    img.save(rf"Pictures\Mandelbrot {img_input}")
    print("Image Saved.")