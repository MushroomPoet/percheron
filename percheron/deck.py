class Deck:
    def __init__(self, name):
        self.name = name
        self.main = []
        self.sideboard = []

    def has_cards(self):
        return len(self.main) > 0 or len(self.sideboard) > 0

    def to_dict(self):
        return {
            "name": self.name,
            "main": _entry_list_for_json(self.main),
            "sideboard": _entry_list_for_json(self.sideboard)
        }

    def card_count(self):
        return len(self.main) + len(self.sideboard)

    def add_cards(self, count, card, sideboard=False):
        if card:
            if sideboard:
                _add_cards(self.sideboard, count, card)
            else:
                _add_cards(self.main, count, card)
            return True
        return False

    def missing(self):
        result = []
        for entry in self.main:
            count = entry[0] - entry[1].count()
            if count > 0:
                result.append([count, entry[1]])
        return result

    def summary(self):
        result = f"{self.name}\nDeck\n{_card_summary(self.main)}"
        if self.sideboard:
            result += f"\n\nSideboard\n{_card_summary(self.sideboard)}"
        return result

def _entry_list_for_json(entry_list):
    return [_entry_for_json(entry) for entry in entry_list]

def _entry_for_json(entry):
    return f"{entry[0]} {entry[1].deck_spec()}"

def _card_summary(card_list):
    return "\n".join([f"{count} {card.name()}" for count, card in card_list])

def _add_cards(entry_list, count_spec, card):
    count = 1
    for deck_entry in entry_list:
        if card == deck_entry[1]:
            if count_spec == "-":
                count = -deck_entry[0]
            elif count_spec != "":
                count = int(count_spec)
            new_count = deck_entry[0] + count
            if new_count <= 0:
                entry_list.remove(deck_entry)
            else:
                deck_entry[0] = new_count
            return
    if not count_spec.startswith("-"):
        if count_spec != "":
            count = int(count_spec)
        entry_list.append([count, card])
