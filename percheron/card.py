class Card:
    def __init__(self, description):
        self.descriptions = [description]

    def add_description(self, description):
        match = self._find_matching_description(description)
        if match:
            match.update(description)
        else:
            self.descriptions.append(description)
            return True
        return False

    def _find_matching_description(self, description):
        for desc in self.descriptions:
            if _descriptions_match(desc, description):
                return desc
        return False

    def value(self, key):
        values = self.values(key)
        if len(values) == 0:
            return None
        return values[0]

    def values(self, key):
        result = []
        for desc in self.descriptions:
            if key in desc:
                result.append(desc[key])
        return result

    def has_value(self, key):
        for desc in self.descriptions:
            if key in desc:
                return True
        return False

    def name(self):
        return self.value("name")

    def set_code(self):
        return self.value("setCode")

    def number(self):
        return self.value("number")

    def deck_spec(self):
        return f"{self.name()} ({self.set_code()}) {self.number()}"

    def assign(self, key, value):
        for desc in self.descriptions:
            desc[key] = value

    def assign_from_dict(self, value_dict):
        for key, value in value_dict.items():
            try:
                converted_value = float(value)
            except ValueError:
                converted_value = value
            self.assign(key, converted_value)

    def clear(self, key):
        for desc in self.descriptions:
            if key in desc:
                desc.pop(key)

    def print_by_name(self, stream):
        name = self.name()
        score = self.score()
        draft_value = self.draft_value()
        rarity = self.value("rarity")
        count = self.count()
        stream.write(f"{name} {score} {draft_value} ({rarity}) {count}\n")
        stream.flush()

    def print_by_score(self, stream):
        name = self.name()
        score = self.score()
        draft_value = self.draft_value()
        rarity = self.value("rarity")
        count = self.count()
        alsa = self.value("ALSA")
        gihwr = self.value("GIHWR")
        stream.write(f"{score} {draft_value} {alsa} {gihwr} {name} ({rarity}) {count}\n")
        stream.flush()

    def types(self):
        types = set()
        for versions in self.values("types"):
            for some_type in versions:
                types.add(some_type)
        return types

    def score(self):
        if self.has_value("score"):
            return self.value("score")
        return 0

    def draft_value(self):
        if self.has_value("value"):
            return self.value("value")
        if self.has_value("inferred_value"):
            return round(self.value("inferred_value"), 2)
        return "No value"

    def float_draft_value(self):
        value = self.draft_value()
        if value == "No value":
            return 0
        return value

    def draft_value_status(self):
        if self.has_value("value"):
            return "known"
        return "inferred"

    def count(self):
        if self.has_value("count"):
            return self.value("count")
        return 0

    def sort_per_client(self):
        return [self._process_colors(),
                self._mana_cost(),
                self.name()]

    def _mana_cost(self):
        if self.has_value("manaCost") and "X" in self.value("manaCost"):
            return 200
        return self.value("convertedManaCost")

    def _process_colors(self):
        if "Land" in self.types():
            true_colors = self.value("colorIdentity")
        else:
            true_colors = self.value("colors")
        order = color_order(true_colors)
        if self.value("supertypes") == ["Basic"]: # Basic Lands
            order = 100
        return order

COLOR_MAP = [
    ["W"],
    ["U"],
    ["B"],
    ["R"],
    ["G"],
    ["U", "W"], # Azorius
    ["B", "W"], # Orzhov
    ["B", "U"], # Dimir
    ["R", "U"], # Izzet
    ["B", "R"], # Rakdos
    ["B", "G"], # Golgari
    ["G", "R"], # Gruul
    ["R", "W"], # Boros
    ["G", "W"], # Selesnya
    ["G", "U"], # Simic
    ["B", "U", "W"], # Esper
    ["B", "R", "U"], # Grixis
    ["B", "G", "R"], # Jund
    ["G", "R", "W"], # Naya
    ["G", "U", "W"], # Bant
    ["B", "R", "W"], # Mardu
    ["G", "R", "U"], # Temur
    ["B", "G", "W"], # Abzan
    ["R", "U", "W"], # Jeskai
    ["B", "G", "U"], # Sultai
    ["B", "R", "U", "W"], # No Green
    ["B", "G", "U", "W"], # No Red
    ["G", "R", "U", "W"], # No Black
    ["B", "G", "R", "W"], # No Blue
    ["B", "G", "R", "U"], # No White
    ["B", "G", "R", "U", "W"],
    []
]

def color_order(colors):
    colors.sort()
    return COLOR_MAP.index(colors)

def _descriptions_match(old_desc, new_desc):
    for key, value in new_desc.items():
        if key in old_desc and old_desc[key] != value:
            return False
    return True
