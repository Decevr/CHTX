"""Build the CHTX catalog from the clothed lookbook.

Writes phone-sized JPEGs and catalog.js. Does not touch the dropdowns.
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from booru_tags import booru_prompt  # noqa: E402

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
WWW = ROOT / "app" / "src" / "main" / "assets" / "www"
RES = ROOT / "app" / "src" / "main" / "res"
LOOKBOOK = Path(r"D:\ComfyUIPIC\anima\lookbook")
PAGE = LOOKBOOK / "index.html"
CHARACTERS = Path(
    r"C:\Users\Danie\Documents\ComfyUI\custom_nodes\ComfyUI-AnimaCharacterCombos\characters.py"
)
ADDED = Path(r"C:\Users\Danie\AppData\Local\Temp\add_lookbook_series.py")
MARKS = Path(
    r"C:\Users\Danie\.grok\sessions\C%3A%5CUsers%5CDanie\01a174ae-54da-7c22-a986-5c300b0c7a6f\images"
)

LABELS = {
    "anime": "Anime",
    "marvel": "Marvel",
    "dc": "DC",
    "disney": "Disney",
    "pixar": "Pixar",
    "pokemon": "Pokemon",
    "video_games": "Video Games",
    "cartoons": "Cartoons",
}

LOOKBOOK_NEG = (
    "lowres, bad quality, worst quality, bad anatomy, extra fingers, extra limbs, extra arms, "
    "extra legs, fused fingers, missing hands, watermark, text, logo, signature, jpeg artifacts, "
    "different character, wrong series, generic face, "
    "nude, naked, nsfw, explicit, nipples, pussy, lingerie, suggestive, porn, blurry, blurry eyes, "
    "extra people, two heads, extra face, child, loli, underage, teen, young girl, little girl, schoolgirl"
)

SETTINGS = {
    "workflow": "Anima text to image",
    "model": r"Anima\pearlySapphireThe_v10.safetensors",
    "clip": r"FluX\qwen_3_06b_base.safetensors",
    "vae": r"Qwen_Vea\hdrVAEAnimaKrea2QWEN_bf16.safetensors",
    "size": "768x1024",
    "steps": 20,
    "cfg": 5,
    "sampler": "er_sde",
    "scheduler": "simple",
    "note": (
        "Paste this with your own prompt in ComfyUI or Forge. "
        "The line names the character. Your prompt sets the scene. "
        "Danbooru and Gelbooru use the same character tags."
    ),
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def character_line(name: str, series: str) -> str:
    return f"{name} from {series}"


def parse_page() -> list[dict]:
    text = PAGE.read_text(encoding="utf-8")
    parts = re.split(r'<section id="([^"]+)">', text)
    rows = []
    card_re = re.compile(
        r'<img src="([^"]+)" alt="([^"]*)"><h3>([^<]*)</h3><p>([^<]*)</p>'
    )
    for index in range(1, len(parts), 2):
        category = parts[index]
        block = parts[index + 1]
        for match in card_re.finditer(block):
            src, alt, name, series = match.groups()
            src = src.split("?", 1)[0]
            rows.append({
                "category": category,
                "src": src,
                "name": html.unescape(name or alt),
                "series": html.unescape(series),
            })
    return rows


def save_jpeg(src: Path, dest: Path, width: int, quality: int):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as image:
        image = image.convert("RGB")
        image.thumbnail((width, width * 2), Image.Resampling.LANCZOS)
        image.save(dest, "JPEG", quality=quality, optimize=True)


def install_marks():
    squares = []
    wides = []
    for path in MARKS.glob("*.jpg"):
        with Image.open(path) as image:
            width, height = image.size
        if abs(width - height) < 40:
            squares.append(path)
        elif width > height:
            wides.append(path)
    if not squares or not wides:
        raise SystemExit(f"missing icon or banner in {MARKS}")
    icon = squares[-1]
    banner = wides[-1]
    save_jpeg(banner, WWW / "banner.jpg", 1600, 84)
    sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    for folder, side in sizes.items():
        dest = RES / folder / "ic_launcher.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(icon) as image:
            image = image.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
            image.save(dest, "PNG")
        round_dest = RES / folder / "ic_launcher_round.png"
        with Image.open(icon) as image:
            image = image.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
            image.save(round_dest, "PNG")


def main():
    characters = load_module("characters", CHARACTERS)
    adult = set(characters.ADULT)
    custom = {}
    if ADDED.exists():
        added = load_module("added", ADDED)
        for item in added.ROWS:
            negative = added.CHILD_NEG if item.get("child") else added.NEG
            custom[(item["name"], item["series"])] = (added.positive(item), negative)

    rows = parse_page()
    print(f"cards={len(rows)} custom={len(custom)}", flush=True)
    if len(rows) < 700:
        raise SystemExit("lookbook parse missed most cards")

    characters_out = []
    for row in rows:
        positive = character_line(row["name"], row["series"])
        negative = LOOKBOOK_NEG
        booru_positive, booru_negative, _tag = booru_prompt(row["name"], row["series"])
        src = LOOKBOOK / row["src"]
        if not src.is_file():
            raise SystemExit(f"missing image {src}")
        rel = f"images/{Path(row['src']).with_suffix('.jpg').as_posix()}"
        dest = WWW / rel
        if not dest.is_file() or dest.stat().st_size < 8000:
            save_jpeg(src, dest, 720, 78)
        characters_out.append({
            "name": row["name"],
            "series": row["series"],
            "category": row["category"],
            "image": rel,
            "positive": positive,
            "negative": negative,
            "booru": booru_positive,
            "booru_negative": booru_negative,
        })

    counts = {}
    for row in characters_out:
        counts[row["category"]] = counts.get(row["category"], 0) + 1
    categories = [
        {"id": key, "label": LABELS.get(key, key), "count": counts[key]}
        for key in counts
    ]
    catalog = {
        "title": "CHTX",
        "count": len(characters_out),
        "settings": SETTINGS,
        "categories": categories,
        "characters": characters_out,
    }
    payload = "window.CATALOG = " + json.dumps(catalog, ensure_ascii=False) + ";\n"
    (WWW / "catalog.js").write_text(payload, encoding="utf-8")
    if not (RES / "mipmap-xxxhdpi" / "ic_launcher.png").is_file():
        install_marks()
    image_bytes = sum(path.stat().st_size for path in (WWW / "images").rglob("*.jpg"))
    print(f"wrote {len(characters_out)} images_mb={image_bytes / 1048576:.1f}", flush=True)


if __name__ == "__main__":
    main()
