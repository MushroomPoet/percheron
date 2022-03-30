import json
from percheron.card import Card

KEYS = [
    "colorIdentity",
    "colors",
    "convertedManaCost",
    "faceName",
    "layout",
    "manaCost",
    "name",
    "number",
    "rarity",
    "setCode",
    "subtypes",
    "supertypes",
    "type",
    "types",
    "count",
    "score",
    "inferred_value",
    "value"
]

def card_list_to_dict(card_list):
    result = {}
    for description in card_list:
        name = description["name"]
        if name not in result and name.startswith("A-"):
            name = name[2:]
        if name in result:
            result[name].add_description(description)
        else:
            result[name] = Card(description)
    return result

def load_all_cards(stream, filename):
    result = {}
    stream.write(f"Reading {filename}...\n")
    stream.flush()
    data = load_json_file(stream, filename)
    if data:
        for set_name, card_list in data.items():
            result[set_name] = card_list_to_dict(card_list)
    return result

def load_json_file(stream, filename):
    try:
        with open(filename, encoding="UTF-8") as file:
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError:
                stream.write(f"Unable to parse {filename}\n")
    except FileNotFoundError:
        stream.write(f"Unable to open {filename}\n")
    return None

def trimmed_desc_list(cards):
    result = []
    for card in cards.values():
        result.extend(_trimmed_descs(card.descriptions))
    return result

def _trimmed_descs(descs):
    result = []
    for desc in descs:
        new_desc = trimmed_description(desc)
        if new_desc not in result:
            result.append(new_desc)
    return result

def trimmed_description(desc):
    result = {}
    for key in KEYS:
        if key in desc:
            result[key] = desc[key]
    return result
