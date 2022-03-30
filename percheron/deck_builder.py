COLORS = {
    "W": "W",
    "WHITE": "W",
    "U": "U",
    "BLUE": "U",
    "B": "B",
    "BLACK": "B",
    "R": "R",
    "RED": "R",
    "G": "G",
    "GREEN": "G"
}

def find_color(color_spec):
    key = color_spec.strip().upper()
    if key in COLORS:
        return COLORS[key]
    return ""

def deck_report(deck, stream):
    total_value = total_deck_value(deck)
    for card in deck:
        card.print_by_score(stream)
    count = len(deck)
    if count == 0:
        stream.write("Empty deck\n")
    else:
        stream.write(f"cards: {count}, average value: {total_value/count}\n")
        curve_report(deck, stream)
        type_report(deck, stream)

def total_deck_value(deck):
    result = 0
    for card in deck:
        result += card.float_draft_value()
    return result

def curve_report(deck, stream):
    curve = {}
    for card in deck:
        cmcs = card.values("convertedManaCost")
        for cmc in cmcs:
            if cmc in curve:
                curve[cmc] += 1
            else:
                curve[cmc] = 1
    print_table("CMC Curve", curve, stream)

def type_report(deck, stream):
    types = {}
    for card in deck:
        for card_type in card.types():
            if card_type in types:
                types[card_type] += 1
            else:
                types[card_type] = 1
    print_table("Type Distribution", types, stream)

def print_table(prefix, table, stream):
    elements = []
    for key in sorted(table.keys()):
        elements.append(f"{key}: {table[key]}")
    stream.write(f"{prefix}:: {', '.join(elements)}\n")


ALL_COLORS = {"W", "U", "B", "R", "G"}

class DeckBuilder:
    def __init__(self, card_pool, colors, io_out):
        card_pool.sort(key = lambda card: card.value("score"))
        self.card_pool = card_pool
        self.colors = colors
        self.io_out = io_out
        self._total_value = 0
        self.cards = []

    def build_deck(self):
        exclude = self.unsupported_colors()
        self.cards = []
        for card in self.card_pool:
            if exclude.intersection(card.value("colorIdentity")) == set():
                self.cards.append(card)

    def unsupported_colors(self):
        listed_colors = set()
        for color_spec in self.colors:
            listed_colors.add(find_color(color_spec))
        return ALL_COLORS - listed_colors

    def report(self):
        self.build_deck()
        deck_report(self.cards[:23], self.io_out)
        self.io_out.write("\nRemaining cards:\n")
        deck_report(self.cards[23:], self.io_out)

    def average_value(self):
        self.build_deck()
        return total_deck_value(self.cards[:23])/23
