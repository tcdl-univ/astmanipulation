from ast import *
from ast_pprint import parseprint

method = """def bleh():
   return 2

def blah(a):
 return a
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
       new_node = Return(value = Str(s="Hello World!!!"))
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
print(ctx['blah'](1))