from percheron.deck_builder import DeckBuilder
from percheron.find_commander import FindCommander

class SealedCommander(FindCommander):
    HELP = """
! - Reset the pool of cards
<card-spec> - Add given card to current pool
pool - List all cards in the current pool
export - Print current pool in more standard format

compare - Print comparison summary of all color pairs
build <colors> - Build a sealed deck for the given colors from current pool
"""
    def __init__(self, mode, library, depth=1):
        super().__init__(mode, library, depth)
        self.card_pool = []

    def help(self):
        super().help()
        self.writeline(self.HELP)

    def process_cmd(self, cmd):
        if cmd == "!":
            self.card_pool = []
        elif cmd == "pool":
            self.print_pool()
        elif cmd == "export":
            self.export_pool()
        elif cmd.startswith("build "):
            DeckBuilder(self.card_pool, cmd.split(" "), self.io_out).report()
        elif cmd == "compare":
            self.compare_decks()
        else:
            super().process_cmd(cmd)

    def compare_decks(self):
        all_colors = ["W", "U", "B", "R", "G"]
        deck_summaries = []
        while all_colors:
            color1 = all_colors.pop()
            for color2 in all_colors:
                deck_summaries.append([
                    DeckBuilder(self.card_pool,
                                [color1, color2],
                                self.io_out).average_value(),
                    color1,
                    color2])
        deck_summaries.sort()
        for value, color1, color2 in deck_summaries:
            self.writeline(f"{color1}, {color2}, {value}")

    def one_card(self, card):
        self.card_pool.append(card)
        card.print_by_name(self.io_out)

    def print_pool(self):
        self.card_pool.sort(key = lambda card: card.score())
        self.writeline("")
        for card in self.card_pool:
            card.print_by_score(self.io_out)

    def export_pool(self):
        self.card_pool.sort(key = lambda card: card.name())
        self.writeline("")
        last = None
        count = 0
        for card in self.card_pool:
            if last is not None and last != card:
                self.writeline(f"{count} {last.name()}")
                count = 0
            count += 1
            last = card
        if last is not None:
            self.writeline(f"{count} {last.name()}")
