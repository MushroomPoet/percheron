from percheron.utils import load_json_file
from percheron.utils import trimmed_description
from percheron.card import Card

class SetLoader:
    def __init__(self, stream, filename):
        self.filename = filename
        self.stream = stream

    def writeline(self, line):
        self.stream.write(line + "\n")
        self.stream.flush()

    def update_card_sets(self, card_sets):
        all_sets = self._load_sets() # dict setCode -> card descriptions
        if all_sets and isinstance(all_sets, dict):
            for set_code in _arena_set_names(all_sets):
                if set_code not in card_sets:
                    self.writeline(f"Adding new card set, {set_code}")
                old_set = card_sets.get(set_code, {})
                new_set = all_sets[set_code]["cards"]
                card_sets[set_code] = self._update_card_set(old_set, new_set)
                self.writeline(f"Updated {set_code}")
        return True

    def _load_sets(self):
        self.writeline(f"Loading {self.filename}...")
        contents = load_json_file(self.stream, self.filename)
        if contents and isinstance(contents, dict) and "data" in contents:
            return contents["data"]
        self.writeline(f"Cannot find data in {self.filename}")
        return None

    def _update_card_set(self, old_set, new_set):
        # old_set is dict card_name => Card
        # new_set is list of card descriptions
        for desc in new_set:
            name = desc.get("name", "")
            if name not in old_set and name.startswith("A-"):
                name = name[2:]
            if name not in old_set:
                old_set[name] = Card(desc)
                self.writeline(f"New card: {name}")
            else:
                desc_trim = trimmed_description(desc)
                if old_set[name].add_description(desc_trim):
                    self.writeline(f"Added description to: {name}")
        return old_set

def _arena_set_names(all_sets):
    return [key for key, value in all_sets.items()
            if _is_arena_set(value)]

def _is_arena_set(card_dict):
    if not isinstance(card_dict, dict) or "cards" not in card_dict:
        return False
    cards = card_dict["cards"]
    if not isinstance(cards, list) or len(cards) == 0:
        return False
    card = cards[0]
    if not isinstance(card, dict) or "availability" not in card:
        return False
    availability = card["availability"]
    if isinstance(availability, list) and "arena" in availability:
        return True
    return False
