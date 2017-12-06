class Compiler:
    def right(self):
        self.bf_out.write('>')

    def left(self):
        self.bf_out.write('<')

    def inc(self):
        self.bf_out.write('+')

    def dec(self):
        self.bf_out.write('-')

    def print_cell(self):
        self.bf_out.write('.')

    def read_cell(self):
        self.bf_out.write(',')

    def do(self, args):
        for operation in args:
            if isinstance(operation, str):
                if operation in self.node_to_func:
                    self.node_to_func[operation]()
                if operation in self.node_to_func_def:
                    self.compile(self.node_to_func_def[operation])
            elif isinstance(operation, list):
                self.compile(operation)

    def loop(self, args):
        self.bf_out.write('[')
        self.do(args)
        self.bf_out.write(']')

    def define(self, args):
        head, parenthesis, list_of_commands, *tail = args
        commands = []
        for command in list_of_commands:
            commands.append(command)

        self.node_to_func_def[head] = commands

    def add(self, args):
        times = args[0]
        for i in range(int(times)):
            self.bf_out.write('+')

    def sub(self, args):
        times = args[0]
        for i in range(int(times)):
            self.bf_out.write('-')

    def do_after(self, args):
        head, *tail = args
        another_tail = []
        for x in tail:
            if isinstance(x, list):
                for k in x:
                    another_tail.append(['do', k, head])
            else:
                another_tail.append(x)
        another_tail.insert(0, 'do')
        self.compile(another_tail)


    def do_before(self, args):
        head, *tail = args
        another_tail = []
        for x in tail:
            if isinstance(x, list):
                for k in x:
                    another_tail.append(['do', head, k])
            else:
                another_tail.append(x)
        another_tail.insert(0, 'do')
        self.compile(another_tail)

    def compile(self, commands=None):
        if commands is None:
            commands = self.ast

        head, *tail = commands

        if head in self.node_to_func:
            self.node_to_func[head]()
        elif head in self.node_to_func_with_args:
            self.node_to_func_with_args[head](tail)

    def __init__(self, ast, bf_out):
        self.bf_out = open(bf_out, "w")
        self.ast = ast

        self.node_to_func = {
            'right': self.right,
            'left': self.left,
            'inc': self.inc,
            'dec': self.dec,
            'print': self.print_cell,
            'read': self.read_cell,
        }

        self.node_to_func_with_args = {
            'loop': self.loop,
            'do': self.do,
            'def': self.define,
            'add': self.add,
            'sub': self.sub,
            'do-before': self.do_before,
            'do-after': self.do_after,
        }

        self.node_to_func_def = {}
