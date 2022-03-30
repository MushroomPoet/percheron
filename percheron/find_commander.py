from percheron.commander import Commander

class FindCommander(Commander):
    HELP = """
Enter the initial part of words to find a card match.
You'll be told if there are multiple matches.  A '.'
by itself stops ignoring following words.

For example,
  ** percheron:find> ug
  Found "Ugin, the Spirit Dragon" from M21 which costs {8}
  ...
  ** percheron:find> car
  ### Multiple matches ###
  Careless Celebrant
  Carrion Grub
  ** percheron:find> car g
  Found "Carrion Grub" from M21 which costs {3}{B}
  ...
  ** percheron:find> doom
  *** Multiple matches ***
  Doomskar
  Doomskar Oracle
  Doomskar Titan
  ** percheron:find> doom .
  Found "Doomskar" from KHM
"""

    def help(self):
        super().help()
        self.writeline(FindCommander.HELP)

    def process_cmd(self, cmd):
        if not super().process_cmd(cmd):
            self.find_cards(cmd)

    def find_cards(self, cmd):
        self.card_count_dispatch(self.library.find_cards(cmd), cmd)

    def card_count_dispatch(self, cards, cmd):
        card_count = len(cards)
        if card_count == 1:
            self.one_card(cards[0])
        elif card_count > 0:
            self.multiple_cards(cards)
        else:
            self.no_cards(cmd)

    def one_card(self, card):
        self.writeline(f"Found \"{card.name()}\" from {card.value('setCode')}")
        self.writeline(f"with score {card.value('score')}")
        self.writeline(f"with value {card.value('value')}")
        self.writeline(f"with count {card.value('count')}")
        for desc in card.descriptions:
            self.writeline(desc)

    def multiple_cards(self, cards):
        self.writeline("\n    *** Multiple matches ***")
        names = []
        for card in cards:
            names.append(card.name())
        for name in sorted(names):
            self.writeline(name)
        self.writeline("\n")

    def no_cards(self, cmd):
        self.writeline(f"\n    Could not find match for '{cmd}'\n")
