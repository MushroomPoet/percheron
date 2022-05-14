import sys

class Commander:
    HELP = """
. - Exit the current command mode
?, help - List commands available in current command mode
set <set-abbrev> - Change the set for commands.
    If unrecognized, list all set abbreviations
"""

    def __init__(self, mode, library, depth=1):
        self.running = True
        self.depth = depth
        self.mode = mode
        self.library = library
        self.io_in = sys.stdin
        self.change_output_stream(sys.stdout)

    def change_output_stream(self, stream):
        self.io_out = stream
        self.library.change_output_stream(stream)

    def run(self, io_in, io_out):
        self.io_in = io_in
        self.change_output_stream(io_out)
        while self.running:
            self.prompt()
            cmd = io_in.readline().strip()
            if cmd != "":
                self.process_cmd(cmd)

    def prompt(self, suffix=""):
        self.io_out.write(f"{'*' * self.depth} {self.mode}{suffix}> ")
        self.io_out.flush()

    def help(self):
        self.writeline(Commander.HELP)

    def writeline(self, line): # Equivalent of print
        self.io_out.write(str(line) + "\n")
        self.io_out.flush()

    def exit_mode(self):
        pass

    def process_cmd(self, cmd):
        if cmd == ".":
            self.exit_mode()
            self.running = False
        elif cmd in ["?", "help"]:
            self.help()
        elif cmd.startswith("set"):
            self.library.change_set(cmd.split(" ")[1:])
        elif cmd.startswith("update "):
            self.library.update_arena_card_sets(
                cmd[cmd.index(" ") + 1:].strip())
        elif cmd.startswith("filename "):
            self.library.change_filename(cmd[cmd.index(" ") + 1:].strip())
        elif cmd == "write":
            self.library.write_card_sets()
        else:
            return False
        return True
