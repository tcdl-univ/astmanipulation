from ast import *
import pprint
from ast_pprint import parseprint

code = """import antigravity
for i in range(10): print i"""
ast = parse(code)
dumped_ast = dump(ast)
#pprint.pprint(parseprint(code))
#pprint.pprint(dumped_ast)


tree = Module(body=[FunctionDef(name='bleh', args=arguments(args=[Name(id='a', ctx=Param())], vararg=None, kwarg=None, defaults=[]), body=[Expr(value=BinOp(left=Name(id='a', ctx=Load()), op=Add(), right=Num(n=1)))], decorator_list=[])])
tree.lineno = 1
tree.col_offset = 1
tree = fix_missing_locations(tree)
#print(tree)


#Ejemplo de modificar el ast

method = """def bleh():
    return 2
"""
my_ast = parse(method)
parseprint(method)
# <_ast.Module object at 0x7ff921554e90>
# Module(body=[
#     FunctionDef(name='bleh', args=arguments(args=[], vararg=None, kwarg=None, defaults=[]), body=[
#         Return(value=Num(n=2)),
#       ], decorator_list=[]),
#   ])

class ReturnTransformer(NodeTransformer):

    def visit_Return(self, node):
        new_node = Return(value = Str(s="Hello World"))
        fix_missing_locations(new_node)
        return new_node


new_ast = ReturnTransformer().visit(my_ast)
parseprint(new_ast)
compiled_code = compile(new_ast, '<string>', 'exec')

#Si no ejecutamos antes de compilar el nodo que se modifico y se agrego al AST
# Traceback (most recent call last):
#   File "/home/ernesto/dev/astmanipulation/src/ast_examples.py", line 44, in <module>
#     compiled_code = compile(new_ast, '<string>', 'exec')
# TypeError: required field "lineno" missing from stmt

ctx = {}
exec(compiled_code, globals(), ctx)
print(ctx['bleh']())