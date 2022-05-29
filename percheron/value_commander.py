import json
from percheron.find_commander import FindCommander

class ValueCommander(FindCommander):
    HELP = """
#[.#] <card-spec> - Update the value for the given card
clear_values - Clear all values in the current set
report - Print the value report for the current set
"""

    def __init__(self, mode, library, depth=1):
        super().__init__(mode, library, depth)
        self.values = {}
        self.value = None

    def help(self):
        super().help()
        self.writeline(self.HELP)

    def process_cmd(self, cmd):
        self.value = None
        if cmd == "report":
            self.report()
            return
        elif cmd == "clear_values":
            self.clear_values()
            return
        try:
            first_space = cmd.index(" ")
            self.value = float(cmd[:first_space])
            self.find_cards(cmd[first_space + 1:])
        except ValueError:
            super().process_cmd(cmd)

    def clear_values(self):
        for card in self.library.sorted_cards():
            card.clear("value")
            card.clear("inferred_value")
        self.values = {}
        self.value = None

    def report(self):
        previous_value = 5
        needed = []
        for card in self.library.sorted_cards():
            card.print_by_score(self.io_out)
            if _value_needed(card, previous_value):
                needed.append(card)
            previous_value = card.draft_value()
        if self.library.cards != {}:
            self._needed_report(needed)

    def one_card(self, card):
        if self.value is not None:
            self.writeline(f"\"{card.name()}\" given the value {self.value}")
            self.writeline(f"Previous value was {card.draft_value()} " +
                           f"which was {card.draft_value_status()}")
            card.assign("value", self.value)
            self.library.update_inferred_values()
            self.values[card.name()] = self.value
        else:
            card.print_by_score(self.io_out)

    def exit_mode(self):
        self.writeline(json.dumps(self.values, indent=4))

    def _needed_report(self, cards):
        self.writeline("\nNeeded cards")
        cards.sort(key=lambda c: c.name())
        by_rarity = {}
        for card in cards:
            rarity = card.value("rarity")
            cards_at_level = by_rarity.get(rarity, [])
            cards_at_level.append(card)
            by_rarity[rarity] = cards_at_level
        min_value = min([self._print_rarity_set("mythic", by_rarity),
                         self._print_rarity_set("rare", by_rarity),
                         self._print_rarity_set("uncommon", by_rarity),
                         self._print_rarity_set("common", by_rarity)])
        self.writeline(f"\nMinimum unknown value: {min_value}")

    def _print_rarity_set(self, rarity, by_rarity):
        min_value = 5
        if rarity in by_rarity:
            self.writeline(f"\n{rarity} cards")
            for card in by_rarity[rarity]:
                if card.draft_value() < min_value:
                    min_value = card.draft_value()
                card.print_by_name(self.io_out)
        else:
            self.writeline(f"\nNo {rarity} cards without values")
        return min_value


def _value_needed(card, previous_value):
    return ((not(card.has_value("value")) or
             card.float_draft_value() == 0) and
            (card.has_value("inferred_value") and
             card.value("inferred_value") != previous_value))
