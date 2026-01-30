"""Auto-crop whitespace from thumbnail images."""
from PIL import Image, ImageOps
from pathlib import Path


def autocrop_image(input_path: Path, output_path: Path, padding: int = 20):
    """Crop whitespace from image, keeping small padding."""
    img = Image.open(input_path)

    # Convert to RGB if needed
    if img.mode in ('RGBA', 'P'):
        # Create white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[3])
        else:
            background.paste(img)
        img = background

    # Get bounding box of non-white content
    # Invert so white becomes black (0), find bbox of non-zero
    inverted = ImageOps.invert(img)
    bbox = inverted.getbbox()

    if bbox:
        # Add padding
        left = max(0, bbox[0] - padding)
        top = max(0, bbox[1] - padding)
        right = min(img.width, bbox[2] + padding)
        bottom = min(img.height, bbox[3] + padding)

        # Make it square (use larger dimension)
        width = right - left
        height = bottom - top
        size = max(width, height)

        # Center the content in square
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        new_left = max(0, center_x - size // 2)
        new_top = max(0, center_y - size // 2)
        new_right = min(img.width, new_left + size)
        new_bottom = min(img.height, new_top + size)

        # Adjust if we hit edges
        if new_right - new_left < size:
            new_left = new_right - size
        if new_bottom - new_top < size:
            new_top = new_bottom - size

        cropped = img.crop((new_left, new_top, new_right, new_bottom))
    else:
        cropped = img

    # Resize to consistent size
    cropped = cropped.resize((400, 400), Image.Resampling.LANCZOS)
    cropped.save(output_path)
    print(f"Cropped: {input_path.name}")


def main():
    thumb_dir = Path(__file__).parent / "thumbnails"

    for png in thumb_dir.glob("*.png"):
        autocrop_image(png, png, padding=30)

    print("Done!")


if __name__ == "__main__":
    main()
