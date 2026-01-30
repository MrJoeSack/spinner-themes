"""Regenerate all thumbnails with bolder, tighter compositions."""
import httpx
import base64
import os
import time
from pathlib import Path
from PIL import Image, ImageOps
from io import BytesIO

# All prompts emphasize BOLD DARK LINES and TIGHT FRAMING
THEMES = [
    {
        "name": "passive-aggressive",
        "prompt": "BOLD black ink sketch, tight framing. A yellow sticky note with an unsettling too-wide smiley face. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "existential-dread",
        "prompt": "BOLD black ink sketch, tight framing. Tiny stick figure pushing huge boulder up steep hill into black void above. Heavy dark lines, high contrast. Dramatic composition filling frame. White background."
    },
    {
        "name": "ai-hype",
        "prompt": "BOLD black ink sketch, tight framing. Eldritch tentacled creature wearing a cheerful smiley face theatre mask. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "robert-greene",
        "prompt": "BOLD black ink sketch, tight framing. Chess pawn piece casting a shadow shaped like a king. Heavy dark lines, dramatic shadow. High contrast. Fills the frame. White background."
    },
    {
        "name": "fran-lebowitz",
        "prompt": "BOLD black ink sketch, tight framing. Typewriter with blank page, overflowing ashtray with cigarette butts. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "silicon-valley",
        "prompt": "BOLD black ink sketch, tight framing. Compass with needle spinning wildly in circles, motion lines. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "tech-bro",
        "prompt": "BOLD black ink sketch, tight framing. Person meditating peacefully inside a large ice cube. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "product-manager",
        "prompt": "BOLD black ink sketch, tight framing. Parking lot full of cars, each car has tiny lightbulb on roof. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "rto-excuses",
        "prompt": "BOLD black ink sketch, tight framing. Office badge on lanyard showing tiny sad face behind turnstile bars. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "back-from-vacation",
        "prompt": "BOLD black ink sketch, tight framing. Person in Hawaiian shirt and sunglasses crushed under massive pile of envelopes. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "iphone-user",
        "prompt": "BOLD black ink sketch, tight framing. Green speech bubble with embarrassed face, sweat drops. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "android-user",
        "prompt": "BOLD black ink sketch, tight framing. Smartphone shaped like swiss army knife with too many tools popping out chaotically. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "marathon-identity",
        "prompt": "BOLD black ink sketch, tight framing. Huge oval 26.2 bumper sticker completely covering a tiny car. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "the-shining",
        "prompt": "BOLD black ink sketch, tight framing. Old typewriter with page showing same wavy line repeated obsessively in rows. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "dark-tower",
        "prompt": "BOLD black ink sketch, tight framing. Single rose growing through cracked concrete, dark tower silhouette in background. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "therapy-speak",
        "prompt": "BOLD black ink sketch, tight framing. Circular feelings wheel diagram with all segments pointing to the word VALID in center. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "performative",
        "prompt": "BOLD black ink sketch, tight framing. Two cupped hands held reverently but holding absolutely nothing, empty space glowing. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "i-claudius",
        "prompt": "BOLD black ink sketch, tight framing. Ornate Roman bowl of figs, one fig has tiny skull symbol. Greek key pattern on bowl. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "sql-server",
        "prompt": "BOLD black ink sketch, tight framing. Two graph lines diverging wildly - one flat labeled '1', other shooting up exponentially. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "layoff-speak",
        "prompt": "BOLD black ink sketch, tight framing. Cardboard box containing laptop, wilted plant, lanyard hanging over edge. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "small-store",
        "prompt": "BOLD black ink sketch, tight framing. Dotted footprint path showing circular walking pattern inside tiny shop outline. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "ending-phone-call",
        "prompt": "BOLD black ink sketch, tight framing. Three speech bubbles in row, each with waving hand, getting more frantic. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "week-in-france",
        "prompt": "BOLD black ink sketch, tight framing. Smug croissant wearing beret looking down at sad plain bagel. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "dorinda-medley",
        "prompt": "BOLD black ink sketch, tight framing. Decorative fish mounted on wall plaque looking nervous/worried. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "twin-peaks",
        "prompt": "BOLD black ink sketch, tight framing. Coffee percolator with fish swimming inside instead of coffee. Surreal. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "breaking-bad",
        "prompt": "BOLD black ink sketch, tight framing. Chemistry beaker with blue crystals inside, sitting on periodic table square showing Br and Ba. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
    {
        "name": "better-call-saul",
        "prompt": "BOLD black ink sketch, tight framing. Sleazy lawyer figure doing finger guns pose next to inflatable waving tube man. Heavy dark outlines, high contrast. Fills the frame. White background."
    },
]


def autocrop_image(img, padding=20):
    """Crop whitespace from image, aggressive."""
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

    success = 0
    failed = 0

    for theme in THEMES:
        if generate_thumbnail(theme, output_dir):
            success += 1
        else:
            failed += 1
        time.sleep(1.5)

    print(f"\nDone: {success} success, {failed} failed")


if __name__ == "__main__":
    main()
