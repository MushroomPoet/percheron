import io
from percheron.root_commander import RootCommander
from percheron.library import Library

PROGRAM = "percheron-test"
SUBCOMMANDS = ["find", "score", "value", "count", "draft", "sealed"]

def test_run_exit():
    cmds = ".\n"
    assert PROGRAM in _process_cmds(cmds)

def test_run_help():
    cmds = "help\n.\n"
    assert RootCommander.HELP in _process_cmds(cmds)

def test_run_unrecognized_command():
    cmds = "unrecognized\n.\n"
    assert "Unrecognized command" in _process_cmds(cmds)

def test_report_is_set_dependent():
    cmds = "report\n.\n"
    assert "Card set not specified" in _process_cmds(cmds)

def test_run_subcommands():
    for subcommand in SUBCOMMANDS:
        cmds = subcommand + "\n.\n.\n"
        assert subcommand in _process_cmds(cmds)

def test_run_report():
    cmds = "set vow\nreport\n.\n"
    assert "Vampire's Kiss" in _process_cmds(cmds)

def test_run_update_filename_write():
    source = "test/files/znr.json"
    cmds = (f"update {source}\n" +
            "filename test/files/all.json\nwrite\n.\n")
    output = _process_cmds(cmds)
    assert f"Loading {source}" in output
    assert "Changing filename from" in output
    assert "Updated ZNR" in output

def test_run_update_non_dict():
    source = "test/files/test.json"
    cmds = f"update {source}\n.\n"
    assert f"Cannot find data in {source}" in _process_cmds(cmds)

def test_run_update_add_junk_card():
    cmds = "update test/files/junk.json\n.\n"
    output = _process_cmds(cmds)
    assert "Adding new card set" in output
    assert "New card" in output

def test_run_update_add_description_to_junk_card():
    cmds = "update test/files/junk.json\nupdate test/files/junk2.json\n.\n"
    assert "Added description" in _process_cmds(cmds)

def test_run_update_bad_updates():
    cmds = "update test/files/bad_updates.json\n.\n"
    assert "Updated" not in _process_cmds(cmds)

def test_report_on_junk_card_set():
    cmds = "set junk\nreport\n.\n"
    expected = "JUNK is not a known card set"
    assert expected in _process_cmds(cmds)

def test_rarity():
    cmds = "rarity vow\n.\n"
    assert "Mythics" in _process_cmds(cmds)

def test_rarity_bogus_set():
    cmds = "rarity bogus\n.\n"
    assert "Mythics" not in _process_cmds(cmds)

def _process_cmds(cmds):
    output = io.StringIO()
    RootCommander(PROGRAM, Library()).run(io.StringIO(cmds), output)
    return output.getvalue()
