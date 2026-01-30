"""Generate thumbnails for Breaking Bad and Better Call Saul."""
import httpx
import base64
import os
from pathlib import Path
from PIL import Image, ImageOps
from io import BytesIO

THEMES = [
    {
        "name": "breaking-bad",
        "prompt": "Minimalist sketch. A chemistry beaker with blue crystals inside, sitting on a periodic table element square labeled 'Br' and 'Ba'. Simple line art, white background. No other text."
    },
    {
        "name": "better-call-saul",
        "prompt": "Minimalist sketch. A business card bent/folded in half, with a tiny figure in a suit doing finger guns pose next to it. Sleazy lawyer energy. Simple line art, white background. No text."
    },
]


def autocrop_image(img, padding=30):
    """Crop whitespace from image."""
    if img.mode in ('RGBA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[3])
        else:
            background.paste(img)
        img = background

    inverted = ImageOps.invert(img)
    bbox = inverted.getbbox()

    if bbox:
        left = max(0, bbox[0] - padding)
        top = max(0, bbox[1] - padding)
        right = min(img.width, bbox[2] + padding)
        bottom = min(img.height, bbox[3] + padding)

        width = right - left
        height = bottom - top
        size = max(width, height)

        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        new_left = max(0, center_x - size // 2)
        new_top = max(0, center_y - size // 2)
        new_right = min(img.width, new_left + size)
        new_bottom = min(img.height, new_top + size)

        if new_right - new_left < size:
            new_left = max(0, new_right - size)
        if new_bottom - new_top < size:
            new_top = max(0, new_bottom - size)

        img = img.crop((new_left, new_top, new_right, new_bottom))

    return img.resize((400, 400), Image.Resampling.LANCZOS)


def generate_thumbnail(theme: dict, output_dir: Path) -> bool:
    """Generate a single thumbnail."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set")
        return False

    output_path = output_dir / f"{theme['name']}.png"
    print(f"Generating: {theme['name']}...")

    try:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://joesack.com",
                "X-Title": "Spinner Theme Thumbnails"
            },
            json={
                "model": "google/gemini-2.5-flash-image",
                "messages": [{"role": "user", "content": theme["prompt"]}],
                "image_config": {"aspect_ratio": "1:1"}
            },
            timeout=120.0
        )

        if response.status_code != 200:
            print(f"  ERROR: {response.status_code} - {response.text[:200]}")
            return False

        data = response.json()
        message = data.get("choices", [{}])[0].get("message", {})

        if "images" not in message:
            print(f"  ERROR: No images in response")
            return False

        url = message["images"][0]["image_url"]["url"]
        _, b64 = url.split(",", 1)

        img = Image.open(BytesIO(base64.b64decode(b64)))
        img = autocrop_image(img)
        img.save(output_path)

        print(f"  SAVED: {output_path}")
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    output_dir = Path(__file__).parent / "thumbnails"
    output_dir.mkdir(exist_ok=True)

    for theme in THEMES:
        generate_thumbnail(theme, output_dir)

    print("Done!")


if __name__ == "__main__":
    main()
