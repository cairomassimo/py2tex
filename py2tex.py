import ast
import contextlib


class Keywords:
    IF = r"\If{{\tt "
    THEN = "}}"
    ELSE = r"\Else%"
    ENDIF = r"\EndIf%"
    WHILE = r"\While{{\tt "
    REPEAT = "}}"
    ENDWHILE = r"\EndWhile%"
    BEGINASSIGN = r"\State{\tt "
    ENDASSIGN = "}"
    ASSIGN = r"$\gets$"
    BEGINRETURN = r"\State{\tt "
    RETURN = "restituisci"
    ENDRETURN = "}"
    FUNCTION = r"\Function{{\tt "
    ENDFUNCTION = r"\EndFunction%"


class CodeGen:
    def __init__(self):
        self._indentation = 0
        self._lines = []

    def line(self, line):
        self._lines.append((line, self._indentation))

    def _indented_lines(self):
        for line, indentation in self._lines:
            yield "  " * indentation + line + "\n"

    def to_string(self):
        return "".join(self._indented_lines())

    @contextlib.contextmanager
    def indent(self):
        self._indentation += 1
        yield
        self._indentation -= 1


class Py2Tex(ast.NodeVisitor, CodeGen):
    def visit_all(self, nodes):
        for node in nodes:
            self.visit(node)

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def body(self, body):
        with self.indent():
            self.visit_all(body)

    def make_annotation(self, a):
        if a is None:
            return ""
        return f": {a.s}"

    def arg(self, a):
        if a.annotation is None:
            return r"\PyArg{" + a.arg + "}"
        else:
            assert isinstance(a.annotation, ast.Str)
            return r"\PyArgAnnotation{" + a.arg + "}{" + a.annotation.s + "}"

    def expr(self, e):
        return r"\PyExpr{" + self.visit(e) + "}"

    def visit_FunctionDef(self, node):
        args = r" \PyArgSep ".join(self.arg(a) for a in node.args.args)
        decl = r"\PyFunction{" + node.name + "}{" + args + "}"
        self.line(r"\Function{" + decl + "}")
        self.body(node.body)
        self.line(r"\EndFunction%")

    def visit_Assign(self, node):
        targets = r" \PyAssignSep ".join(self.visit(target) for target in node.targets)
        assign = r"\PyAssign{" + targets + "}{" + self.expr(node.value) + "}"
        self.line(r"\State{" + assign + "}")

    def visit_Name(self, node):
        return r"\PyName{" + node.id + "}"

    def visit_Num(self, node):
        return r"\PyNum{" + str(node.n) + "}"

    def visit_BinOp(self, node):
        return self.visit(node.left) + r" \Py" + type(node.op).__name__ + " " + self.visit(node.right)

    def visit_UnaryOp(self, node):
        return r"\Py" + type(node.op).__name__ + "{" + self.visit(node.operand) + "}"

    def visit_Subscript(self, node):
        return r"\PySubscript{" + self.visit(node.value) + "}{" + self.visit(node.slice) + "}"

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Compare(self, node):
        result = self.visit(node.left)
        for op, right in zip(node.ops, node.comparators):
            result += r" \Py" + type(op).__name__ + " " + self.visit(right)
        return result

    def visit_If(self, node):
        self.line(r"\If{" + self.expr(node.test) + "}")
        self.body(node.body)
        if node.orelse:
            self.line(r"\Else%")
            self.body(node.orelse)
        self.line(r"\EndIf%")

    def visit_While(self, node):
        self.line(r"\While{" + self.expr(node.test) + "}")
        self.body(node.body)
        self.line(r"\EndWhile%")

    def visit_Return(self, node):
        self.line(r"\Return{" + self.expr(node.value) + "}")

    def generic_visit(self, node):
        raise NotImplementedError(node)


def ast_to_pseudocode(source_ast, **kwargs):
    return "\n".join(Py2Tex(**kwargs).visit(source_ast)) + "\n"


def source_to_pseudocode(source, **kwargs):
    return ast_to_pseudocode(ast.parse(source), **kwargs)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Python file to convert")
    args = parser.parse_args()

    with open(args.file) as f:
        source = f.read()

    py2tex = Py2Tex()
    py2tex.visit(ast.parse(source))

    print(py2tex.to_string(), end="")


if __name__ == "__main__":
    main()
