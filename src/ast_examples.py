from ast import *
import pprint

dumped_ast = dump(parse("for i in range(10): print i"))
pprint.pprint(dumped_ast)


tree = Module(body=[FunctionDef(name='bleh', args=arguments(args=[Name(id='a', ctx=Param())], vararg=None, kwarg=None, defaults=[]), body=[Expr(value=BinOp(left=Name(id='a', ctx=Load()), op=Add(), right=Num(n=1)))], decorator_list=[])])
tree.lineno = 1
tree.col_offset = 1
tree = fix_missing_locations(tree)
print(tree)

