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
pile = []


css_output = ""

css_context = [("selector","body")]


@addToClass(AST.ProgramNode)
def execute(self):
    print("szds")
    for c in self.children:
        c.execute()


@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:

            if "\"" in self.tok:
                return self.tok.replace("\"", "")
            else:
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
    # print("SET %s" % type(self.children[1]))


@addToClass(AST.PrintNode)
def execute(self):
    print(self.children[0].execute())


@addToClass(AST.CssNode)
def execute(self):

    last = css_context[-1]

    css = self.children[0].tok

    print("This will be outputed in %s with the value %s" % (last,css))

    return


@addToClass(AST.ConditionNode)
def execute(self):
    if (self.children[0].execute()):
        self.children[1].execute()


@addToClass(AST.IsEqualNode)
def execute(self):
    return self.children[0].execute() == self.children[1].execute()


@addToClass(AST.WhileNode)
def execute(self):
    ix = self.children[0].children[1].tok
    end = self.children[1].children[1].tok
    increment = self.children[2].children[1].tok

    while ix < end:
        vars['ix'] = ix
        self.children[3].execute()
        ix += increment


@addToClass(AST.KeyframesNode)
def execute(self):
    name = self.children[0].children[1].tok
    css_context.append(
        ("keyframes", name)
    )
    res = self.children[1].execute()
    css_context.pop()
    return res


@addToClass(AST.AnimationNode)
def execute(self):
    name = self.children[0].children[1].tok
    css_context.append(
        ("selector", name)
    )
    return self.children[1].execute()


@addToClass(AST.FrameNode)
def execute(self):
    name = self.children[0].children[1].tok
    css_context.append(
        ("frame", name)
    )
    return self.children[1].execute()


if __name__ == "__main__":
    from parser import parse
    import sys

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()
