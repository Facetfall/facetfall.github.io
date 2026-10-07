"""Facetfall Studios emblem: a cut diamond with shards falling from it.

python brand/make_emblem.py ->
  emblem.svg              vector, transparent (site)
  emblem_512.png          transparent PNG
  emblem_roblox_512.png   on a dark rounded tile (Roblox group icon, 512x512)
  favicon_64.png
"""
import os
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 4  # supersampling for smooth edges

# Geometry on a 512 canvas
T1, T2, T3 = (186, 118), (256, 118), (326, 118)
G1, G2, G3, G4, G5 = (100, 200), (178, 200), (256, 200), (334, 200), (412, 200)
C = (256, 404)
FACETS = [
    # crown
    ([G1, T1, G2], "#9ff3ff"),
    ([T1, T2, G3, G2], "#e6fcff"),
    ([T2, T3, G4, G3], "#7fe4ff"),
    ([T3, G5, G4], "#3fb8f0"),
    # pavilion
    ([G1, G2, C], "#38c8f5"),
    ([G2, G3, C], "#8de6ff"),
    ([G3, G4, C], "#5b6cf2"),
    ([G4, G5, C], "#7a3fe0"),
]
# falling shards (small facets breaking off the lower right)
SHARDS = [
    ([(346, 350), (390, 334), (374, 386)], "#8de6ff"),
    ([(394, 400), (424, 392), (410, 430)], "#7a3fe0"),
    ([(428, 446), (448, 442), (438, 466)], "#9ff3ff"),
]
EDGE = "#0b1630"


def hexrgb(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def draw_gem(size=512):
    s = size / 512 * SS
    img = Image.new("RGBA", (int(512 * s), int(512 * s)), (0, 0, 0, 0))
    # soft glow behind the gem
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    pts = [(x * s, y * s) for x, y in [G1, T1, T3, G5, C]]
    gd.polygon(pts, fill=(90, 200, 255, 150))
    glow = glow.filter(ImageFilter.GaussianBlur(28 * s))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)
    for poly, col in FACETS + SHARDS:
        pts = [(x * s, y * s) for x, y in poly]
        d.polygon(pts, fill=hexrgb(col))
        d.line(pts + [pts[0]], fill=hexrgb(EDGE, 200), width=int(3 * s), joint="curve")
    # sparkle on the table
    cx, cy, r = 222 * s, 150 * s, 26 * s
    d.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
               (cx, cy + r), (cx - r * 0.28, cy + r * 0.28), (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)],
              fill=(255, 255, 255, 255), outline=(40, 90, 160, 255), width=int(2 * s))
    return img.resize((size, size), Image.LANCZOS)


def tile(size=512):
    s = SS
    bg = Image.new("RGBA", (size * s, size * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle([0, 0, size * s - 1, size * s - 1], 110 * s, fill=(14, 18, 34, 255))
    glow = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([60 * s, 20 * s, 452 * s, 412 * s], fill=(60, 80, 200, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(70 * s))
    mask = bg.split()[3]
    bg.alpha_composite(Image.composite(glow, Image.new("RGBA", bg.size, (0, 0, 0, 0)), mask))
    bg = bg.resize((size, size), Image.LANCZOS)
    gem = draw_gem(int(size * 0.86))
    off = (size - gem.width) // 2
    bg.alpha_composite(gem, (off, off + int(size * 0.02)))
    return bg


def svg():
    parts = []
    for poly, col in FACETS + SHARDS:
        pts = " ".join(f"{x},{y}" for x, y in poly)
        parts.append(f'<polygon points="{pts}" fill="{col}" stroke="{EDGE}" stroke-opacity=".8" stroke-width="3" stroke-linejoin="round"/>')
    star = "222,124 229.3,142.7 248,150 229.3,157.3 222,176 214.7,157.3 196,150 214.7,142.7"
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="80 90 370 380">'
        '<defs><filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter></defs>'
        f'<polygon points="{G1[0]},{G1[1]} {T1[0]},{T1[1]} {T3[0]},{T3[1]} {G5[0]},{G5[1]} {C[0]},{C[1]}" fill="#5ac8ff" opacity=".55" filter="url(#g)"/>'
        + "".join(parts)
        + f'<polygon points="{star}" fill="#fff" stroke="#285aa0" stroke-width="2"/></svg>'
    )


if __name__ == "__main__":
    draw_gem(512).save(os.path.join(HERE, "emblem_512.png"))
    tile(512).save(os.path.join(HERE, "emblem_roblox_512.png"))
    tile(64).save(os.path.join(HERE, "favicon_64.png"))
    open(os.path.join(HERE, "emblem.svg"), "w", encoding="utf-8").write(svg())
    print("ok")
