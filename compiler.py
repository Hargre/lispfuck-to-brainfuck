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
            elif isinstance(operation, list):
                self.compile(operation)

    def loop(self, args):
        self.bf_out.write('[')
        self.do(args)
        self.bf_out.write(']')

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
        }


test = ['do', 'right', 'left', ['loop', 'inc', 'dec'], 'print', 'read']
compiler = Compiler(test, "test.bf")

compiler.compile()