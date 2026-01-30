"""Regenerate ALL thumbnails - COLORFUL, FRAME-FILLING, BOLD."""
import httpx
import base64
import os
import time
from pathlib import Path
from PIL import Image, ImageOps
from io import BytesIO

THEMES = [
    {
        "name": "passive-aggressive",
        "prompt": "FILLS ENTIRE FRAME. Bright yellow sticky note with passive-aggressive smiley face, the smile too wide and unsettling. Note fills 90% of image. Bold black outlines, yellow fill. White background only at very edges."
    },
    {
        "name": "existential-dread",
        "prompt": "FILLS ENTIRE FRAME. Dramatic scene: tiny orange figure pushing gray boulder up steep black hill into dark void. High contrast, bold colors. Scene fills entire frame edge to edge."
    },
    {
        "name": "ai-hype",
        "prompt": "FILLS ENTIRE FRAME. Purple eldritch tentacled creature wearing cheerful yellow smiley face mask. Creature fills entire image. Bold colors, high contrast. Tentacles reach to all corners."
    },
    {
        "name": "robert-greene",
        "prompt": "FILLS ENTIRE FRAME. Large black chess pawn casting long shadow shaped like a king crown. Pawn fills left side, shadow fills right. Bold black and gray, dramatic lighting effect."
    },
    {
        "name": "fran-lebowitz",
        "prompt": "FILLS ENTIRE FRAME. Close-up of old typewriter with blank white page, overflowing orange ashtray with cigarette butts. Objects fill entire frame. Bold colors, vintage feel."
    },
    {
        "name": "silicon-valley",
        "prompt": "FILLS ENTIRE FRAME. Large compass with needle spinning wildly in circles, motion blur lines. Compass face fills 90% of image. Red and blue accents, bold black outlines."
    },
    {
        "name": "tech-bro",
        "prompt": "FILLS ENTIRE FRAME. Person meditating serenely inside large blue ice cube. Ice cube fills entire image corner to corner. Blue tones, peaceful expression, bold outlines."
    },
    {
        "name": "product-manager",
        "prompt": "FILLS ENTIRE FRAME. Aerial view of crowded parking lot, cars packed tight with tiny yellow lightbulbs on roofs. Cars fill entire image edge to edge. Colorful cars, bold outlines."
    },
    {
        "name": "rto-excuses",
        "prompt": "FILLS ENTIRE FRAME. Large office badge on blue lanyard, badge shows sad face behind gray bars. Badge fills 80% of frame. Bold colors, high contrast."
    },
    {
        "name": "back-from-vacation",
        "prompt": "FILLS ENTIRE FRAME. Person in bright Hawaiian shirt buried under massive pile of white envelopes. Pile fills entire image. Colorful shirt, white envelope avalanche, bold style."
    },
    {
        "name": "iphone-user",
        "prompt": "FILLS ENTIRE FRAME. Large green speech bubble with embarrassed blushing face, sweat drops. Bubble fills 90% of image. Bright green, pink blush, bold black outlines."
    },
    {
        "name": "android-user",
        "prompt": "FILLS ENTIRE FRAME. Smartphone transformed into swiss army knife with colorful tools popping out chaotically in all directions. Phone fills entire frame. Bright colors, bold outlines."
    },
    {
        "name": "marathon-identity",
        "prompt": "FILLS ENTIRE FRAME. Huge white oval 26.2 bumper sticker completely covering a tiny blue car beneath it. Sticker dominates 80% of image. Bold black text, high contrast."
    },
    {
        "name": "the-shining",
        "prompt": "FILLS ENTIRE FRAME. Old typewriter close-up with paper showing same wavy line repeated obsessively in red ink. Typewriter fills entire frame. Black typewriter, white paper, red marks."
    },
    {
        "name": "dark-tower",
        "prompt": "FILLS ENTIRE FRAME. Single red rose growing through cracked gray concrete, dark tower silhouette in orange sunset background. Rose large in foreground filling bottom half."
    },
    {
        "name": "therapy-speak",
        "prompt": "FILLS ENTIRE FRAME. Large circular feelings wheel diagram in pastel colors, multiple segments all pointing to word VALID in center. Wheel fills entire image edge to edge."
    },
    {
        "name": "performative",
        "prompt": "FILLS ENTIRE FRAME. Two large cupped hands held reverently, soft golden glow emanating from empty space between them. Hands fill entire frame. Warm colors, peaceful mood."
    },
    {
        "name": "i-claudius",
        "prompt": "FILLS ENTIRE FRAME. Ornate Roman bowl overflowing with purple figs, one fig has tiny white skull. Bowl fills entire image. Gold bowl, purple figs, Greek key pattern border."
    },
    {
        "name": "sql-server",
        "prompt": "FILLS ENTIRE FRAME. Graph with two lines: flat blue line labeled 1 at bottom, red line shooting up exponentially. Graph fills entire frame. Bold colors, grid background."
    },
    {
        "name": "layoff-speak",
        "prompt": "FILLS ENTIRE FRAME. Brown cardboard box containing laptop, wilted green plant, blue lanyard hanging over edge. Box fills 90% of frame. Sad colors, bold outlines."
    },
    {
        "name": "small-store",
        "prompt": "FILLS ENTIRE FRAME. Bird's eye view of person walking in endless circle inside tiny shop, dotted footprint trail showing the loop. Figure and path fill entire image. Warm colors."
    },
    {
        "name": "ending-phone-call",
        "prompt": "FILLS ENTIRE FRAME. Three large speech bubbles with waving hands inside, each more frantic than last. Bubbles fill entire image top to bottom. Blue bubbles, skin tone hands."
    },
    {
        "name": "week-in-france",
        "prompt": "FILLS ENTIRE FRAME. Smug golden croissant wearing black beret looking down at sad plain beige bagel. Both pastries large, filling the frame. Warm bakery colors, expressive faces."
    },
    {
        "name": "dorinda-medley",
        "prompt": "FILLS ENTIRE FRAME. Mounted fish trophy on wood plaque, fish has worried/nervous expression. Fish fills entire image. Teal fish, brown wood, googly worried eyes."
    },
    {
        "name": "twin-peaks",
        "prompt": "FILLS ENTIRE FRAME. Glass coffee percolator with orange goldfish swimming inside instead of coffee. Percolator fills entire image. Brown coffee tones, orange fish, surreal."
    },
    {
        "name": "breaking-bad",
        "prompt": "FILLS ENTIRE FRAME. Chemistry beaker with bright blue crystals inside, sitting on periodic table square showing Br Ba. Beaker fills 80% of frame. Blue crystals, bold black outlines."
    },
    {
        "name": "better-call-saul",
        "prompt": "FILLS ENTIRE FRAME. Sleazy lawyer in tan suit doing finger guns next to red/yellow inflatable tube man. Both figures fill frame. Bright colors, car dealership energy."
    },
]


def autocrop(img, padding=5):
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


def generate(theme, output_dir):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    output_path = output_dir / f"{theme['name']}.png"
    print(f"Generating: {theme['name']}...")

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
            print(f"  ERROR: {response.status_code} - {response.text[:100]}")
            return False

        data = response.json()
        msg = data.get("choices", [{}])[0].get("message", {})
        if "images" not in msg:
            print(f"  ERROR: No images in response")
            return False

        url = msg["images"][0]["image_url"]["url"]
        _, b64 = url.split(",", 1)
        img = Image.open(BytesIO(base64.b64decode(b64)))
        img = autocrop(img)
        img.save(output_path)
        print(f"  OK: {theme['name']}")
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    output_dir = Path(__file__).parent / "thumbnails"
    output_dir.mkdir(exist_ok=True)

    success = 0
    for theme in THEMES:
        if generate(theme, output_dir):
            success += 1
        time.sleep(1.5)

    print(f"\nDone: {success}/{len(THEMES)} succeeded")


if __name__ == "__main__":
    main()
