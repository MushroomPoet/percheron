from percheron.commander import Commander
from percheron.count_commander import CountCommander
from percheron.deck_commander import DeckCommander
from percheron.draft_commander import DraftCommander
from percheron.find_commander import FindCommander
from percheron.score_commander import ScoreCommander
from percheron.sealed_commander import SealedCommander
from percheron.value_commander import ValueCommander

class RootCommander(Commander):
    HELP = """
report - Report on all cards in current set

find - Find and print details on cards in the current set
score - Record the draft score (order) for cards in the current set
value - Record the draft value (0-5) for cards in the current set
count - Record counts of cards in the current set
draft - Enter draft helper mode for the current set
sealed - Enter sealed helper mode for the current set
deck - Load and assess decks against the current collection
update - Update the current set from AllPrintings.json
filename - Set the filename for the storage file.  Default 'percheron.json'.
write - Write out any new data to the storage file
"""

    def help(self):
        super().help()
        self.writeline(RootCommander.HELP)

    SUBCOMMANDERS = {
        "find": FindCommander,
        "score": ScoreCommander,
        "value": ValueCommander,
        "count": CountCommander,
        "draft": DraftCommander,
        "sealed": SealedCommander,
        "deck": DeckCommander
    }

    def process_cmd(self, cmd):
        if not super().process_cmd(cmd):
            commander = self.SUBCOMMANDERS.get(cmd)
            if commander:
                commander(self.mode + f":{cmd}",
                          self.library,
                          self.depth + 1).run(self.io_in, self.io_out)
            elif cmd == "report":
                self.report()
            elif cmd.startswith("rarity "):
                self.rarity_report(cmd[cmd.index(" ") + 1:])
            else:
                self.writeline(f"Unrecognized command: {cmd}")

    def report(self):
        for card in self.library.sorted_cards():
            card.print_by_score(self.io_out)

    def rarity_report(self, set_codes):
        for set_code in set_codes.split(" "):
            mythic_counts = self.library.rarity_counts(set_code, "mythic")
            if not mythic_counts:
                continue
            mythics = f"Mythics {mythic_counts[0]} out of {mythic_counts[1]}"
            rare_counts = self.library.rarity_counts(set_code, "rare")
            rares = f"Rares {rare_counts[0]} out of {rare_counts[1]}"
            self.writeline(f"{set_code}: {mythics}, {rares}")
