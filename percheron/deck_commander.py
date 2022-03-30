import json
import re
from percheron.deck import Deck
from percheron.commander import Commander
from percheron.utils import load_json_file
from percheron.deck_reporter import DeckReporter

class DeckCommander(Commander):
    HELP = """
decklist - List all available decks in current deck.json
write <name> - Write deck to <name>.
read <name> - Read deck from <name>.

name <deck-name> - Set the current deck name
copy <deck-name> - Add cards in current deck to <deck-name>
! - Empty current deck
status - List cards whose total count is less than the number in current deck
cards - List current deck in arena format
cost - Estimated 

deck, Deck - Edit the main card list of the deck
sideboard, Sideboard, sb - Edit the sideboard card list of the deck
[#] <card-spec> - Add # of given card to current card list. Default is 1.
-[#] <card-spec> - Remove # of given card from current card list. Default is 1.
"""
    def __init__(self, mode, library, depth=1):
        super().__init__(mode, library, depth)
        self.decks = {}
        self.current_name = None
        self.current_deck = None
        self.add_to_sideboard = False

    def help(self):
        super().help()
        self.writeline(self.HELP)

    def process_cmd(self, cmd):
        if cmd == "decklist":
            self._list_decks()
        elif cmd == "cards":
            self._list_cards()
        elif cmd == "status":
            self._deck_status()
        elif cmd.startswith("name "):
            self._find_name(cmd[cmd.index(" ") + 1:])
        elif cmd in ['deck', 'Deck']:
            self.add_to_sideboard = False
        elif cmd in ['sideboard', 'Sideboard', 'sb']:
            self.add_to_sideboard = True
        elif cmd.startswith("write "):
            self._write_decks(cmd[cmd.index(" ") + 1:])
        elif cmd.startswith("read "):
            self._read_decks(cmd[cmd.index(" ") + 1:])
        elif not super().process_cmd(cmd):
            if not self._add_card_cmd(cmd):
                self.writeline(f"Failed to add '{cmd}'")
        # elif cmd.startswith("copy "):
        #     self.writeline(f"{cmd} not yet implemented")
        # elif cmd == "!":
        #     self.writeline(f"{cmd} not yet implemented")
        # elif cmd == "status":
        #     self.writeline(f"{cmd} not yet implemented")

    def _has_current_deck(self):
        if self.current_deck is None:
            self.writeline("Select a deck with the 'name' command")
            return False
        return True

    def _deck_status(self):
        reporter = DeckReporter(self.library)
        for deck in self.decks.values():
            self.writeline(reporter.report(deck))
        self.writeline("Name Report")
        self.writeline(reporter.name_report())
        self.writeline("\nCard Set Report")
        self.writeline(reporter.card_set_report())

    def _write_decks(self, filename):
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump([deck.to_dict() for deck in self.decks.values()
                       if deck.has_cards()],
                      file, indent=4)
        self.writeline(f"Successfully wrote {filename}")

    def _read_decks(self, filename):
        contents = load_json_file(self.io_out, filename)
        if contents:
            if isinstance(contents, list):
                for deck in contents:
                    self._load_deck(deck)
                self.writeline(f"Successfully read {filename}")
            else:
                self.writeline(f"{filename} not a JSON list")
        else:
            self.writeline(f"Unable to read content from {filename}")

    def _load_deck(self, deck):
        if "name" in deck:
            self._find_name(deck["name"])
            if "main" in deck:
                self.add_to_sideboard = False
                for card_spec in deck["main"]:
                    self._add_card_cmd(card_spec)
            if "sideboard" in deck:
                self.add_to_sideboard = True
                for card_spec in deck["sideboard"]:
                    self._add_card_cmd(card_spec)
        else:
            self.writeline("Unable to load unnamed deck")

    def _list_decks(self):
        for name in sorted(self.decks.keys()):
            self.writeline(f"{name} ({self.decks[name].card_count()})")

    def _list_cards(self):
        if self.current_deck:
            self.writeline(self.current_deck.summary())
        else:
            self.writeline("No deck selected")

    def _find_name(self, name):
        self.current_name = name
        self.current_deck = self.decks.get(name, Deck(name))
        self.decks[name] = self.current_deck

    def _add_card_cmd(self, cmd):
        if self._has_current_deck():
            parse = _card_parse(cmd)
            if parse:
                return self._add_card(parse[1], parse[2], parse[4])
        return False

    def _add_card(self, count, name, set_name):
        card = self.library.find_named_card(name, set_name)
        return self.current_deck.add_cards(count, card, self.add_to_sideboard)


def _card_parse(cmd):
    pattern = r"^(-?[-0-9]*) *([^ ][^\(]*)( +\((.+)\) ([0-9]+))?$"
    return re.match(pattern, cmd)
