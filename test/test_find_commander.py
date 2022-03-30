import io
from percheron.find_commander import FindCommander
from percheron.library import Library

PROGRAM = "percheron-test"

def _process_cmds(cmds):
    output = io.StringIO()
    FindCommander(PROGRAM, Library()).run(io.StringIO(cmds), output)
    return output.getvalue()

def test_run_help():
    cmds = "help\n.\n"
    assert FindCommander.HELP in _process_cmds(cmds)

def test_single_card():
    cmds = "set vow\nabra\n.\n"
    assert "Abrade" in _process_cmds(cmds)

def test_multiple_cards():
    cmds = "set vow\na\n.\n"
    assert "Multiple matches" in _process_cmds(cmds)

def test_doomskar():
    cmds = "set khm\ndoom .\n.\n"
    assert "Doomskar" in _process_cmds(cmds)

def test_escaped_regex():
    cmds = "set afr\n\\+2\n.\n"
    assert "+2 Mace" in _process_cmds(cmds)

def test_regex_fail():
    cmds = "set afr\n+2\n.\n"
    assert "+2 Mace" not in _process_cmds(cmds)

def test_no_cards():
    cmds = "set vow\nno match\n.\n"
    assert "Could not find match" in _process_cmds(cmds)
