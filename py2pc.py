import ast


class Keywords:
    IF = "if"
    THEN = "then"
    ELSE = "else"
    ENDIF = "endif"
    WHILE = "while"
    REPEAT = "repeat"
    ENDWHILE = "end"
    ASSIGN = "<-"
    RETURN = "return"
    FUNCTION = "function"


operator_map = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.Mod: "mod",
    ast.USub: "-",
    ast.Eq: "=",
    ast.NotEq: "!=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: "<=",
}


class Visitor(ast.NodeVisitor):
    def __init__(self, Keywords=Keywords):
        self.Keywords = Keywords

    def visit_all(self, nodes):
        for node in nodes:
            yield from self.visit(node)

    def visit_Module(self, node):
        for stmt in node.body:
            yield from self.visit(stmt)

    def make_annotation(self, a):
        if a is None:
            return ""
        return f": {a.s}"

    def visit_FunctionDef(self, node):
        args = ", ".join(
            f"{a.arg}{self.make_annotation(a.annotation)}"
            for a in node.args.args
        )
        yield f"{self.Keywords.FUNCTION} {node.name}({args}){self.make_annotation(node.returns)}"
        yield from self.indent_all(self.visit_all(node.body))

    def visit_Assign(self, node):
        [target] = node.targets
        yield f"{self.visit(target)} {self.Keywords.ASSIGN} {self.visit(node.value)}"

    def visit_Name(self, node):
        return node.id

    def visit_Num(self, node):
        return str(node.n)

    def visit_BinOp(self, node):
        return f"{self.visit(node.left)} {operator_map[type(node.op)]} {self.visit(node.right)}"

    def visit_UnaryOp(self, node):
        return f"{operator_map[type(node.op)]}{self.visit(node.operand)}"

    def visit_Subscript(self, node):
        return f"{self.visit(node.value)}[{self.visit(node.slice)}]"

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Compare(self, node):
        [op] = node.ops
        [right] = node.comparators
        return f"{self.visit(node.left)} {operator_map[type(op)]} {self.visit(right)}"

    def visit_If(self, node):
        yield f"{self.Keywords.IF} {self.visit(node.test)} {self.Keywords.THEN}"
        yield from self.indent_all(self.visit_all(node.body))
        if node.orelse:
            yield Keywords.ELSE
            yield from self.indent_all(self.visit_all(node.orelse))
        if self.Keywords.ENDIF is not None:
            yield self.Keywords.ENDIF

    def visit_While(self, node):
        yield f"{self.Keywords.WHILE} {self.visit(node.test)} {self.Keywords.REPEAT}"
        yield from self.indent_all(self.visit_all(node.body))
        if self.Keywords.ENDWHILE is not None:
            yield self.Keywords.ENDWHILE

    def visit_Return(self, node):
        yield f"{self.Keywords.RETURN} {self.visit(node.value)}"

    def indent(self, line):
        return " " * 4 + line

    def indent_all(self, lines):
        for line in lines:
            yield self.indent(line)

    def generic_visit(self, node):
        raise NotImplementedError(node)


def ast_to_pseudocode(source_ast, **kwargs):
    return "\n".join(Visitor(**kwargs).visit(source_ast)) + "\n"


def source_to_pseudocode(source, **kwargs):
    return ast_to_pseudocode(ast.parse(source), **kwargs)


def main():
    import argparse
    import py2pc_i18n

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Python file to convert")
    parser.add_argument("--language", "-l", choices=list(py2pc_i18n.lang.keys()))
    args = parser.parse_args()

    kwargs = {}
    if args.language is not None:
        kwargs.update(Keywords=py2pc_i18n.lang[args.language])

    with open(args.file) as f:
        source = f.read()
    print(source_to_pseudocode(source, **kwargs), end="")


if __name__ == "__main__":
    main()
