# 33 Inqisitor Captain: 9 decks want 3, 3 decks want 2

class Counter:
    def __init__(self):
        self.total = 0
        self.counts = {}

    def tally(self, count):
        self.total += count
        self.counts[count] = 1 + self.counts.get(count, 0)
        return self

    def report(self):
        return ", ".join([
            f"{value} decks want {key}" for key, value
            in sorted(self.counts.items(), key=lambda item: -item[0])
        ])


class CardCounter:
    def __init__(self):
        self.total = 0
        self.counters = {} # name -> Counter

    def tally(self, card, count):
        self.total += count
        name = card.name()
        self.counters[name] = self.counters.get(name, Counter()).tally(count)

    def report(self):
        return "".join([
            f"{counter.total} {name}: {counter.report()}\n"
            for name, counter
            in sorted(self.counters.items(), key=lambda item: -item[1].total)])


# 125 Y22: 45 distict mythics, 12 distinct rares (0.12345)

class SetCardCounter:
    def __init__(self, set_code, library):
        self.set_code = set_code
        self.total = 0
        self.mythics = {}
        self.rares = {}
        self.mythic_counts = library.rarity_counts(set_code, "mythic")
        self.rare_counts = library.rarity_counts(set_code, "rare")

    def tally(self, card, count):
        self.total += count
        name = card.name()
        rarity = card.value("rarity")
        if rarity == "mythic":
            self.mythics[name] = max(count, self.mythics.get(name, 0))
        elif rarity == "rare":
            self.rares[name] = max(count, self.rares.get(name, 0))
        return self

    def mythic_desired(self):
        return sum(self.mythics.values())

    def rare_desired(self):
        return sum(self.rares.values())

    def chance_per_pack(self):
        m_chance = 1 / 7.4 # True for current standard except AFR which is 1/7
        m_prob = _prob_of_some(self.mythic_counts, self.mythic_desired())
        r_chance = 1 - m_chance
        r_prob = _prob_of_some(self.rare_counts, self.rare_desired())
        return m_chance * m_prob + r_chance * r_prob

    def report(self):
        return (f"{self.total} {self.set_code}: " +
                f"{self.mythic_desired()} mythics, " +
                f"{self.rare_desired()} rares: " +
                f"chance per pack: {self.chance_per_pack()}\n")

class SetCounter:
    def __init__(self, library):
        self.library = library
        self.counters = {}

    def tally(self, card, count):
        set_code = card.value("setCode")
        counter = self.counters.get(set_code,
                                    SetCardCounter(set_code, self.library))
        counter.tally(card, count)
        self.counters[set_code] = counter

    def report(self):
        return "".join([counter.report()
                        for counter in sorted(self.counters.values(),
                                              key=lambda c: -c.total)])


class DeckReporter:
    def __init__(self, library):
        self.card_counter = CardCounter()
        self.set_counter = SetCounter(library)

    def report(self, deck):
        missing = deck.missing()
        if missing != []:
            return (f"{deck.name} is incomplete\n" +
                    self.missing_report(missing))
        return f"{deck.name} is complete\n"

    def missing_report(self, missing):
        return _rarity_report(self._rarity_dict(missing))

    def name_report(self):
        return self.card_counter.report()

    def card_set_report(self):
        return self.set_counter.report()

    def _rarity_dict(self, missing):
        by_rarity = {}
        for count, card in missing:
            rarity = card.value("rarity")
            if rarity in ["mythic", "rare"]:
                entry = by_rarity.get(rarity, [])
                entry.append([count, card.name(), card.value("setCode")])
                by_rarity[rarity] = entry
                self._tally(card, count)
        return by_rarity

    def _tally(self, card, count):
        self.card_counter.tally(card, count)
        self.set_counter.tally(card, count)

def _rarity_report(by_rarity):
    result = ""
    for rarity in ['mythic', 'rare']:
        if rarity in by_rarity:
            total = 0
            summary = []
            for count, name, set_code in by_rarity[rarity]:
                total += count
                vote_name = f"{name} ({set_code})"
                summary.append(f"{count} {vote_name}")
            result += f"  {total} {rarity}: {', '.join(summary)}\n"
        else:
            result += f"  0 {rarity}\n"
    return result

def _prob_of_some(counts, desired):
    owned, available = counts
    missing = available - owned
    return 1 - pow(1 - 1.0 / missing, desired)
