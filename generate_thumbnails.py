"""Generate thumbnail images for each spinner theme."""
import httpx
import base64
import os
import time
from pathlib import Path

THEMES = [
    {
        "name": "passive-aggressive",
        "prompt": "Minimalist sketch. A yellow sticky note with a smiley face drawn on it, but the smile is slightly too wide, unsettling. Clean white background. Simple line art style. No text."
    },
    {
        "name": "existential-dread",
        "prompt": "Minimalist sketch. A tiny stick figure pushing a boulder up a hill, with the hill continuing infinitely upward into darkness. Simple line art, white background. No text."
    },
    {
        "name": "ai-hype",
        "prompt": "Minimalist sketch. An eldritch tentacled creature (lovecraftian) wearing a friendly theatre mask with a simple smiley face. Contrast between horror and cheerfulness. Line art, white background. No text."
    },
    {
        "name": "robert-greene",
        "prompt": "Minimalist sketch. A chess pawn casting a shadow that shows a king piece. Power and deception theme. Simple line art, white background. No text."
    },
    {
        "name": "fran-lebowitz",
        "prompt": "Minimalist sketch. A typewriter with a completely blank page, an overflowing ashtray beside it, and a clock showing decades passing. Writer's block personified. Line art, white background. No text."
    },
    {
        "name": "silicon-valley",
        "prompt": "Minimalist sketch. A compass needle spinning wildly in circles, unable to find direction. Pivot metaphor. Simple line art, white background. No text."
    },
    {
        "name": "tech-bro",
        "prompt": "Minimalist sketch. A person meditating inside an ice cube, looking serene but frozen. Cold plunge optimization culture. Simple line art, white background. No text."
    },
    {
        "name": "product-manager",
        "prompt": "Minimalist sketch. A literal parking lot full of cars, each car labeled with a tiny idea lightbulb. Ideas parked and forgotten. Simple line art, white background. No text."
    },
    {
        "name": "rto-excuses",
        "prompt": "Minimalist sketch. An office badge on a lanyard, with the badge showing a tiny sad face behind turnstile bars. Badge swipe prison. Simple line art, white background. No text."
    },
    {
        "name": "back-from-vacation",
        "prompt": "Minimalist sketch. A person in beach attire (sunglasses, lei) being crushed under a massive towering pile of envelopes. Inbox mountain. Simple line art, white background. No text."
    },
    {
        "name": "iphone-user",
        "prompt": "Minimalist sketch. A speech bubble that is an ugly green color, looking ashamed with cartoon sweat drops. The green bubble of shame. Simple line art, white background. No text."
    },
    {
        "name": "android-user",
        "prompt": "Minimalist sketch. A Swiss army knife but it's a smartphone with way too many tools/attachments popping out chaotically. Feature overload. Simple line art, white background. No text."
    },
    {
        "name": "marathon-identity",
        "prompt": "Minimalist sketch. An oval bumper sticker showing '26.2' but the sticker is enormous, taking over the entire car. Identity consumed by marathon. Simple line art, white background. No text."
    },
    {
        "name": "the-shining",
        "prompt": "Minimalist sketch. An old typewriter with a single page coming out, the page filled with the same wavy line repeated over and over in neat rows. Obsessive repetition. Simple line art, white background. No text."
    },
    {
        "name": "dark-tower",
        "prompt": "Minimalist sketch. A single perfect rose growing through cracked concrete in an empty urban lot, with a dark tower silhouette in the distant background. Simple line art, white background. No text."
    },
    {
        "name": "therapy-speak",
        "prompt": "Minimalist sketch. A circular feelings wheel diagram with many segments, but all segments somehow point to 'valid'. Validation wheel. Simple line art, white background. No text except the word 'valid' repeated in segments."
    },
    {
        "name": "performative",
        "prompt": "Minimalist sketch. Two empty cupped hands holding absolutely nothing, but with reverent pose as if holding something precious. Holding space literally. Simple line art, white background. No text."
    },
    {
        "name": "i-claudius",
        "prompt": "Minimalist sketch. A decorative Roman bowl of figs, with one fig having a tiny skull symbol on it. Poisoned figs. Simple line art, white background. No text."
    },
    {
        "name": "sql-server",
        "prompt": "Minimalist sketch. Two diverging lines on a graph - one labeled with '1' staying flat near bottom, another shooting up exponentially. Estimated vs actual rows. Simple line art, white background. Minimal text just the number 1."
    },
    {
        "name": "layoff-speak",
        "prompt": "Minimalist sketch. A cardboard box with a laptop inside it, a small wilted plant, and a lanyard hanging over the edge. The layoff box. Simple line art, white background. No text."
    },
    {
        "name": "small-store",
        "prompt": "Minimalist sketch. Dotted footprint path showing someone walking in the same small circle/loop pattern repeatedly inside a tiny shop outline. Trapped browsing. Simple line art, white background. No text."
    },
    {
        "name": "ending-phone-call",
        "prompt": "Minimalist sketch. Three speech bubbles in a row, each containing a small wave hand emoji, getting progressively more frantic. The triple bye. Simple line art, white background. No text."
    },
    {
        "name": "week-in-france",
        "prompt": "Minimalist sketch. A croissant wearing a tiny beret and looking smugly at a plain American bagel. Pastry superiority. Simple line art, white background. No text."
    },
    {
        "name": "dorinda-medley",
        "prompt": "Minimalist sketch. A decorative fish (like a fish room decoration) mounted on a wall plaque, but the fish looks nervous/worried. The fish room assignment. Simple line art, white background. No text."
    },
    {
        "name": "twin-peaks",
        "prompt": "Minimalist sketch. A coffee percolator with a fish swimming inside it instead of coffee. Surreal Lynchian absurdity. Simple line art, white background. No text."
    },
]


def generate_thumbnail(theme: dict, output_dir: Path) -> bool:
    """Generate a single thumbnail."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set")
        return False

    output_path = output_dir / f"{theme['name']}.png"

    # Skip if already exists
    if output_path.exists():
        print(f"SKIP: {theme['name']} (already exists)")
        return True

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
                "image_config": {
                    "aspect_ratio": "1:1"
                }
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

        # Extract base64 image
        url = message["images"][0]["image_url"]["url"]
        _, b64 = url.split(",", 1)

        # Save image
        img_data = base64.b64decode(b64)
        with open(output_path, "wb") as f:
            f.write(img_data)

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
        # Rate limiting
        time.sleep(2)

    print(f"\nDone: {success} success, {failed} failed")


if __name__ == "__main__":
    main()
