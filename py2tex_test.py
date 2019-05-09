import py2tex
import functools
import inspect
import ast

assign = py2tex.Keywords.ASSIGN

def expected_pseudocode(pseudocode):
    def decorator(f):
        @functools.wraps(f)
        def wrapped():
            source = inspect.getsource(f)
            [function_def] = ast.parse(source).body
            module_ast = ast.Module(function_def.body)

            assert py2tex.ast_to_pseudocode(module_ast).strip() == pseudocode.strip()
        
        return wrapped

    return decorator

@expected_pseudocode(f"a <- 1")
def test_assign():
    a = 1

@expected_pseudocode(f"i <- i + 1")
def test_add():
    i = i + 1

@expected_pseudocode(f"i <- i - 1")
def test_sub():
    i = i - 1

@expected_pseudocode(f"i <- -i")
def test_unary():
    i = -i

@expected_pseudocode(f"""
if a = b then
    i <- 1
""")
def test_if():
    if a == b:
        i = 1

@expected_pseudocode(f"""
if a = b then
    i <- 1
else
    i <- 2
""")
def test_if_else():
    if a == b:
        i = 1
    else:
        i = 2


@expected_pseudocode(f"""
    a[i] <- 3
""")
def test_subscript():
    a[i] = 3


@expected_pseudocode(f"""
i <- 1
while i < 10 repeat
    i <- i + 1
end
""")
def test_while():
    i = 1
    while i < 10:
        i = i + 1
