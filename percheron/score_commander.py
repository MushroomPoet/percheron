import json
from percheron.find_commander import FindCommander

class ScoreCommander(FindCommander):
    HELP = """
<card-spec> - Give matching card the current score (in prompt)
# <card-spec> - Explicitly set the score for the given card

Current score is the last score applied + 1.
"""

    def __init__(self, mode, library, depth=1):
        super().__init__(mode, library, depth)
        self.score = None
        self.scores = {}
        self.current_score = 1

    def help(self):
        super().help()
        self.writeline(self.HELP)

    def prompt(self, _suffix=""):
        super().prompt(f"({self.current_score})")

    def process_cmd(self, cmd):
        self.score = None
        try:
            first_space = cmd.index(" ")
            self.score = int(cmd[:first_space])
            self.find_cards(cmd[first_space + 1:])
        except ValueError:
            super().process_cmd(cmd)

    def one_card(self, card):
        if not self.score:
            self.score = self.current_score
        self.current_score = self.score + 1
        self.writeline(f"\"{card.name()}\" given the score {self.score}")
        if card.value("score") != self.score:
            card.assign("score", self.score)
            card.clear("value")
            self.library.update_inferred_values()
        self.scores[card.name()] = self.score

    def exit_mode(self):
        self.writeline(json.dumps(self.scores, indent=4))
