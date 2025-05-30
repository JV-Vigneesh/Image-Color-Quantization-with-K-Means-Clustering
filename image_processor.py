from PIL import Image
import numpy as np


def load_image_and_get_dimensions(image_path):
    try:
        with Image.open(image_path).convert("RGB") as image:
            pixel_array = np.array(image)
            height, width, _ = pixel_array.shape
        return pixel_array, height, width
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None, None


def create_image_from_pixels(pixel_array, height, width, output_path=None):
    try:
        pixel_array = pixel_array.reshape(height, width, -1).astype(np.uint8)
        image = Image.fromarray(pixel_array, "RGB")
        if output_path:
            image.save(output_path)
            print(f"Image saved to '{output_path}'.")
        return image
    except Exception as e:
        print(f"Error creating image: {e}")
        return None
