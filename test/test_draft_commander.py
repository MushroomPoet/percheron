import io
from percheron.draft_commander import DraftCommander
from percheron.library import Library

PROGRAM = "percheron-test"

def test_run_help():
    cmds = "help\n.\n"
    assert DraftCommander.HELP in _process_cmds(cmds)

def test_multiple_cards():
    cmds = "set mid\na\n.\n"
    assert "Multiple matches" in _process_cmds(cmds)

def test_no_cards():
    cmds = "set mid\nno match\n.\n"
    assert "Could not find match" in _process_cmds(cmds)

def test_draft_cards():
    commander = DraftCommander(PROGRAM, Library())
    commander.run(io.StringIO("set mid\nt me ma\nw a s\nto hu\n.\n"),
                  io.StringIO())
    assert len(commander.drafted_cards) == 3

def test_draft_cards_with_reset():
    commander = DraftCommander(PROGRAM, Library())
    commander.run(io.StringIO("set mid\nt me ma\nw a s\nto hu\n!\n.\n"),
                  io.StringIO())
    assert len(commander.drafted_cards) == 0

def _process_cmds(cmds):
    output = io.StringIO()
    DraftCommander(PROGRAM, Library()).run(io.StringIO(cmds), output)
    return output.getvalue()
