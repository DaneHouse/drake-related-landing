#!/usr/bin/env python3
"""Generate ranch-themed room images using Imagen 4.0 Fast"""

import json
import base64
import urllib.request
import urllib.error
import sys
import os

API_KEY = "AIzaSyDsMAAQBZv--CntVxudAYDY9sc11IoFvQ4"
MODEL = "imagen-4.0-fast-generate-001"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict"

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

PROMPTS = {
    "gate": "3D rendered isometric overhead view looking down at 45 degrees at a modern ranch entrance gate at golden hour. Rustic timber and iron gate with large stone pillars on either side. A long dirt driveway stretching into the distance lined with wooden post-and-rail fences. Rolling green hills and distant mountains under a warm golden sunset sky. Mature oak trees flanking the driveway. A matte black Rolls Royce Cullinan SUV parked near the gate. Warm golden hour lighting casting long shadows. Wildflowers along the fence line. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks.",

    "lounge": "3D rendered isometric overhead view looking down at 45 degrees into a modern ranch lodge living room. Open-concept with soaring high ceilings and exposed timber beams. Large stone fireplace with a crackling fire as the centerpiece. Floor-to-ceiling windows showing mountain views at dusk. Deep leather sectional sofa with wool blankets and scattered pillows. A large black and white polka dot area rug inspired by dalmatian spots on wide-plank hardwood floors. Antler chandelier with warm amber bulbs. Whiskey glasses and a bottle on a rustic wood coffee table. Built-in bookshelves. Warm ambient firelight glow throughout. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks.",

    "kitchen": "3D rendered isometric overhead view looking down at 45 degrees into a modern ranch house chef's kitchen. Warm rustic luxury atmosphere. Large butcher block island with copper pendant lights hanging above. Dark green cabinetry with brass hardware. Professional range stove with a cast iron skillet. Open wooden shelving displaying ceramics and spice jars. Herb garden in small pots on the windowsill with golden light streaming in. Copper pots and pans hanging from a ceiling rack. Fresh bread and ingredients laid out on the island. Wide-plank wood floors, subway tile backsplash. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks.",

    "court": "3D rendered isometric overhead view looking down at 45 degrees at a basketball court inside a converted barn with large open barn doors showing a beautiful scenic mountain landscape with golden sunset light streaming in. Exposed timber beam ceiling with industrial pendant lights. Polished hardwood court floor painted in Toronto Raptors red and black theme with a large Raptors claw logo at center court. Basketball hoop and glass backboard with red padding. A red and black basketball sitting on the court. Raptors banner hanging from the rafters. Red LED accent lighting along the walls. A bench with towels and water bottles on the sideline. Sneakers and a gym bag left courtside. High-end 3D architectural visualization, cinematic dramatic lighting, 16:9 composition. No people, no text, no watermarks.",

    "gym": "3D rendered isometric overhead view looking down at 45 degrees into a private gym inside a converted ranch barn. Exposed timber beams and reclaimed wood walls. Heavy iron weight rack with dumbbells and plates. A squat rack and flat bench in the center. Heavy bag hanging from a beam. Rubber mat flooring with chalk dust. Battle ropes coiled on the floor. A speaker playing music on a shelf. Towels draped over equipment. Water bottles and a shaker cup on a wooden bench. Large barn doors open to show scenic ranch landscape and golden light. Raw, gritty, functional gym atmosphere. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks.",

    "backyard": "3D rendered isometric overhead view looking down at 45 degrees at a modern ranch backyard at sunset. Wide open range with rolling green hills extending to distant mountains. A stone fire pit with dancing flames at center surrounded by Adirondack chairs. String lights hanging between wooden posts. A beautiful dalmatian dog sitting proudly in the center foreground of the scene, looking happy and alert with tongue out, well-lit and detailed. Wooden deck extending from the ranch house. Wildflower patches, a horse fence in the distance. Warm golden sunset light with purple sky. Blankets draped over chairs. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks.",

    "closet": "3D rendered isometric overhead view looking down at 45 degrees into a modern ranch walk-in closet and sneaker room. Warm wood-paneled walls with recessed LED lighting. Multiple rows of open shelving displaying an extensive Nike sneaker collection — Air Jordans, Air Force 1s, Dunks, Air Max in various colorways. A glass-front sneaker display case with premium pairs. Clothing rack with Nike Tech Fleece hoodies, designer jackets, and streetwear. A center island with dark wood top. Sneaker cleaning station with brushes and solution. Several pairs of Nikes casually left on the wide-plank wood floor. Warm amber lighting throughout. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks.",

    "lab": "3D rendered isometric overhead view looking down at 45 degrees into a converted barn workspace and tech studio. Exposed timber beams and original barn wood walls. Large industrial desk with dual monitors, mechanical keyboard, and warm desk lamp. Server rack with blinking lights in the corner. Leather office chair. Cables neatly managed. A whiteboard with diagrams and sticky notes. Vintage workbench repurposed as a side table with coffee mug. Edison bulb string lights across the ceiling. Concrete and wood floors. A hoodie draped over the chair. Warm industrial amber lighting. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks.",

    "stable": "3D rendered isometric overhead view looking down at 45 degrees at a wide open ranch pasture at golden hour. Six beautiful horses of different breeds and colors galloping together across a green grass field. A dark brown horse, a cream palomino, a black horse, a golden chestnut, a grey horse, and a reddish-brown horse all running freely in formation. Wooden post-and-rail fences lining the pasture. Rolling hills and mountains in the background under a warm golden sunset sky. Dust kicking up from their hooves. A rustic red barn visible in the far background. Wildflowers and tall grass. High-end 3D architectural visualization, cinematic warm lighting, 16:9 composition. No people, no text, no watermarks."
}


def generate_image(room, prompt):
    payload = json.dumps({
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9"
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

    # Imagen 4.0 returns predictions array
    if "predictions" in data and len(data["predictions"]) > 0:
        img_b64 = data["predictions"][0].get("bytesBase64Encoded")
        if img_b64:
            img_data = base64.b64decode(img_b64)
            mime = data["predictions"][0].get("mimeType", "image/jpeg")
            ext = "png" if "png" in mime else "jpg"
            filepath = os.path.join(IMAGES_DIR, f"{room}.{ext}")
            with open(filepath, "wb") as f:
                f.write(img_data)
            print(f"[{room}] Saved {filepath} ({len(img_data):,} bytes)")
            return True

    print(f"[{room}] Unexpected response: {json.dumps(data, indent=2)[:1000]}")
    return False


if __name__ == "__main__":
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
