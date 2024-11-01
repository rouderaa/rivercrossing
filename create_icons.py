from PIL import Image, ImageDraw
import numpy as np
import os
import sys

from PIL import Image, ImageDraw

from PIL import Image
import numpy as np


def replace_transparent_with_dimmed(image, background_color=(255, 255, 255)):
    """
    Replace transparent pixels with dimmed colors based on alpha value,
    blending with a white background.

    Parameters:
    image: PIL.Image.Image
        The input image with transparency (must be in RGBA mode)
    background_color: tuple
        RGB values for the background color (default is white)

    Returns:
    PIL.Image.Image
        New image with transparency replaced by dimmed colors
    """
    # Convert image to RGBA if it isn't already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Convert to numpy array for faster processing
    img_array = np.array(image, dtype=np.float32)

    # Normalize alpha channel to range 0-1
    alpha = img_array[:, :, 3] / 255.0

    # Create 3D alpha array for broadcasting
    alpha_3d = np.stack([alpha] * 3, axis=-1)

    # Create background color array of same shape as RGB channels
    background = np.full_like(img_array[:, :, :3], background_color, dtype=np.float32)

    # Blend colors based on alpha value
    # Formula: result = (foreground * alpha) + (background * (1 - alpha))
    blended_colors = (img_array[:, :, :3] * alpha_3d) + (background * (1 - alpha_3d))

    # Create result array with full opacity
    result_array = np.zeros_like(img_array)
    result_array[:, :, :3] = blended_colors
    result_array[:, :, 3] = 255  # Set full opacity

    # Convert back to uint8 type
    result_array = result_array.astype(np.uint8)

    # Convert back to PIL Image
    result_image = Image.fromarray(result_array)
    return result_image


def preview_with_checkerboard(image, checker_size=10):
    """
    Create a preview of the image with a checkerboard background to better
    visualize the transparency effects.

    Parameters:
    image: PIL.Image.Image
        The input image
    checker_size: int
        Size of each checker square in pixels

    Returns:
    PIL.Image.Image
        Image with checkerboard background
    """
    # Get image size
    width, height = image.size

    # Create checkerboard pattern
    checker = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    for y in range(0, height, checker_size):
        for x in range(0, width, checker_size):
            if ((x // checker_size) + (y // checker_size)) % 2:
                box = (x, y, min(x + checker_size, width), min(y + checker_size, height))
                checker.paste((200, 200, 200, 255), box)

    # Composite the image over the checkerboard
    return Image.alpha_composite(checker, image.convert('RGBA'))

def create_vignette(input_path, output_path, border_color=(144, 238, 144, 255), border_width=20):
    # Open the image
    img = Image.open(input_path)

    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # remove transparent pixels by opaque white pixels
    img = replace_transparent_with_dimmed(img)

    # Create a new transparent image for the mask
    mask = Image.new('L', img.size, 0)  # 'L' mode for single-channel mask
    draw = ImageDraw.Draw(mask)

    # Calculate dimensions
    width, height = img.size
    center_x = width // 2
    center_y = height // 2
    radius = min(center_x, center_y)

    # Draw a white circle on the mask (white areas will be visible)
    draw.ellipse([center_x - radius, center_y - radius,
                  center_x + radius, center_y + radius],
                 fill=255)

    # Create a white background image
    white_bg = Image.new('RGBA', img.size, (255, 255, 255, 255))

    # Create final image with transparent background
    result = Image.new('RGBA', img.size, (0, 0, 0, 0))

    # First, paste the white background using the mask
    result.paste(white_bg, mask=mask)

    # Then paste the original image using the same mask
    result.paste(img, mask=mask)

    # Draw the border on top
    draw_border = ImageDraw.Draw(result)
    draw_border.ellipse([center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius],
                        outline=border_color, width=border_width)

    # Save the result
    result.save(output_path, 'PNG')

def process_directory(input_dir="assets", output_dir="assets_with_vignette"):
    """
    Process all PNG files in the input directory and save them to the output directory
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get list of PNG files in input directory
    png_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]

    if not png_files:
        print(f"No PNG files found in {input_dir}")
        return

    # Process each PNG file
    for png_file in png_files:
        input_path = os.path.join(input_dir, png_file)
        output_path = os.path.join(output_dir, f"vignette_{png_file}")

        try:
            print(f"Processing: {png_file}")
            create_vignette(input_path, output_path)
            print(f"Created: {output_path}")
        except Exception as e:
            print(f"Error processing {png_file}: {str(e)}")


if __name__ == "__main__":
    # Check if input and output paths are provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_path> <output_path>")
        print("Example: python script.py ./assets ./output")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Validate input path exists
    if not os.path.exists(input_path):
        print(f"Error: Input path '{input_path}' does not exist")
        sys.exit(1)

    # Process the directory
    process_directory(input_path, output_path)