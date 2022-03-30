import json
import re
from percheron.find_commander import FindCommander

class CountCommander(FindCommander):
    HELP = """
# <card-spec> - Update the count for the given card
report - List counts for all cards in set sorted by rarity, client order
"""

    def __init__(self, mode, library, depth=1):
        super().__init__(mode, library, depth)
        self.counts = {}
        self.count = None

    def help(self):
        super().help()
        self.writeline(self.HELP)

    def process_cmd(self, cmd):
        self.count = None
        if cmd == "report":
            self.report()
            return
        super().process_cmd(cmd)

    # Override method from FindCommander
    def find_cards(self, cmd):
        pattern = r"^(([0-9]*) *)?([^ 0-9][^\(]*)(\((.+)\) ([0-9]+))?$"
        match = re.match(pattern, cmd)
        if match:
            self.writeline(f"Processing {cmd}")
            if match[1]:
                self.count = int(match[1])
            cards = self.library.find_cards(match[3].strip(), match[5])
            self.card_count_dispatch(cards, cmd)

    def report(self):
        result = self.library.card_list()
        result.sort(key = lambda c: c.sort_per_client())
        self._report_by_rarity("common", result)
        self._report_by_rarity("uncommon", result)
        self._report_by_rarity("rare", result)
        self._report_by_rarity("mythic", result)

    def _report_by_rarity(self, rarity, cards):
        self.writeline(f"\nReport for {rarity} cards")
        count = 0
        for card in cards:
            if rarity in card.values("rarity"):
                count += 1
                self.writeline(f"{count}\t{card.name()}\t{card.count()}")

    def one_card(self, card):
        if self.count is None:
            super().one_card(card)
        else:
            self.writeline(f"\"{card.name()}\" given the count {self.count}")
            card.assign("count", self.count)
            self.counts[card.name()] = self.count

    def exit_mode(self):
        self.writeline(json.dumps(self.counts, indent=4))
