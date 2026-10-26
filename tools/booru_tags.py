"""Danbooru / Gelbooru tag prompts for the lookbook characters.

Tags come from the local Danbooru tag list used by ComfyUI tag complete.
Gelbooru uses the same character spellings.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

TAG_FILE = Path(
    r"C:\Users\Danie\Documents\ComfyUI\custom_nodes\comfy-ex-tagcomplete\tags\danbooru.csv"
)

# English series title -> Danbooru copyright tag, when the English words are not the tag.
SERIES_ALIAS = {
    "Sailor Moon": "bishoujo_senshi_sailor_moon",
    "Attack on Titan": "shingeki_no_kyojin",
    "Demon Slayer": "kimetsu_no_yaiba",
    "My Hero Academia": "boku_no_hero_academia",
    "Spirited Away": "sen_to_chihiro_no_kamikakushi",
    "Howl's Moving Castle": "howl_no_ugoku_shiro",
    "Princess Mononoke": "mononoke_hime",
    "Kiki's Delivery Service": "majo_no_takkyuubin",
    "Nausicaa of the Valley of the Wind": "kaze_no_tani_no_nausicaa",
    "Castle in the Sky": "tenkuu_no_shiro_laputa",
    "Your Name": "kimi_no_na_wa.",
    "Weathering With You": "tenki_no_ko",
    "Frieren": "sousou_no_frieren",
    "Re:Zero": "re:zero_kara_hajimeru_isekai_seikatsu",
    "KonoSuba": "kono_subarashii_sekai_ni_shukufuku_wo!",
    "That Time I Got Reincarnated as a Slime": "tensei_shitara_slime_datta_ken",
    "Kaguya-sama: Love Is War": "kaguya-sama_wa_kokurasetai_~tensai-tachi_no_renai_zunousen~",
    "Rascal Does Not Dream of Bunny Girl Senpai": "seishun_buta_yarou_wa_bunny_girl_senpai_no_yume_wo_minai",
    "Bocchi the Rock": "bocchi_the_rock!",
    "Puella Magi Madoka Magica": "mahou_shoujo_madoka_magica",
    "Gurren Lagann": "tengen_toppa_gurren_lagann",
    "One Punch Man": "one-punch_man",
    "JoJo's Bizarre Adventure": "jojo_no_kimyou_na_bouken",
    "Naruto": "naruto_(series)",
    "The Witcher": "the_witcher_(series)",
    "Super Mario": "mario_(series)",
    "Mass Effect": "mass_effect_(series)",
    "Metal Gear": "metal_gear_(series)",
    "NieR": "nier_(series)",
    "NieR: Automata": "nier:automata",
    "Honkai: Star Rail": "honkai:_star_rail",
    "Cyberpunk: Edgerunners": "cyberpunk_edgerunners",
    "Avatar: The Last Airbender": "avatar:_the_last_airbender",
    "The Legend of Korra": "avatar:_the_legend_of_korra",
    "DC": "dc_comics",
    "The Powerpuff Girls": "powerpuff_girls",
    "Hey Arnold": "hey_arnold!",
    "American Dad": "american_dad!",
    "Bob's Burgers": "bob's_burgers",
    "Who Framed Roger Rabbit": "who_framed_roger_rabbit",
    "Assassin's Creed Chronicles: China": "assassin's_creed_chronicles:_china",
    "Tomb Raider King": "tomb_raider_king",
    "Darkstalkers": "vampire_(game)",
    "The King of Fighters": "the_king_of_fighters",
    "Horizon": "horizon_(series)",
    "Halo": "halo_(series)",
    "Diablo": "diablo_(series)",
    "StarCraft": "starcraft_(series)",
    "Portal": "portal_(series)",
    "Half-Life": "half-life",
    "Mirror's Edge": "mirror's_edge",
    "Xenoblade Chronicles": "xenoblade_chronicles_(series)",
    "Fire Emblem": "fire_emblem",
    "Kid Icarus": "kid_icarus",
    "Soulcalibur": "soulcalibur",
    "Mortal Kombat": "mortal_kombat_(series)",
    "Street Fighter": "street_fighter",
    "Resident Evil Village": "resident_evil_village",
    "Metal Gear Solid V": "metal_gear_solid_v:_the_phantom_pain",
    "Final Fantasy XVI": "final_fantasy_xvi",
    "Final Fantasy XV": "final_fantasy_xv",
    "Final Fantasy XIII": "final_fantasy_xiii",
    "Final Fantasy XII": "final_fantasy_xii",
    "Final Fantasy X": "final_fantasy_x",
    "Final Fantasy IX": "final_fantasy_ix",
    "Final Fantasy VIII": "final_fantasy_viii",
    "Final Fantasy VII": "final_fantasy_vii",
    "Final Fantasy VI": "final_fantasy_vi",
    "Pokemon": "pokemon",
    "Overwatch": "overwatch_(game)",
    "Stellar Blade": "stellar_blade",
    "Wuthering Waves": "wuthering_waves",
    "Zenless Zone Zero": "zenless_zone_zero",
    "Solo Leveling": "solo_leveling",
    "High School DxD": "high_school_dxd",
    "Dandadan": "dandadan",
    "Lycoris Recoil": "lycoris_recoil",
    "Toradora": "toradora!",
    "Fruits Basket": "fruits_basket",
    "Cardcaptor Sakura": "cardcaptor_sakura",
    "Kill la Kill": "kill_la_kill",
    "Fairy Tail": "fairy_tail",
    "Ghost in the Shell": "ghost_in_the_shell",
    "Cowboy Bebop": "cowboy_bebop",
    "Death Note": "death_note",
    "Steins;Gate": "steins;gate",
    "Sword Art Online": "sword_art_online",
    "Violet Evergarden": "violet_evergarden",
    "Fullmetal Alchemist": "fullmetal_alchemist",
    "Neon Genesis Evangelion": "neon_genesis_evangelion",
    "Code Geass": "code_geass",
    "Dragon Ball": "dragon_ball",
    "One Piece": "one_piece",
    "Bleach": "bleach",
    "Jujutsu Kaisen": "jujutsu_kaisen",
    "Chainsaw Man": "chainsaw_man",
    "Spy x Family": "spy_x_family",
    "Genshin Impact": "genshin_impact",
    "League of Legends": "league_of_legends",
    "The Legend of Zelda": "the_legend_of_zelda",
    "Star Wars": "star_wars",
    "Looney Tunes": "looney_tunes",
    "Teenage Mutant Ninja Turtles": "teenage_mutant_ninja_turtles",
    "Tomb Raider": "tomb_raider",
    "Hazbin Hotel": "hazbin_hotel",
    "Helluva Boss": "helluva_boss",
    "Steven Universe": "steven_universe",
    "Adventure Time": "adventure_time",
    "Gravity Falls": "gravity_falls",
    "The Owl House": "the_owl_house",
    "Amphibia": "amphibia",
    "Rick and Morty": "rick_and_morty",
    "The Simpsons": "the_simpsons",
    "Family Guy": "family_guy",
    "Futurama": "futurama",
    "Scooby-Doo": "scooby-doo",
    "Kim Possible": "kim_possible",
    "Totally Spies": "totally_spies!",
    "Betty Boop": "betty_boop",
    "Daria": "daria_(series)",
    "Archer": "archer_(series)",
    "Bayonetta": "bayonetta_(series)",
    "Metroid": "metroid",
    "Tekken": "tekken",
    "Uncharted": "uncharted_(series)",
    "Warcraft": "warcraft",
    "Persona 3": "persona_3",
    "Persona 4": "persona_4",
    "Persona 5": "persona_5",
    "Resident Evil": "resident_evil",
    "Cyberpunk 2077": "cyberpunk_2077",
    "Marvel": "marvel",
    "Disney": "disney",
    "Pixar": "pixar",
    "Overlord": "overlord_(maruyama)",
}

SERIES_SHORT = {
    "sword_art_online": ["sao"],
    "final_fantasy_vii": ["ff7", "ffvii"],
    "final_fantasy_viii": ["ff8"],
    "final_fantasy_ix": ["ff9"],
    "final_fantasy_x": ["ff10"],
    "final_fantasy_xii": ["ff12"],
    "final_fantasy_xiii": ["ff13"],
    "final_fantasy_xv": ["ff15"],
    "final_fantasy_xvi": ["ff16"],
    "boku_no_hero_academia": ["bnha", "mha"],
    "kimetsu_no_yaiba": ["kny"],
    "shingeki_no_kyojin": ["snk"],
    "spy_x_family": ["spy_x_family"],
    "tensei_shitara_slime_datta_ken": ["tensei_shitara_slime_datta_ken", "tensura"],
    "jujutsu_kaisen": ["jjk"],
    "genshin_impact": ["genshin"],
    "honkai:_star_rail": ["hsr", "star_rail"],
    "zenless_zone_zero": ["zzz"],
    "neon_genesis_evangelion": ["evangelion"],
    "code_geass": ["geass"],
    "re:zero_kara_hajimeru_isekai_seikatsu": ["re_zero", "rezero"],
}

QUALITY = (
    "(masterpiece, best quality, good quality, score_9, score_8), "
    "(soft anime, gentle shading, illustrated), gorgeous face, detailed eyes, sharp focus"
)
FRAMING = "1girl, solo, looking_at_viewer, upper_body, simple_background"
# Canonical Danbooru tag when the display name does not match the tag or its aliases.
CHARACTER_ALIAS = {
    ("Anya Forger", "Spy x Family"): "anya_(spy_x_family)",
    ("Soi Fon", "Bleach"): "sui-feng",
    ("Mt. Lady", "My Hero Academia"): "takeyama_yu",
    ("Mulan", "Disney"): "fa_mulan_(disney)",
    ("Toph Beifong", "Avatar: The Last Airbender"): "toph_bei_fong",
    ("Marceline", "Adventure Time"): "marceline_abadeer",
    ("Lightning", "Final Fantasy XIII"): "lightning_farron",
    ("Invisible Woman", "Marvel"): "sue_storm",
    ("Zatanna", "DC"): "zatanna_zatara",
    ("Garnet Til Alexandros", "Final Fantasy IX"): "garnet_til_alexandros_xvii",
    ("Vanille", "Final Fantasy XIII"): "oerba_dia_vanille",
    ("Leia Organa", "Star Wars"): "princess_leia",
    ("Blossom", "The Powerpuff Girls"): "blossom_(ppg)",
    ("Bubbles", "The Powerpuff Girls"): "bubbles_(ppg)",
    ("Buttercup", "The Powerpuff Girls"): "buttercup_(ppg)",
}

BOORU_NEGATIVE = (
    "lowres, bad quality, worst quality, bad anatomy, extra fingers, extra limbs, extra arms, "
    "extra legs, missing fingers, fused fingers, watermark, text, logo, signature, blurry, "
    "multiple girls, 2girls, 3girls, nsfw, nude, naked, nipples, pussy, lingerie, underwear, "
    "cleavage, photorealistic, realistic, 3d, sketch, monochrome"
)

_CACHE = None


def loose(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def fold(text: str) -> str:
    text = text.lower().replace("’", "'").replace("–", "-").replace("—", "-")
    text = text.replace("oh", "o").replace("ou", "o").replace("oo", "o").replace("uu", "u")
    text = text.replace("'", "")
    return text


def name_forms(name: str) -> set[str]:
    cleaned = name.lower().strip().replace("’", "'").replace("–", "-").replace("—", "-")
    spaced = re.sub(r"\s+", "_", cleaned).strip("_")
    forms = {
        spaced,
        spaced.replace("-", "_"),
        spaced.replace("'", ""),
        spaced.replace(".", ""),
        spaced.replace("-", "_").replace("'", "").replace(".", ""),
    }
    parts = [part for part in re.split(r"[_\s]+", spaced.replace("-", "_")) if part]
    if len(parts) >= 2:
        forms.add("_".join(parts))
        forms.add(parts[-1] + "_" + "_".join(parts[:-1]))
        forms.add("_".join(reversed(parts)))
    if "." in cleaned:
        forms.add(cleaned.replace(" ", ""))
    return {form.strip("_") for form in forms if form}


def split_tag(tag: str) -> tuple[str, str]:
    match = re.match(r"^(.*)_\((.*)\)$", tag)
    if match:
        return match.group(1), match.group(2)
    return tag, ""


def load_tags():
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    characters = []
    by_base: dict[str, list] = {}
    copyrights: dict[str, int] = {}
    loose_copyright: dict[str, list[str]] = {}
    with TAG_FILE.open(encoding="utf-8", newline="") as handle:
        for row in csv.reader(handle):
            if len(row) < 3 or row[1] not in {"3", "4"}:
                continue
            tag = row[0]
            count = int(row[2] or 0)
            aliases = []
            if len(row) > 3 and row[3]:
                aliases = [part.strip() for part in row[3].split(",") if part.strip()]
            if row[1] == "3":
                copyrights[tag] = count
                loose_copyright.setdefault(loose(tag), []).append(tag)
                continue
            base, paren = split_tag(tag)
            item = (tag, count, base, paren)
            characters.append(item)
            keys = {tag, base, fold(tag), fold(base), *aliases}
            keys.update(fold(alias) for alias in aliases)
            for source in {base, *aliases}:
                parts = [part for part in source.split("_") if part and not part.startswith("(")]
                if len(parts) >= 3:
                    keys.add("_".join(parts[:2]))
                    keys.add("_".join(parts[-2:]))
                    keys.add(fold("_".join(parts[:2])))
                    keys.add(fold("_".join(parts[-2:])))
            for key in keys:
                if key:
                    by_base.setdefault(key, []).append(item)
    _CACHE = (characters, by_base, copyrights, loose_copyright)
    return _CACHE


def copyright_tag(series: str, copyrights: dict[str, int], loose_copyright: dict[str, list[str]]) -> str:
    alias = SERIES_ALIAS.get(series, "")
    if alias and alias in copyrights:
        return alias
    forms = name_forms(series)
    for form in forms:
        if form in copyrights:
            return form
    loose_hits = []
    for form in forms:
        loose_hits.extend(loose_copyright.get(loose(form), []))
    if len(set(loose_hits)) == 1:
        return loose_hits[0]
    series_tokens = {token for token in re.split(r"[^a-z0-9]+", series.lower()) if len(token) > 2}
    best_tag = ""
    best_score = 0
    for tag in copyrights:
        tokens = {token for token in re.split(r"[^a-z0-9]+", tag.lower()) if len(token) > 1}
        if not series_tokens or series_tokens != tokens:
            continue
        score = len(series_tokens) * 10
        if score > best_score or (score == best_score and copyrights[tag] > copyrights.get(best_tag, 0)):
            best_score = score
            best_tag = tag
    return best_tag


def character_tag(name: str, series: str, series_tag: str, by_base: dict[str, list]) -> tuple[str, int]:
    forced = CHARACTER_ALIAS.get((name, series))
    if forced and forced in by_base:
        item = by_base[forced][0]
        return item[0], int(item[1])
    forms = name_forms(name)
    forms.update(fold(form) for form in list(forms))
    partials = set()
    for form in list(forms):
        parts = [part for part in form.split("_") if part]
        if len(parts) >= 2:
            partials.update({parts[0], parts[-1], fold(parts[0]), fold(parts[-1])})
        elif parts:
            partials.add(parts[0])
    series_forms = name_forms(series)
    for short in SERIES_SHORT.get(series_tag, []):
        series_forms.add(short)
    if series_tag:
        series_forms.add(series_tag)
        series_forms.add(split_tag(series_tag)[0])
    seen = set()
    best = ("", -1, -1)
    for form in forms:
        for item in by_base.get(form, []):
            tag, count, base, paren = item
            if tag in seen:
                continue
            seen.add(tag)
            score = 100
            if form in {tag, base, fold(tag), fold(base)}:
                score += 20
            if tag in forms:
                score += 25
            overlap = series_overlap(paren, series_forms)
            if overlap:
                score += 40 + overlap * 10
            elif not paren and (base in forms or fold(base) in forms):
                score += 15
            elif paren and not overlap:
                score -= 50
            if len(base) < 4 and not overlap:
                score -= 40
            score += min(count, 20000) / 20000 * 8
            if score > best[1] or (score == best[1] and count > best[2]):
                best = (tag, score, count)
    for form in partials:
        if len(form) < 4:
            continue
        for item in by_base.get(form, []):
            tag, count, base, paren = item
            if tag in seen:
                continue
            overlap = series_overlap(paren, series_forms)
            if not overlap:
                continue
            seen.add(tag)
            score = 110 + overlap * 10 + min(count, 20000) / 20000 * 8
            if score > best[1] or (score == best[1] and count > best[2]):
                best = (tag, score, count)
    if best[1] < 90:
        if series in {"Disney", "Pixar", "Marvel", "DC"}:
            dominant = dominant_partial(partials, by_base)
            if dominant:
                return dominant
        return "", 0
    tag, count = best[0], int(best[2])
    base, paren = split_tag(tag)
    if paren:
        for item in by_base.get(base, []):
            if item[0] == base and item[1] > count:
                return item[0], int(item[1])
    return tag, count


def series_overlap(paren: str, series_forms: set[str]) -> int:
    if not paren:
        return 0
    paren_text = paren.lower().replace("_", " ").replace(":", " ")
    overlap = 0
    seen = set()
    for token in re.split(r"[^a-z0-9]+", " ".join(series_forms)):
        if len(token) > 1 and token not in seen and token in paren_text:
            seen.add(token)
            overlap += 1
    return overlap


def dominant_partial(partials: set[str], by_base: dict[str, list]) -> tuple[str, int]:
    best = ("", 0, 0)
    for form in partials:
        if len(form) < 4:
            continue
        ranked = []
        seen = set()
        for item in by_base.get(form, []):
            tag, count, base, _paren = item
            if base != form and fold(base) != form:
                continue
            if tag in seen:
                continue
            seen.add(tag)
            ranked.append(item)
        if not ranked:
            continue
        ranked.sort(key=lambda item: item[1], reverse=True)
        top = ranked[0]
        second = ranked[1][1] if len(ranked) > 1 else 0
        if top[1] < 400 or top[1] < second * 4:
            continue
        if top[1] > best[1]:
            best = (top[0], top[1], second)
    if not best[0]:
        return ()
    return best[0], int(best[1])


def booru_prompt(name: str, series: str) -> tuple[str, str, str]:
    _, by_base, copyrights, loose_copyright = load_tags()
    series_tag = copyright_tag(series, copyrights, loose_copyright)
    chosen, count = character_tag(name, series, series_tag, by_base)
    tags = [QUALITY, FRAMING]
    if chosen:
        tags.append(chosen)
    else:
        tags.append(name.lower().strip().replace(" ", "_").replace("’", "'"))
    if series_tag and series_tag not in tags[-1]:
        tags.append(series_tag)
    positive = ", ".join(tags)
    return positive, BOORU_NEGATIVE, chosen or "fallback"


def report(rows: list[dict]) -> None:
    _, by_base, copyrights, loose_copyright = load_tags()
    missed_series = []
    weak = []
    for row in rows:
        series_tag = copyright_tag(row["series"], copyrights, loose_copyright)
        chosen, count = character_tag(row["name"], row["series"], series_tag, by_base)
        if row["series"] not in {item[0] for item in missed_series} and not series_tag:
            missed_series.append((row["series"],))
        if not chosen:
            weak.append((row["name"], row["series"], series_tag, "MISS"))
        elif count < 30:
            weak.append((row["name"], row["series"], chosen, count))
    print(f"series_miss={len({row['series'] for row in rows if not copyright_tag(row['series'], copyrights, loose_copyright)})}")
    seen = set()
    for row in rows:
        if row["series"] in seen:
            continue
        tag = copyright_tag(row["series"], copyrights, loose_copyright)
        if not tag:
            print("SERIES", row["series"])
            seen.add(row["series"])
    matched = len(rows) - sum(1 for item in weak if item[-1] == "MISS")
    print(f"matched={matched} weak_or_miss={len(weak)}")
    for item in weak:
        print("CHAR", " | ".join(str(part) for part in item))
