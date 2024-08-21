# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2024 Uri Shaked, 2024 Leo Moser

import klayout.db as db
import argparse
from PIL import Image

def convert_to_gds(input_filepath, output_filepath, cellname='TOP', scale=1.0, threshold=128, merge=False, pixel_size=0.3):

    ly = db.Layout()
    ly.dbu = 0.001

    top = ly.create_cell(cellname)
    to_um = db.CplxTrans(ly.dbu)
    from_um = to_um.inverted()

    # Open the image
    img = Image.open(input_filepath)

    layer_met4_drawing = ly.layer(db.LayerInfo(71, 20))

    new_image = Image.new("RGBA", img.size, "WHITE") # Create a white rgba background
    new_image.paste(img, (0, 0), img)                # Paste the image on the background

    # Convert the image to grayscale
    new_image = new_image.convert("L")

    # Scale down the image
    new_image.thumbnail((new_image.width * scale, new_image.height * scale), Image.LANCZOS)

    # Use a region to merge pixels together
    if merge:
        top_region = db.Region()

    for y in range(new_image.height):
        for x in range(new_image.width):
            color = new_image.getpixel((x, y))
            if color < threshold:
                # Adjust y-coordinate to flip the image vertically
                flipped_y = new_image.height - y - 1
                
                pixel = db.DBox(0.0, 0.0, pixel_size, pixel_size).moved(x * pixel_size, flipped_y * pixel_size)
                
                if merge:
                    pixel_polygon = db.DPolygon(pixel)
                    top_region.insert(from_um * pixel_polygon)
                else:
                    top.shapes(layer_met4_drawing).insert(pixel)

    if merge:
        top_region.merge()
        top.shapes(layer_met4_drawing).insert(top_region)

    # Save the layout to a file
    ly.write(output_filepath)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='img2gds',
        description='Convert an image to GDS format'
    )

    parser.add_argument('image_path')
    parser.add_argument('gds_path')
    parser.add_argument('--cellname', default='TOP', help='top cellname')
    parser.add_argument('--pixel-size', type=float, default=0.3, help='pixel size in um')
    parser.add_argument('--scale', type=float, default=1.0, help='downscale the image, e.g. 0.5')
    parser.add_argument('--threshold', type=int, default=128, help='threshold to compare against')
    parser.add_argument('--merge', action='store_true', help='merge polygons')

    args = parser.parse_args()

    convert_to_gds(args.image_path, args.gds_path, cellname=args.cellname, scale=args.scale, threshold=args.threshold, merge=args.merge, pixel_size=args.pixel_size)
