import io
from percheron.deck_commander import DeckCommander
from percheron.library import Library

PROGRAM = "percheron-test"

DECK_NAME = "Werewolves"
NAME_DECK = f"name {DECK_NAME}\n"

NAME_1 = "Lunarch Veteran"
SHORT_SPEC_1 = f"4 {NAME_1}"
LONG_SPEC_1 = f"{SHORT_SPEC_1} (MID) 27"

NAME_2 = "Skyclave Cleric"
SHORT_SPEC_2 = f"3 {NAME_2}"
LONG_SPEC_2 = f"{SHORT_SPEC_2} (ZNR) 40"

NAME_3 = "Cleric of Life's Bond"
SHORT_SPEC_3 = f"1 {NAME_3}"
LONG_SPEC_3 = f"{SHORT_SPEC_3} (ZNR) 222"

LONG_SPEC_BAD = "4 Bad Card (BAD) 1234"

AMBIGOUS_NAME = "doom"


DECK = """
Deck
4 Brutal Cathar (MID) 7
4 Forest (VOW) 402
4 Rahilda, Wanted Cutthroat (Y22) 42
4 Forsaken Crossroads (Y22) 63
4 Reckless Stormseeker (MID) 157
4 Ascendant Packleader (VOW) 186
4 Tenacious Pup (Y22) 56
4 Werewolf Pack Leader (AFR) 211
3 Ranger Class (AFR) 202
3 Tovolar, Dire Overlord (MID) 246
2 Fateful Absence (MID) 18
4 Inquisitor Captain (Y22) 8
2 Lair of the Hydra (AFR) 259
4 Cragcrown Pathway (ZNR) 261
4 Needleverge Pathway (ZNR) 263
4 Branchloft Pathway (ZNR) 258
2 Rockfall Vale (MID) 266

Sideboard
1 Containment Breach (STX) 125
1 Environmental Sciences (STX) 1
1 Mascot Exhibition (STX) 5
1 Bloodrage Alpha (Y22) 36
1 Avabruck Caretaker (VOW) 187
2 Legion Angel (ZNR) 23
"""

def test_incomplete_status():
    cmds = f"{NAME_DECK}1{LONG_SPEC_3}\nstatus" # Can't have more than 10
    assert f"{DECK_NAME} is incomplete" in _process_cmds(cmds)

def test_complete_status():
    cmds = f"{NAME_DECK}{LONG_SPEC_3}\nstatus"
    assert f"{DECK_NAME} is complete" in _process_cmds(cmds)

def test_deck_status():
    cmds = f"{NAME_DECK}{DECK}\nstatus"
    assert f"{DECK_NAME} is incomplete" in _process_cmds(cmds)

def test_write():
    cmds = f"{NAME_DECK}{DECK}write test/files/test.json"
    assert "Successfully wrote test/files/test.json" in _process_cmds(cmds)

def test_read():
    cmds = f"{NAME_DECK}read test/files/test.json"
    assert "Successfully read test/files/test.json" in _process_cmds(cmds)

def test_read_empty():
    cmds = f"{NAME_DECK}read test/files/empty_dict.json"
    assert "Unable to read content" in _process_cmds(cmds)

def test_read_non_list():
    cmds = f"{NAME_DECK}read test/files/non_list.json"
    assert "not a JSON list" in _process_cmds(cmds)

def test_read_non_json():
    cmds = f"{NAME_DECK}{DECK}read cli"
    assert "Unable to parse cli" in _process_cmds(cmds)

def test_read_missing_file():
    cmds = f"{NAME_DECK}{DECK}read file that does not exist"
    assert "Unable to read content" in _process_cmds(cmds)

def test_read_unnamed_deck_file():
    cmds = f"{NAME_DECK}{DECK}read test/files/unnamed.json"
    assert "Unable to load unnamed deck" in _process_cmds(cmds)

def test_run_help():
    cmds = "help"
    assert DeckCommander.HELP in _process_cmds(cmds)

def test_decklist():
    cmds = f"{NAME_DECK}decklist"
    assert DECK_NAME in _process_cmds(cmds)

def test_cards_no_deck():
    cmds = "cards"
    assert "No deck selected" in _process_cmds(cmds)

def test_cards_no_name():
    cmds = f"{SHORT_SPEC_1}"
    assert "Select a deck with the 'name' command" in _process_cmds(cmds)

def test_cards_empty_deck():
    cmds = f"{NAME_DECK}cards"
    assert not "Sideboard" in _process_cmds(cmds)

def test_add_card():
    cmds = f"{NAME_DECK}{NAME_1}\ncards"
    output = _process_cmds(cmds)
    assert "Failed" not in output
    assert f"Deck\n1 {NAME_1}" in output

def test_add_ambigous_card_spec():
    cmds = f"{NAME_DECK}{AMBIGOUS_NAME}\ncards"
    assert f"'{AMBIGOUS_NAME}' is ambigous" in _process_cmds(cmds)

def test_add_long_card_spec():
    cmds = f"{NAME_DECK}{LONG_SPEC_1}\ncards"
    output = _process_cmds(cmds)
    assert "Failed" not in output
    assert f"Deck\n{SHORT_SPEC_1}" in output

def test_add_short_card_spec():
    cmds = f"{NAME_DECK}{SHORT_SPEC_1}\ncards"
    output = _process_cmds(cmds)
    assert f"Deck\n{SHORT_SPEC_1}" in output

def test_add_lower_card_spec():
    cmds = f"{NAME_DECK}{SHORT_SPEC_1.lower()}\ncards"
    output = _process_cmds(cmds)
    assert f"Deck\n{SHORT_SPEC_1}" in output

def test_add_two_card_same_set():
    cmds = f"{NAME_DECK}{LONG_SPEC_2}\n{LONG_SPEC_3}\ncards"
    output = _process_cmds(cmds)
    assert f"{SHORT_SPEC_3}" in output

def test_add_same_card_twice():
    cmds = f"{NAME_DECK}{LONG_SPEC_3}\n{LONG_SPEC_3}\ncards"
    output = _process_cmds(cmds)
    expected_count = 2*int(LONG_SPEC_3.split(" ")[0])
    assert f"Deck\n{expected_count}" in output

def test_add_same_card_then_remove():
    cmds = (f"{NAME_DECK}{LONG_SPEC_3}\n{LONG_SPEC_3}\n" +
            f"-{LONG_SPEC_3}\ncards")
    output = _process_cmds(cmds)
    expected_count = int(LONG_SPEC_3.split(" ")[0])
    assert f"Deck\n{expected_count}" in output

def test_add_card_then_remove_all():
    cmds = (f"{NAME_DECK}{LONG_SPEC_1}\n- {NAME_1}\n" +
            "cards")
    assert "Deck\n\n" in _process_cmds(cmds)

def test_skip_bad_card():
    cmds = f"{NAME_DECK}{LONG_SPEC_BAD}\ncards"
    assert "Failed" in _process_cmds(cmds)

def test_add_to_sideboard():
    cmds = f"{NAME_DECK}sb\n{LONG_SPEC_1}\ncards"
    output = _process_cmds(cmds)
    assert f"Sideboard\n{SHORT_SPEC_1}" in output

def test_add_to_deck_after_sideboard():
    cmds = (f"{NAME_DECK}sb\n{LONG_SPEC_1}\n" +
            f"deck\n{LONG_SPEC_2}\ncards")
    output = _process_cmds(cmds)
    assert f"Deck\n{SHORT_SPEC_2}" in output

def _process_cmds(cmds):
    output = io.StringIO()
    DeckCommander(PROGRAM, Library()).run(io.StringIO(cmds + "\n.\n"), output)
    return output.getvalue()
