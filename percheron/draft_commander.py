from percheron.commander import Commander
from percheron.find_commander import FindCommander

class DraftCommander(FindCommander):
    HELP = """
! - Reset the pack of cards
<card-spec> - Add given card to current pack and list pack
"""

    def __init__(self, mode, library, depth=1):
        super().__init__(mode, library, depth)
        self.drafted_cards = []

    def help(self):
        self.writeline(Commander.HELP)
        self.writeline(self.HELP)

    def process_cmd(self, cmd):
        if cmd == "!":
            self.drafted_cards = []
        else:
            super().process_cmd(cmd)

    def one_card(self, card):
        self.drafted_cards.append(card)
        self.write_draft_report()

    def write_draft_report(self):
        self.drafted_cards.sort(key = lambda c: c.score())
        self.writeline("")
        for card in self.drafted_cards:
            card.print_by_score(self.io_out)
