import AST
from AST import addToClass
from functools import reduce

from CssVarExtractor import extract
from CssWriter import CssWriter

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: int(x) % int(y),
}

vars = {}

"""
css_output = {
    "selectors": {
        "#tata" : [],
        "body" : [],
        ".test3": []
    },
    "keyframes": {
        "anim1":{
            "30%": ["color:red;", "background-color: 0000"],
        },
        "anim2":[]
    }
}
"""

css_output = {
    "selectors": {
        "body": []
    },
    "keyframes": {}
}

css_context = [("selector", "body")]


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

            if "\"" in self.tok:
                return self.tok.replace("\"", "")
            else:
                print('*** Error: variable %s undefined ! ' % self.tok)

    if not isinstance(self.tok, AST.TokenNode):
        return self.tok
    else:
        return self.tok.execute()


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

    css = str(self.children[0].tok)

    extracted_vars = extract(css, vars)

    for var in extracted_vars:
        clean_var = vars[var]

        if isinstance(clean_var, float):
            clean_var = int(clean_var)

        css = css.replace("$%s" % var, str(clean_var))

    if last[0] == "animation":
        name = last[1]
        selector = last[2]

        if selector not in css_output["selectors"]:
            css_output["selectors"][selector] = ["animation-name: {0}".format(name)]
        css_output["selectors"][selector].append(css)

    elif last[0] == "frame":
        value = last[1]
        name = last[2][1]

        if name not in css_output["keyframes"]:
            css_output["keyframes"][name] = {}
        if value not in css_output["keyframes"][name]:
            css_output["keyframes"][name][value] = []
        css_output["keyframes"][name][value].append(css)

    elif last[1] == "body":
        css_output["selectors"]["body"].append(css)

    print("This will be output in %s with the value %s" % (last, css))

    return


@addToClass(AST.ConditionNode)
def execute(self):
    if self.children[0].execute():
        self.children[1].execute()


@addToClass(AST.IsEqualNode)
def execute(self):
    return self.children[0].execute() == self.children[1].execute()


@addToClass(AST.IsLessNode)
def execute(self):
    return self.children[0].execute() < self.children[1].execute()


@addToClass(AST.IsGreaterNode)
def execute(self):
    return self.children[0].execute() > self.children[1].execute()


@addToClass(AST.WhileNode)
def execute(self):
    ix = self.children[0].children[1].execute()
    end = self.children[1].children[1].execute()
    increment = self.children[2].children[1].tok

    while ix < end:
        vars['ix'] = ix
        self.children[3].execute()
        ix += increment


@addToClass(AST.KeyframesNode)
def execute(self):
    name = css_context[-1]

    css_context.append(
        ("keyframes", name)
    )
    res = self.children[0].execute()

    css_context.pop()

    return res


@addToClass(AST.AnimationNode)
def execute(self):
    name = self.children[0].children[1].tok
    selector = self.children[1].children[1].tok
    css_context.append(
        ("animation", name, selector)
    )
    res = self.children[2].execute()
    css_context.pop()
    return res


@addToClass(AST.FrameNode)
def execute(self):
    value = int(self.children[0].children[1].execute())
    css_context.append(
        ("frame", value, css_context[-1][1])
    )
    res = self.children[1].execute()
    css_context.pop()
    return res


if __name__ == "__main__":
    from parser import parse
    import sys

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()
    writer = CssWriter()
    writer.write_context(css_output)
