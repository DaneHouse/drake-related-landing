#!/usr/bin/env python3
"""Generate room images using Gemini Nano Banana API"""

import json
import base64
import urllib.request
import urllib.error
import sys
import os

API_KEY = "AIzaSyDsMAAQBZv--CntVxudAYDY9sc11IoFvQ4"
MODEL = "nano-banana-pro-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

PROMPTS = {
    "front": "3D rendered isometric overhead view of a luxury modern mansion entrance at night. Dark moody atmosphere, looking down at a 45-degree angle. Dramatic front door with ambient warm lighting from wall sconces, dark stone pathway with landscape lighting, manicured hedges, a parked matte black luxury SUV in the driveway. Dark walls, warm golden porch lights casting pools of light. High-end architectural visualization style, cinematic lighting, dark shadows, 16:9 composition. No people, no text, no watermarks.",

    "lounge": "3D rendered isometric overhead view looking down at 45 degrees into a luxury modern living room at night. Dark moody atmosphere with warm ambient lamp lighting. Large cream L-shaped sectional sofa with scattered throw pillows and a fur blanket. Black marble coffee table with champagne bottle and glasses, fashion magazines scattered around. Leopard print area rug on dark hardwood floors. Gold pendant lights hanging from ceiling. Tall curtains along floor-to-ceiling windows showing city lights. Rose petals scattered on the floor. Lived-in luxury feel with designer items casually placed. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks.",

    "kitchen": "3D rendered isometric overhead view looking down at 45 degrees into a luxury modern dark kitchen at night. Moody atmosphere with warm under-cabinet LED lighting. Black marble island with gold bar stools, dark cabinetry with brass hardware. Professional espresso machine on counter, wine glasses, a bottle of red wine. Pendant lights with warm amber glow. Dark hardwood floors, subtle backlighting. Takeout containers and a half-eaten meal casually left on the island. Luxury lived-in feel. High-end 3D architectural visualization, cinematic lighting, 16:9 composition. No people, no text, no watermarks.",

    "court": "3D rendered isometric overhead view looking down at 45 degrees at a private indoor basketball court. Dark moody atmosphere with dramatic overhead spotlights creating pools of light on a polished dark wood court floor with white lines. Basketball hoop and backboard visible. A basketball sitting on the court. Scoreboard on the wall. Dark concrete walls, industrial ceiling with exposed beams. A bench with towels and water bottles on the sideline. Sneakers and a gym bag left courtside. High-end 3D architectural visualization, cinematic dramatic lighting, 16:9 composition. No people, no text, no watermarks.",

    "backyard": "3D rendered isometric overhead view looking down at 45 degrees at a luxury rooftop terrace at night. Dark moody atmosphere with warm string lights overhead and a modern fire pit with dancing flames at center. Dark outdoor sectional sofa with cream cushions arranged around the fire pit. City skyline visible in the background at night. Potted plants, a bar cart with liquor bottles and cocktail glasses. Outdoor speakers, blankets draped over furniture. Ambient warm golden lighting, dark atmosphere. High-end 3D architectural visualization, cinematic lighting, 16:9 composition. No people, no text, no watermarks.",

    "closet": "3D rendered isometric overhead view looking down at 45 degrees into a luxury walk-in closet. Dark moody atmosphere with warm recessed LED ceiling lights creating amber glow. Dark walnut wood built-in shelving on both sides displaying designer sneakers, folded hoodies, and accessories. Center island with dark marble top and gold drawer pulls. Clothing racks with designer jackets and streetwear. A few pairs of sneakers casually left on the floor. Sunglasses display case, watches, gold jewelry. Full-length mirror with gold frame. Dark carpet floor. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks.",

    "lab": "3D rendered isometric overhead view looking down at 45 degrees into a dark moody recording studio and production room. Red-tinted warm ambient lighting. Large U-shaped sectional sofa in olive green and burnt orange tones with scattered pillows. Professional mixing console and studio monitors on a desk with multiple screens. Microphone on a boom stand in the center. Cables running across the floor. A keyboard synthesizer, vinyl records leaning against equipment. Gold starburst chandelier hanging from dark ceiling. Basketball casually left on the sofa. A hoodie draped over a studio chair. Dark industrial walls. High-end 3D architectural visualization, cinematic moody red and amber lighting, 16:9 composition. No people, no text, no watermarks."
}

def generate_image(room, prompt):
    payload = json.dumps({
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{URL}?key={API_KEY}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"[{room}] HTTP {e.code}: {body[:500]}")
        return False
    except Exception as e:
        print(f"[{room}] Error: {e}")
        return False

    # Debug: show response structure
    if "candidates" not in data:
        print(f"[{room}] No candidates in response. Keys: {list(data.keys())}")
        if "error" in data:
            print(f"[{room}] Error: {data['error'].get('message', '')}")
        else:
            print(f"[{room}] Response: {json.dumps(data, indent=2)[:1000]}")
        return False

    for part in data["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            img_data = base64.b64decode(part["inlineData"]["data"])
            mime = part["inlineData"].get("mimeType", "image/png")
            ext = "png" if "png" in mime else "jpg" if "jpeg" in mime or "jpg" in mime else "webp"
            filepath = os.path.join(IMAGES_DIR, f"{room}.{ext}")
            with open(filepath, "wb") as f:
                f.write(img_data)
            print(f"[{room}] Saved {filepath} ({len(img_data):,} bytes)")
            return True

    # Check if there's text explaining why no image
    for part in data["candidates"][0]["content"]["parts"]:
        if "text" in part:
            print(f"[{room}] Text response (no image): {part['text'][:300]}")

    print(f"[{room}] No image data found in response")
    return False


if __name__ == "__main__":
    # Generate one at a time or specific room
    rooms = sys.argv[1:] if len(sys.argv) > 1 else list(PROMPTS.keys())

    success = 0
    for room in rooms:
        if room not in PROMPTS:
            print(f"[{room}] Unknown room, skipping")
            continue
        print(f"[{room}] Generating...")
        if generate_image(room, PROMPTS[room]):
            success += 1

    print(f"\nDone: {success}/{len(rooms)} images generated")
