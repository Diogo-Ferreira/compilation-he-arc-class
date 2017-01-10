import AST
from AST import addToClass
from functools import reduce

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}

vars = {}


@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print('*** Error: variable %s undefined ! ' % self.tok)
    return self.tok


@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]

    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()
    #print("SET %s" % type(self.children[1]))


@addToClass(AST.PrintNode)
def execute(self):
    print(self.children[0].execute())


@addToClass(AST.WhileNode)
def execute(self):
    ix = self.children[0].children[1].tok
    end = self.children[1].children[1].tok
    increment = self.children[2].children[1].tok

    while ix < end:
        vars['ix'] = ix
        self.children[3].execute()
        ix += increment

if __name__ == "__main__":
    from parser import parse
    import sys

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()
