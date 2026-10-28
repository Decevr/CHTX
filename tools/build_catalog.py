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


# Lookbook portraits added after the 744-card page. Jade was already on that page.
EXTRAS = [
    ("anime", "Revy", "Black Lagoon", "anime/revy__black_lagoon.png"),
    ("anime", "Balalaika", "Black Lagoon", "anime/balalaika__black_lagoon.png"),
    ("anime", "Fujiko Mine", "Lupin the Third", "anime/fujiko_mine__lupin_the_third.png"),
    ("anime", "Retsu Unohana", "Bleach", "anime/retsu_unohana__bleach.png"),
    ("anime", "Lisa Lisa", "JoJo's Bizarre Adventure", "anime/lisa_lisa__jojo_s_bizarre_adventure.png"),
    ("anime", "Esdeath", "Akame ga Kill!", "anime/esdeath__akame_ga_kill.png"),
    ("anime", "Nana Osaki", "Nana", "anime/nana_osaki__nana.png"),
    ("anime", "Serie", "Frieren", "anime/serie__frieren.png"),
    ("anime", "Fiona Frost", "Spy x Family", "anime/fiona_frost__spy_x_family.png"),
    ("anime", "Integra Hellsing", "Hellsing", "anime/integra_hellsing__hellsing.png"),
    ("anime", "Roberta", "Black Lagoon", "anime/roberta__black_lagoon.png"),
    ("anime", "Ritsuko Akagi", "Neon Genesis Evangelion", "anime/ritsuko_akagi__neon_genesis_evangelion.png"),
    ("anime", "Naomi Misora", "Death Note", "anime/naomi_misora__death_note.png"),
    ("anime", "Sylvia Sherwood", "Spy x Family", "anime/sylvia_sherwood__spy_x_family.png"),
    ("anime", "Crusch Karsten", "Re:Zero", "anime/crusch_karsten__re_zero.png"),
    ("anime", "Lust", "Fullmetal Alchemist", "anime/lust__fullmetal_alchemist.png"),
    ("anime", "Holo", "Spice and Wolf", "anime/holo__spice_and_wolf.png"),
    ("anime", "Merlin", "The Seven Deadly Sins", "anime/merlin__the_seven_deadly_sins.png"),
    ("anime", "Cornelia li Britannia", "Code Geass", "anime/cornelia_li_britannia__code_geass.png"),
    ("anime", "Utahime Iori", "Jujutsu Kaisen", "anime/utahime_iori__jujutsu_kaisen.png"),
    ("cartoons", "Wilma Flintstone", "The Flintstones", "cartoons/wilma_flintstone__the_flintstones.png"),
    ("cartoons", "Betty Rubble", "The Flintstones", "cartoons/betty_rubble__the_flintstones.png"),
    ("cartoons", "Jane Jetson", "The Jetsons", "cartoons/jane_jetson__the_jetsons.png"),
    ("cartoons", "Peggy Hill", "King of the Hill", "cartoons/peggy_hill__king_of_the_hill.png"),
    ("cartoons", "Morticia Addams", "The Addams Family", "cartoons/morticia_addams__the_addams_family.png"),
    ("cartoons", "Aeon Flux", "Aeon Flux", "cartoons/aeon_flux__aeon_flux.png"),
    ("cartoons", "Teela", "He-Man and the Masters of the Universe", "cartoons/teela__he_man_and_the_masters_of_the_universe.png"),
    ("cartoons", "Evil-Lyn", "He-Man and the Masters of the Universe", "cartoons/evil_lyn__he_man_and_the_masters_of_the_universe.png"),
    ("cartoons", "Cheetara", "ThunderCats", "cartoons/cheetara__thundercats.png"),
    ("cartoons", "Princess Bean", "Disenchantment", "cartoons/princess_bean__disenchantment.png"),
    ("video_games", "Skarlet", "Mortal Kombat", "video_games/skarlet__mortal_kombat.png"),
    ("video_games", "Rose", "Street Fighter", "video_games/rose__street_fighter.png"),
    ("video_games", "Blue Mary", "The King of Fighters", "video_games/blue_mary__the_king_of_fighters.png"),
    ("video_games", "Hilde", "Soulcalibur", "video_games/hilde__soulcalibur.png"),
    ("video_games", "Philippa Eilhart", "The Witcher", "video_games/philippa_eilhart__the_witcher.png"),
    ("video_games", "Maria", "Silent Hill 2", "video_games/maria__silent_hill_2.png"),
    ("video_games", "Tess", "The Last of Us", "video_games/tess__the_last_of_us.png"),
    ("video_games", "Talanah Khane Padish", "Horizon Zero Dawn", "video_games/talanah_khane_padish__horizon_zero_dawn.png"),
    ("video_games", "Samantha Nishimura", "Tomb Raider", "video_games/samantha_nishimura__tomb_raider.png"),
    ("disney", "The Evil Queen", "Disney", "disney/the_evil_queen__disney.png"),
    ("disney", "Ursula", "Disney", "disney/ursula__disney.png"),
    ("disney", "Lady Tremaine", "Disney", "disney/lady_tremaine__disney.png"),
    ("disney", "Fairy Godmother", "Disney", "disney/fairy_godmother__disney.png"),
    ("disney", "Queen of Hearts", "Disney", "disney/queen_of_hearts__disney.png"),
    ("disney", "Madam Mim", "Disney", "disney/madam_mim__disney.png"),
    ("disney", "Helga Sinclair", "Disney", "disney/helga_sinclair__disney.png"),
    ("disney", "Captain Amelia", "Disney", "disney/captain_amelia__disney.png"),
    ("disney", "Judy Hopps", "Disney", "disney/judy_hopps__disney.png"),
    ("disney", "Elizabeth Swann", "Disney", "disney/elizabeth_swann__disney.png"),
    ("pixar", "Mirage", "Pixar", "pixar/mirage__pixar.png"),
    ("pixar", "Evelyn Deavor", "Pixar", "pixar/evelyn_deavor__pixar.png"),
    ("pixar", "Jill Andersen", "Pixar", "pixar/jill_andersen__pixar.png"),
    ("pixar", "Queen Elinor", "Pixar", "pixar/queen_elinor__pixar.png"),
    ("pixar", "Mama Imelda", "Pixar", "pixar/mama_imelda__pixar.png"),
    ("pixar", "Laurel Lightfoot", "Pixar", "pixar/laurel_lightfoot__pixar.png"),
    ("pixar", "Dorothea Williams", "Pixar", "pixar/dorothea_williams__pixar.png"),
    ("pixar", "Celia Mae", "Pixar", "pixar/celia_mae__pixar.png"),
    ("pixar", "Sally Carrera", "Pixar", "pixar/sally_carrera__pixar.png"),
    ("pixar", "Cinder Lumen", "Pixar", "pixar/cinder_lumen__pixar.png"),
    ("marvel", "Mantis", "Marvel", "marvel/mantis__marvel.png"),
    ("marvel", "Frigga", "Marvel", "marvel/frigga__marvel.png"),
    ("marvel", "Ramonda", "Marvel", "marvel/ramonda__marvel.png"),
    ("marvel", "Thena", "Marvel", "marvel/thena__marvel.png"),
    ("marvel", "Amora", "Marvel", "marvel/amora__marvel.png"),
    ("marvel", "Clea", "Marvel", "marvel/clea__marvel.png"),
    ("marvel", "Misty Knight", "Marvel", "marvel/misty_knight__marvel.png"),
    ("marvel", "Echo", "Marvel", "marvel/echo__marvel.png"),
    ("marvel", "Viper", "Marvel", "marvel/viper__marvel.png"),
    ("dc", "Nubia", "DC", "dc/nubia__dc.png"),
    ("dc", "Atlanna", "DC", "dc/atlanna__dc.png"),
    ("dc", "Andrea Beaumont", "DC", "dc/andrea_beaumont__dc.png"),
    ("dc", "Madame Xanadu", "DC", "dc/madame_xanadu__dc.png"),
    ("dc", "Isis", "DC", "dc/isis__dc.png"),
    ("dc", "Jo Mullein", "DC", "dc/jo_mullein__dc.png"),
    ("dc", "Cheshire", "DC", "dc/cheshire__dc.png"),
    ("dc", "Silver Banshee", "DC", "dc/silver_banshee__dc.png"),
    ("pokemon", "Zinnia", "Pokemon", "pokemon/zinnia__pokemon.png"),
    ("pokemon", "Professor Burnet", "Pokemon", "pokemon/professor_burnet__pokemon.png"),
    ("pokemon", "Ariana", "Pokemon", "pokemon/ariana__pokemon.png"),
]


def with_extras(rows: list[dict]) -> list[dict]:
    have = {row["src"] for row in rows}
    grouped: dict[str, list[dict]] = {}
    order: list[str] = []
    for row in rows:
        if row["category"] not in grouped:
            grouped[row["category"]] = []
            order.append(row["category"])
        grouped[row["category"]].append(row)
    added = 0
    for category, name, series, src in EXTRAS:
        if src in have:
            continue
        if category not in grouped:
            grouped[category] = []
            order.append(category)
        grouped[category].append({
            "category": category,
            "src": src,
            "name": name,
            "series": series,
        })
        added += 1
    print(f"extras={added}", flush=True)
    merged = []
    for category in order:
        merged.extend(grouped[category])
    return merged


def main():
    characters = load_module("characters", CHARACTERS)
    adult = set(characters.ADULT)
    custom = {}
    if ADDED.exists():
        added = load_module("added", ADDED)
        for item in added.ROWS:
            negative = added.CHILD_NEG if item.get("child") else added.NEG
            custom[(item["name"], item["series"])] = (added.positive(item), negative)

    rows = with_extras(parse_page())
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
