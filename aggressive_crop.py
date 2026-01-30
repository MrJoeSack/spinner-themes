"""Aggressively crop whitespace from thumbnails."""
from PIL import Image, ImageOps
from pathlib import Path


def autocrop_aggressive(input_path: Path, padding: int = 10):
    """Crop whitespace very aggressively."""
    img = Image.open(input_path)

    # Convert to RGB if needed
    if img.mode in ('RGBA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[3])
        else:
            background.paste(img)
        img = background

    # Find bounding box of non-white content
    inverted = ImageOps.invert(img)
    bbox = inverted.getbbox()

    if bbox:
        # Very tight crop
        left = max(0, bbox[0] - padding)
        top = max(0, bbox[1] - padding)
        right = min(img.width, bbox[2] + padding)
        bottom = min(img.height, bbox[3] + padding)

        # Make square using the larger dimension
        width = right - left
        height = bottom - top
        size = max(width, height)

        # Center the content
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        new_left = center_x - size // 2
        new_top = center_y - size // 2
        new_right = new_left + size
        new_bottom = new_top + size

        # Clamp to image bounds
        if new_left < 0:
            new_right -= new_left
            new_left = 0
        if new_top < 0:
            new_bottom -= new_top
            new_top = 0
        if new_right > img.width:
            new_left -= (new_right - img.width)
            new_right = img.width
        if new_bottom > img.height:
            new_top -= (new_bottom - img.height)
            new_bottom = img.height

        cropped = img.crop((max(0, new_left), max(0, new_top),
                           min(img.width, new_right), min(img.height, new_bottom)))
    else:
        cropped = img

    # Resize to consistent size
    cropped = cropped.resize((400, 400), Image.Resampling.LANCZOS)
    cropped.save(input_path)
    print(f"Cropped: {input_path.name} (bbox: {bbox})")


def main():
    thumb_dir = Path(__file__).parent / "thumbnails"

    for png in sorted(thumb_dir.glob("*.png")):
        autocrop_aggressive(png, padding=8)

    print("\nDone!")


if __name__ == "__main__":
    main()
