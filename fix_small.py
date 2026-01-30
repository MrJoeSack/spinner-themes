"""Regenerate small/whitespace-heavy thumbnails with zoomed-in compositions."""
import httpx
import base64
import os
import time
from pathlib import Path
from PIL import Image, ImageOps
from io import BytesIO

FIXES = [
    {
        "name": "small-store",
        "prompt": "EXTREME CLOSE-UP, fills entire frame edge to edge. Bold black ink. A person's feet walking in a circle pattern, shown from above, footprints making a loop. The feet and footprints fill the ENTIRE image, no margins. Heavy black lines."
    },
    {
        "name": "i-claudius",
        "prompt": "EXTREME CLOSE-UP, fills entire frame edge to edge. Bold black ink. A Roman bowl overflowing with figs, one fig has a tiny skull on it. Greek key pattern on bowl rim. Bowl is HUGE and fills entire frame corner to corner. Heavy black lines."
    },
    {
        "name": "ending-phone-call",
        "prompt": "EXTREME CLOSE-UP, fills entire frame. Bold black ink. Three waving hands getting progressively more frantic/desperate, shown very large filling the frame. Heavy black outlines, high contrast."
    },
    {
        "name": "therapy-speak",
        "prompt": "EXTREME CLOSE-UP, fills entire frame edge to edge. Bold black ink. A circular wheel diagram divided into segments, the word VALID written in several segments. Wheel fills entire frame corner to corner. Heavy black lines."
    },
    {
        "name": "marathon-identity",
        "prompt": "EXTREME CLOSE-UP, fills entire frame. Bold black ink. A huge oval 26.2 bumper sticker shown very large, almost bursting out of frame, on back of tiny car. Sticker dominates image. Heavy black lines."
    },
    {
        "name": "fran-lebowitz",
        "prompt": "EXTREME CLOSE-UP, fills entire frame edge to edge. Bold black ink. Typewriter keys and paper with blank page, overflowing ashtray with cigarettes, shown very large filling entire frame. Heavy black lines, high contrast."
    },
]


def autocrop(img, padding=8):
    """Tight crop."""
    if img.mode in ('RGBA', 'P'):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA':
            bg.paste(img, mask=img.split()[3])
        else:
            bg.paste(img)
        img = bg

    inv = ImageOps.invert(img)
    bbox = inv.getbbox()

    if bbox:
        l, t, r, b = bbox
        l, t = max(0, l - padding), max(0, t - padding)
        r, b = min(img.width, r + padding), min(img.height, b + padding)
        w, h = r - l, b - t
        size = max(w, h)
        cx, cy = (l + r) // 2, (t + b) // 2
        nl, nt = cx - size // 2, cy - size // 2
        nr, nb = nl + size, nt + size
        if nl < 0: nr -= nl; nl = 0
        if nt < 0: nb -= nt; nt = 0
        if nr > img.width: nl -= (nr - img.width); nr = img.width
        if nb > img.height: nt -= (nb - img.height); nb = img.height
        img = img.crop((max(0, nl), max(0, nt), min(img.width, nr), min(img.height, nb)))

    return img.resize((400, 400), Image.Resampling.LANCZOS)


def generate(theme: dict, output_dir: Path) -> bool:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    output_path = output_dir / f"{theme['name']}.png"
    print(f"Regenerating: {theme['name']}...")

    try:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://joesack.com",
                "X-Title": "Spinner Thumbnails"
            },
            json={
                "model": "google/gemini-2.5-flash-image",
                "messages": [{"role": "user", "content": theme["prompt"]}],
                "image_config": {"aspect_ratio": "1:1"}
            },
            timeout=120.0
        )

        if response.status_code != 200:
            print(f"  ERROR: {response.status_code}")
            return False

        data = response.json()
        msg = data.get("choices", [{}])[0].get("message", {})
        if "images" not in msg:
            print(f"  ERROR: No images")
            return False

        url = msg["images"][0]["image_url"]["url"]
        _, b64 = url.split(",", 1)
        img = Image.open(BytesIO(base64.b64decode(b64)))
        img = autocrop(img)
        img.save(output_path)
        print(f"  SAVED: {output_path}")
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    output_dir = Path(__file__).parent / "thumbnails"
    for theme in FIXES:
        generate(theme, output_dir)
        time.sleep(2)
    print("Done!")


if __name__ == "__main__":
    main()
