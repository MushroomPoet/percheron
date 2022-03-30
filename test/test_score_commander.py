import io
from percheron.score_commander import ScoreCommander
from percheron.library import Library

PROGRAM = "percheron-test"

def test_run_help():
    cmds = "help\n.\n"
    assert ScoreCommander.HELP in _process_cmds(cmds)

def test_multiple_cards():
    cmds = "set znr\na\n.\n"
    assert "Multiple matches" in _process_cmds(cmds)

def test_no_cards():
    cmds = "set znr\nno match\n.\n"
    assert "Could not find match" in _process_cmds(cmds)

def test_single_card():
    cmds = "set znr\nphyl\n.\n"
    expected = '"Phylath, World Sculptor" given the score 1'
    assert expected in _process_cmds(cmds)

def test_single_card_with_score():
    cmds = "set znr\n266 phyl\n.\n"
    expected = '"Phylath, World Sculptor" given the score 266'
    assert expected in _process_cmds(cmds)

def _process_cmds(cmds):
    output = io.StringIO()
    ScoreCommander(PROGRAM, Library()).run(io.StringIO(cmds), output)
    return output.getvalue()
