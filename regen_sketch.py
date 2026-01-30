"""Regenerate ALL thumbnails - SKETCH STYLE with Joe's color palette."""
import httpx
import base64
import os
import time
from pathlib import Path
from PIL import Image, ImageOps
from io import BytesIO

# Style: Hand-drawn sketch, diagonal hatching, fills frame
# Colors: Orange #FF6B35, Blue #4A90E2, Green #7FB069, Lines #2D3142, Background white

STYLE = """Hand-drawn sketch-note style. FILLS ENTIRE FRAME edge to edge.
Diagonal hatching for shading (NOT solid fills).
Colors: orange #FF6B35, blue #4A90E2, green #7FB069, dark gray lines #2D3142.
Pure white background. Clean minimalist. No drop shadows. No realistic rendering."""

THEMES = [
    ("passive-aggressive", "Large yellow sticky note with unsettling too-wide smiley face. Note fills 90% of frame. Orange hatching accents."),
    ("existential-dread", "Tiny figure pushing boulder up steep hill into darkness above. Blue and orange hatching. Dramatic, fills frame."),
    ("ai-hype", "Eldritch tentacled creature wearing cheerful smiley face mask. Purple-blue hatching on tentacles. Creature fills entire frame."),
    ("robert-greene", "Large chess pawn casting shadow shaped like king crown. Pawn fills left half, dramatic shadow fills right. Bold contrast."),
    ("fran-lebowitz", "Typewriter with blank page, overflowing ashtray with cigarettes. Objects large, fill frame. Orange hatching on ashtray."),
    ("silicon-valley", "Large compass with needle spinning wildly, motion lines. Compass fills 90% of frame. Blue and orange accents."),
    ("tech-bro", "Person meditating serenely inside ice cube. Ice cube fills entire frame corner to corner. Blue hatching for ice."),
    ("product-manager", "Aerial view of parking lot packed with cars, tiny lightbulbs on roofs. Cars fill entire frame. Colorful hatching."),
    ("rto-excuses", "Large office badge on lanyard, badge shows sad face behind bars. Badge fills 80% of frame. Blue lanyard."),
    ("back-from-vacation", "Person in Hawaiian shirt buried under pile of envelopes. Fills frame. Orange shirt, white envelopes."),
    ("iphone-user", "Large green speech bubble with embarrassed blushing face, sweat drops. Bubble fills 90% of frame. Green #7FB069."),
    ("android-user", "Smartphone as swiss army knife with tools popping out chaotically. Phone fills entire frame. Colorful tool accents."),
    ("marathon-identity", "Huge oval 26.2 bumper sticker covering tiny car beneath. Sticker dominates 80% of image. Bold outline."),
    ("the-shining", "Typewriter close-up with paper showing same line repeated obsessively. Typewriter fills frame. Orange accents."),
    ("dark-tower", "Single rose growing through cracked concrete, dark tower silhouette in background. Rose large, fills bottom half. Orange rose."),
    ("therapy-speak", "Large circular feelings wheel, segments in orange/blue/green, word VALID in center. Wheel fills entire frame."),
    ("performative", "Two large cupped hands held reverently, soft glow from empty space between. Hands fill frame. Orange glow."),
    ("i-claudius", "Ornate Roman bowl overflowing with figs, one fig has tiny skull. Bowl fills entire frame. Green figs, orange bowl accents."),
    ("sql-server", "Graph with flat line labeled 1 at bottom, another line shooting up exponentially. Graph fills frame. Blue/orange lines."),
    ("layoff-speak", "Cardboard box with laptop, wilted plant, lanyard hanging over edge. Box fills 90% of frame. Sad green plant."),
    ("small-store", "Bird's eye view of person walking in circle inside tiny shop, dotted footprint trail. Fills entire frame. Orange path."),
    ("ending-phone-call", "Three speech bubbles with waving hands, each more frantic. Bubbles fill frame top to bottom. Blue bubbles."),
    ("week-in-france", "Smug croissant wearing beret looking down at sad bagel. Both large, fill frame. Orange croissant, blue accents."),
    ("dorinda-medley", "Mounted fish trophy on plaque, fish has worried expression. Fish fills entire frame. Blue-green fish."),
    ("twin-peaks", "Coffee percolator with fish swimming inside instead of coffee. Percolator fills frame. Orange fish, blue-gray tones."),
    ("breaking-bad", "Chemistry beaker with blue crystals inside, on periodic table square Br Ba. Beaker fills 80% of frame. Blue #4A90E2 crystals."),
    ("better-call-saul", "Sleazy lawyer doing finger guns next to waving inflatable tube man. Both fill frame. Orange tube man."),
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


def generate(name, desc, output_dir):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    output_path = output_dir / f"{name}.png"
    prompt = f"{STYLE}\n\nSubject: {desc}"
    print(f"Generating: {name}...")

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
                "messages": [{"role": "user", "content": prompt}],
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
        print(f"  OK")
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    output_dir = Path(__file__).parent / "thumbnails"
    output_dir.mkdir(exist_ok=True)

    success = 0
    for name, desc in THEMES:
        if generate(name, desc, output_dir):
            success += 1
        time.sleep(1.5)

    print(f"\nDone: {success}/{len(THEMES)}")


if __name__ == "__main__":
    main()
