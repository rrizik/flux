import _globals

commands = {}


class CommandInfo:
    tooltip = ""
    name = None
    proc = None
    arg_count_min = None
    arg_count_max = None

    def __getitem__(cls, index):
        return cls.name[index]

    def __len__(cls):
        return len(cls.name)


def init_commands():
    add_command("editor", command_editor, tooltip="enables/disables editor mode")
    add_command("save_level", command_save_level, 1, 1, tooltip="saves the current level to a file")
    add_command("new_level", command_new_level, tooltip="creates a blank new level")
    add_command("quit", command_quit, tooltip="quit the engine")
    add_command("exit", command_quit, tooltip="quit the engine")
    add_command("clear", command_clear, tooltip="clears console history")
    add_command("help", command_help, 0, 1, tooltip="lists all commands")
    add_command("helpppppp", command_help, 0, 1, tooltip="lists all commands")
    add_command("helpbbbbb", command_help, 0, 1, tooltip="lists all commands")
    add_command("hel_2", command_help, 0, 1, tooltip="lists all commands")
    add_command("cursor_underscored", command_cursor_underscored, 1, 1, tooltip="changes whether the cursor is underscored or full (0, 1)")
    add_command("selection_data", command_selection_data, tooltip="shows selection data")


def add_command(name, proc, arg_count_min=0, arg_count_max=0, tooltip=""):
    info = CommandInfo()
    info.name = name
    info.proc = proc
    info.arg_count_min = arg_count_min
    info.arg_count_max = arg_count_max
    info.tooltip = tooltip
    commands[str(name)] = info


def get_commands():
    return commands.values()


def get_command_names():
    return commands.keys()


def get_command(command_name):
    if command_name in commands.keys():
        return commands[command_name]

    return None


def run_command(command_string):
    command_array = list(filter(None, command_string.split(" ")))
    if not len(command_array):
        return

    command_name = command_array[0]
    command_arguments = command_array[1:]
    command_input(command_string)

    command = get_command(command_name)
    if command is not None:
        command.proc(command_arguments)
    else:
        command_output("Uknown command \"%s\"" % command_name)


def command_output(command):
    _globals.history_output.insert(0, str(command))


def command_input(command):
    _globals.history_input.insert(0, command)


def command_ls(arguments):
    command_output("We called ls with arguments: %s" % arguments)
    command_output("We called ls!!")


def command_clear(arguments):
    _globals.history_output = []
    command_output("history cleared!")


def command_quit(arguments):
    command_output("We called quit. existing!")
    _globals.running = False


def command_editor(arguments):
    if len(arguments) == 0:
        command_output("\"editor\" = \"%s\"" % _globals.editor)
    elif arguments[0] == "0" or arguments[0] == "1":
        _globals.editor = int(arguments[0])
        command_output("\"editor\" = \"%s\"" % _globals.editor)
    else:
        command_output("invalid arguments. 0 or 1")


def command_cursor_underscored(arguments):
    pass


def command_selection_data(arguments):
    pass


def command_save_level(arguments):
    pass


def command_new_level(arguments):
    pass


def command_help(arguments):
    if arguments:
        command = get_command(arguments[0])
        if command is not None:
            command_output(command.name + " - " + command.tooltip)
        else:
            command_output(str(arguments[0]) + " - Unkown command")
    else:
        for command in get_commands():
            command_output(command.name + " - " + command.tooltip)