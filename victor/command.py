__all__ = ['CommandException', 'register_ex_command', 'run_ex_command'];

ex_commands = { };

class CommandException(BaseException):
    pass;

def run_ex_command(command_line):
    tokens = command_line[1:].split();

    f = ex_commands.get(tokens[0], None);
    if f is None: raise CommandException('unable to find command {}'.format(tokens[0]));
    return f(*tokens[1:]);

def register_ex_command(command, f):
    ex_commands[command] = f;
