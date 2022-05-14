import json
import re
import sys
from percheron.utils import load_all_cards
from percheron.utils import trimmed_desc_list
from percheron.set_loader import SetLoader

class Library:
    def __init__(self):
        self.filename = "percheron.json"
        self.cards = {}
        self.card_set = ""
        self.card_sets = {}
        self.io_out = sys.stdout

    def writeline(self, line):
        self.io_out.write(str(line) + "\n")
        self.io_out.flush()

    def change_output_stream(self, stream):
        self.io_out = stream

    def sorted_cards(self):
        result = self.card_list()
        result.sort(key = lambda card: card.score())
        return result

    def update_inferred_values(self):
        value = 5.0
        need_values = []
        for card in self.sorted_cards():
            if card.has_value("value"):
                low_value = card.float_draft_value()
                _infer_values(value, low_value, need_values)
                need_values = []
                value = low_value
            else:
                if card.score() != 0:
                    need_values.append(card)
        _infer_values(value, value - 1, need_values)

    def card_list(self):
        if not self.cards:
            self.load_cards()
        result = []
        for card in self.cards.values():
            result.append(card)
        return result

    def find_card_set(self, set_code):
        self.load_card_sets()
        return self.card_sets.get(set_code.strip().upper(), {})

    def rarity_counts(self, set_code, rarity):
        cards = self.find_card_set(set_code)
        if cards:
            counts = [card.count() for card in cards.values()
                      if card.value("rarity") == rarity]
            return (sum(counts), (4 * len(counts)))
        return None

    def find_named_card(self, name, set_name=None):
        cards = self.find_cards(name, set_name)
        if len(cards) == 1:
            return cards[0]
        if len(cards) == 0:
            self.writeline(f"No match for {name}")
        else:
            self.writeline(f"'{name}' is ambigous.\nOptions are:")
            for card in cards:
                self.writeline(f"{card.name()} ({card.value('setCode')}) {card.value('number')}")
            self.writeline("")
        return False

    def find_cards(self, name, set_name=None):
        self.load_card_sets()
        cards = []
        default_set = (set_name or self.card_set).strip()
        if default_set:
            cards = self.find_cards_in_set(name, default_set)
        if not cards:
            cards = self.search_for_named_card(name)
        return cards

    def find_cards_in_set(self, spec, set_name):
        self.load_card_sets()
        if set_name and set_name not in self.card_sets:
            self.writeline(f"Unknown setCode, {set_name}")
        result = []
        search_strings = spec.split(" ") # "k", "g", "o", "d"
        if set_name in self.card_sets:
            for name, card in self.card_sets[set_name].items():
                if _match(iter(search_strings), name):
                    result.append(card)
        return result

    def search_for_named_card(self, name):
        result = []
        for set_name in self.card_sets:
            result.extend(self.find_cards_in_set(name, set_name))
        return result

    def load_card_sets(self):
        if not self.card_sets:
            self.writeline(f"Loading from {self.filename}")
            card_sets = load_all_cards(self.io_out, self.filename)
            if card_sets:
                self.card_sets = card_sets

    def load_cards(self):
        self.load_card_sets()
        if self.card_set == "":
            self.writeline("Card set not specified")
            return
        if self.card_set in self.card_sets:
            self.cards = self.card_sets[self.card_set]
        else:
            self.writeline(f"{self.card_set} is not a known card set")

    def update_arena_card_sets(self, filename):
        self.load_card_sets()
        loader = SetLoader(self.io_out, filename)
        loader.update_card_sets(self.card_sets)

    def change_filename(self, filename):
        if filename:
            self.writeline(f"Changing filename from {self.filename} " +
                           f"to {filename}")
            self.filename = filename

    def write_card_sets(self):
        all_sets = {}
        self.load_card_sets()
        for card_set, cards in self.card_sets.items():
            if cards:
                all_sets[card_set] = trimmed_desc_list(cards)
        with open(self.filename, "w", encoding="UTF-8") as file:
            file.write(json.dumps(all_sets, indent=4))
        self.writeline(f"Wrote {len(self.card_sets)} card sets " +
                       f"to {self.filename}")
        return True

    def change_set(self, card_sets):
        self.load_card_sets()
        loaded_sets = self.card_sets.keys()
        self.cards = {}
        self.card_set = ""
        for card_set in card_sets:
            clean_set = card_set.strip().upper()
            if clean_set in loaded_sets:
                self.card_set = clean_set
        if self.card_set != "":
            self.writeline(f"Search card set: {self.card_set}")
        else:
            self.writeline("Available card sets are:")
            for card_set in loaded_sets:
                self.writeline(card_set)


def _infer_values(high, low, cards):
    count = len(cards)
    increment = (high - low)/(count + 1)
    current = high
    for card in cards:
        current -= increment
        card.assign("inferred_value", current)

def _match(search_iter, name):
    name_iter = iter(name.split(" ")) # "Klothys,", "God", "of", "Destiny"
    name_str = next(name_iter)
    done = False
    for search_str in search_iter:
        if search_str == ".":
            return done
        if done:
            return False
        try:
            if re.match(search_str, name_str, re.IGNORECASE):
                try:
                    name_str = next(name_iter)
                except StopIteration:
                    done = True
            else:
                return False
        except re.error:
            return False
    return True
