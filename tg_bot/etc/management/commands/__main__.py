import pkgutil
import pathlib
import functools
import importlib


class BaseCommand:
    def __init__(self):
        pass

    def handle(self):
        raise ValueError("The function is not overridden")

    @classmethod
    def all_commands(cls):
        commands = cls.__subclasses__().copy()
        return commands


def execute_from_command_line(args):
    if 1 == len(args):
        args.append("run")

    command = args[1]
    commands = get_commands()

    if command not in commands:
        ValueError("Unknown command: '{}'".format(command))

    command = importlib.import_module("tg_bot.etc.management.commands.{}".format(command))
    command.Command().handle()


def find_commands():
    command_dir = pathlib.Path(__file__).resolve().parent
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


@functools.lru_cache(maxsize=None)
def get_commands():
    commands = {name: "tg_bot.etc.management.commands.{}".format(name) for name in find_commands()}
    return commands
