import io
from percheron.sealed_commander import SealedCommander
from percheron.library import Library

PROGRAM = "percheron-test"
POOL = """
Cemetery Desecrator
Cemetery Illuminator
Cemetery Protector
Creepy Puppeteer
Hamlet Vanguard
Bleed Dry
Brine Comber // Brinebound Gift
Reclusive Taxidermist
Bramble Wurm
Abrade
Twinblade Geist // Twinblade Invocation
Fleeting Spirit
Fleeting Spirit
Diver Skaab
Oakshade Stalker // Moonlit Ambusher
Old Rutstein
Blood Hypnotist
Panicked Bystander // Cackling Culprit
Distracting Geist // Clever Distraction
Apprentice Sharpshooter
Edgar's Awakening
Edgar's Awakening
Cruel Witness
Hookhand Mariner // Riphook Raider
Drogskol Infantry // Drogskol Armaments
Flourishing Hunter
Scattered Thoughts
Nature's Embrace
Nature's Embrace
Markov Retribution
Blood Petal Celebrant
Vampire Slayer
Vampire Slayer
Piercing Light
Mischievous Catgeist // Catlike Curiosity
Kindly Ancestor // Ancestor's Embrace
Kindly Ancestor // Ancestor's Embrace
Rural Recruit
Howling Moon
Lacerate Flesh
Mindleech Ghoul
Parish-Blade Trainee
Fearful Villager // Fearsome Werewolf
Kessig Flamebreather
Into the Night
Into the Night
Belligerent Guest
Heron of Hope
Gift of Fangs
Syphon Essence
Syphon Essence
Syphon Essence
Steelclad Spirit
Nebelgast Beguiler
Weary Prisoner // Wrathful Jailbreaker
Wretched Throng
Sporeback Wolf
Sheltering Boughs
Sheltering Boughs
Falkenrath Celebrants
Persistent Specimen
Gluttonous Guest
Gluttonous Guest
Diregraf Scavenger
Repository Skaab
Heron-Blessed Geist
Adamant Will
Toxic Scorpion
Toxic Scorpion
Pointed Discussion
Skywarp Skaab
Selhoff Entomber
Selhoff Entomber
Cradle of Safety
Traveling Minister
Unhallowed Phalanx
Honored Heirloom
Honored Heirloom
Blood Fountain
Unholy Officiant
Unholy Officiant
Lantern of the Lost
Ceremonial Knife
Blood Servitor
Groom's Finery
"""
POOL_SIZE = 85

def test_run_help():
    cmds = "help\n.\n"
    assert SealedCommander.HELP in _process_cmds(cmds)

def test_multiple_cards():
    cmds = "set vow\na\n.\n"
    assert "Multiple matches" in _process_cmds(cmds)

def test_no_cards():
    cmds = "set vow\nno match\n.\n"
    assert "Could not find match" in _process_cmds(cmds)

def test_sealed_cards():
    commander = SealedCommander(PROGRAM, Library())
    commander.run(io.StringIO(f"set vow\n{POOL}.\n"),
                  io.StringIO())
    assert len(commander.card_pool) == POOL_SIZE

def test_sealed_cards_with_reset():
    commander = SealedCommander(PROGRAM, Library())
    commander.run(io.StringIO(f"set vow\n{POOL}!\n.\n"),
                  io.StringIO())
    assert len(commander.card_pool) == 0

def test_pool():
    cmds = f"set vow\n{POOL}pool\n.\n"
    assert "Groom's Finery (uncommon)" in _process_cmds(cmds)

def test_export():
    cmds = f"set vow\n{POOL}export\n.\n"
    assert "2 Unholy Officiant" in _process_cmds(cmds)

def test_accurate_list():
    cmds = "set vow\ncem des\ncem prot\nexport\n.\n"
    output = _process_cmds(cmds)
    assert "Cemetery Desecrator" in output
    assert "Cemetery Protector" in output

def test_supports_cards_with_no_score():
    cmds = "set vow\ncem des\nplains\nexport\n.\n"
    output = _process_cmds(cmds)
    assert "Cemetery Desecrator" in output
    assert "Plains" in output

def test_compare():
    cmds = f"set vow\n{POOL}compare\n.\n"
    assert "B, W, 2.8" in _process_cmds(cmds)

def test_build():
    cmds = f"set vow\n{POOL}build b w\n.\n"
    output = _process_cmds(cmds)
    assert "Gluttonous Guest (common)" in output
    assert "cards: 23" in output

def test_empty_build():
    cmds = "set vow\nbuild b w\n.\n"
    assert "Empty deck" in _process_cmds(cmds)

def _process_cmds(cmds):
    output = io.StringIO()
    SealedCommander(PROGRAM, Library()).run(io.StringIO(cmds), output)
    return output.getvalue()
