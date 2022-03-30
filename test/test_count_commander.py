import io
from percheron.count_commander import CountCommander
from percheron.library import Library

PROGRAM = "percheron-test"

def test_run_help():
    cmds = "help\n.\n"
    assert CountCommander.HELP in _process_cmds(cmds)

def test_multiple_cards():
    cmds = "set iko\na\n.\n"
    assert "Multiple matches" in _process_cmds(cmds)

def test_no_cards():
    cmds = "set iko\nno match\n.\n"
    assert "Could not find match" in _process_cmds(cmds)

def test_report():
    cmds = "set iko\nreport\n.\n"
    assert "\tBrokkos, Apex of Forever" in _process_cmds(cmds)

def test_single_card():
    cmds = "set iko\nbrok\n.\n"
    assert 'Found "Brokkos, Apex of Forever"' in _process_cmds(cmds)

def test_single_card_with_count():
    cmds = "set iko\n3 brok\n.\n"
    expected = '"Brokkos, Apex of Forever" given the count 3'
    assert expected in _process_cmds(cmds)

def test_single_explicit_card():
    cmds = "4 Brokkos, Apex of Forever (IKO) 179\n.\n"
    expected = '"Brokkos, Apex of Forever" given the count 4'
    assert expected in _process_cmds(cmds)

def _process_cmds(cmds):
    output = io.StringIO()
    CountCommander(PROGRAM, Library()).run(io.StringIO(cmds), output)
    return output.getvalue()
