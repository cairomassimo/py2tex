import ast
import contextlib


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
    def __init__(self):
        super().__init__()
        self._emit_tex = True

    def visit(self, node):
        result = super().visit(node)
        if result is None:
            return ""
        return result

    def visit_all(self, nodes):
        for node in nodes:
            self.visit(node)

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def body(self, body):
        with self.indent():
            self.visit_all(body)

    def arg(self, a):
        if a.annotation is None:
            return r"\PyArg{" + a.arg + "}"
        else:
            assert isinstance(a.annotation, ast.Str)
            return r"\PyArgAnnotation{" + a.arg + "}{" + a.annotation.s + "}"

    def expr(self, e):
        return r"\PyExpr{" + self.visit(e) + "}"

    def visit_FunctionDef(self, node):
        if not self._emit_tex:
            return
        args = r"\PyArgSep".join(self.arg(a) for a in node.args.args)
        if node.returns:
            self.line(r"\Function{" + node.name + "}{" + args +
                      r"}{ $\rightarrow$ \texttt{" + node.returns.s + "}}")
            self.body(node.body)
            self.line(r"\EndFunction%")
        else:
            self.line(r"\Procedure{" + node.name + "}{" + args + "}")
            self.body(node.body)
            self.line(r"\EndProcedure%")

    def visit_Assign(self, node):
        if not self._emit_tex:
            return
        targets = r" \PyAssignSep ".join(
            self.visit(target) for target in node.targets)
        assign = r"\PyAssign{" + targets + "}{" + self.expr(node.value) + "}"
        self.line(r"\State{" + assign + "}")

    def visit_AnnAssign(self, node):
        if not self._emit_tex:
            return

        target = self.visit(node.target)

        assert isinstance(node.annotation, ast.Str)
        assert node.value == None

        assign = r"\PyAnnotation{" + target + "}{" + node.annotation.s + "}"

        self.line(r"\State{" + assign + "}")

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str):
            self.handle_magic_string(node.value.s)
            return
        if not self._emit_tex:
            return
        self.line(r"\State{" + self.expr(node.value) + "}")

    def handle_magic_string(self, s: str):
        if s.startswith("!tex\n"):
            for l in s.splitlines()[1:]:
                self.line(l)
        elif s == "!show":
            self._emit_tex = True
        elif s == "!hide":
            self._emit_tex = False
        else:
            self.line(r"\Comment{" + s + "}")

    def visit_Str(self, node):
        return r"\PyStr{" + node.s + "}"

    def visit_Name(self, node):
        return r"\PyName{" + node.id + "}"

    def visit_Num(self, node):
        return r"\PyNum{" + str(node.n) + "}"

    def visit_NameConstant(self, node):
        return r"\Py" + str(node.value)

    def visit_BoolOp(self, node):
        return (r" \Py" + type(node.op).__name__ + " ").join(self.visit(v) for v in node.values)

    def visit_Call(self, node):
        assert isinstance(node.func, ast.Name)
        if node.func.id == "_":
            assert len(node.args) == 1
            [arg] = node.args
            return r"\PyPar{" + self.visit(arg) + "}"
        return r"\PyCall{" + node.func.id + "}" + "{" + r" \PyCallSep ".join(self.visit(a) for a in node.args) + "}"

    def visit_For(self, node):
        if not self._emit_tex:
            return

        assert isinstance(node.iter, ast.Call)
        assert isinstance(node.iter.func, ast.Name)

        nargs = len(node.iter.args)
        args = map(self.visit, node.iter.args)
        assert 1 <= nargs <= 3
        if nargs == 1:
            start = 0
            [stop] = args
            step = 1
        if nargs == 2:
            [start, stop] = args
            step = 1
        if nargs == 3:
            [start, stop, step] = args

        variable = self.visit(node.target)

        self.line(
            r"\PyFor" + "".join("{" + x + "}" for x in [variable, start, stop, step]))
        self.body(node.body)
        self.line(r"\EndPyFor")

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
        if not self._emit_tex:
            return
        self.line(r"\If{" + self.expr(node.test) + "}")
        self.body(node.body)
        if node.orelse:
            self.line(r"\Else%")
            self.body(node.orelse)
        self.line(r"\EndIf%")

    def visit_While(self, node):
        if not self._emit_tex:
            return
        self.line(r"\While{" + self.expr(node.test) + "}")
        self.body(node.body)
        self.line(r"\EndWhile%")

    def visit_Return(self, node):
        if not self._emit_tex:
            return
        self.line(r"\Return{" + self.expr(node.value) + "}")

    def visit_List(self, node):
        elts = r" \PyListSep ".join(self.visit(el) for el in node.elts)
        return r"\PyList{" + elts + "}"


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
