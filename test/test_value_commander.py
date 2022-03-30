import io
from percheron.value_commander import ValueCommander
from percheron.library import Library

PROGRAM = "percheron-test"

def test_run_help():
    cmds = "help\n.\n"
    assert ValueCommander.HELP in _process_cmds(cmds)

def test_multiple_cards():
    cmds = "set akr\na\n.\n"
    assert "Multiple matches" in _process_cmds(cmds)

def test_no_cards():
    cmds = "set akr\nno match\n.\n"
    assert "Could not find match" in _process_cmds(cmds)

def test_report():
    cmds = "set akr\nreport\n.\n"
    assert "Deem Worthy" in _process_cmds(cmds)

def test_single_card():
    cmds = "set akr\nde wo\n.\n"
    assert "Deem Worthy" in _process_cmds(cmds)

def test_single_card_with_new_value():
    cmds = "set akr\n3.5 de wo\n.\n"
    expected = """\"Deem Worthy\" given the value 3.5
Previous value was 3.53 which was inferred"""
    assert expected in _process_cmds(cmds)

def test_single_card_with_old_value():
    cmds = "set akr\n4.3 grind\n.\n"
    expected = """\"Grind // Dust\" given the value 4.3
Previous value was 4.3 which was known"""
    assert expected in _process_cmds(cmds)

def _process_cmds(cmds):
    output = io.StringIO()
    ValueCommander(PROGRAM, Library()).run(io.StringIO(cmds), output)
    return output.getvalue()
