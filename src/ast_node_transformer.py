import __builtin__
from ast import *
import compileall
import sys
import traceback
import itertools
from ast_report import *

class RewriteInterpolation(NodeTransformer):
    def __init__(self, filename):
        self.filename = filename
        self.enter_linenos = {}  # id -> (lineno, col_offset)
        self.reach_linenos = {}  # id -> (lineno, col_offset)
        self.counter = itertools.count()
    def visit_Module(self, module_node):
        body_future = []
        body_rest = []
        for node in module_node.body:
            node = self.visit(node)
            if (not body_rest and isinstance(node, ImportFrom) and
                node.module == "__future__"):
                body_future.append(node)
            else:
                body_rest.append(node)

        import_line = parse("from ast_report import register_module, check_string").body[0]
        print ("ast_enter, ast_leave, ast_reached = register_module(%r, %r, %r)" %
               (self.filename, self.enter_linenos, self.reach_linenos))
        register_line = parse(
            "ast_enter, ast_leave, ast_reached = register_module(%r, %r, %r)" %
            (self.filename, self.enter_linenos, self.reach_linenos)).body[0]

        lineno = 1
        if body_future:
            lineno = body_future[0].lineno
        for new_node in (import_line, register_line):
            new_node.col_offset = 1
            new_node.lineno = lineno

        new_body = body_future + [import_line, register_line] + body_rest
        return Module(body=new_body)

    def track_enter_leave_lineno(self, node):
        node = self.generic_visit(node)
        id = next(self.counter)
        enter = parse("ast_enter[%d] += 1" % id).body[0]
        leave = parse("ast_leave[%d] += 1" % id).body[0]
        self.enter_linenos[id] = (node.lineno, node.col_offset)
        for new_node in (enter, leave):
            copy_location(new_node, node)

        n = Num(n=1)
        copy_location(n, node)
        if_node = If(test=n, body=[enter, node, leave], orelse=[])
        copy_location(if_node, node)
        return if_node

    visit_FunctionDef = track_enter_leave_lineno
    visit_ClassDef = track_enter_leave_lineno
    visit_Assign = track_enter_leave_lineno
    visit_AugAssign = track_enter_leave_lineno
    visit_Delete = track_enter_leave_lineno
    visit_Print = track_enter_leave_lineno
    visit_For = track_enter_leave_lineno
    visit_While = track_enter_leave_lineno
    visit_If = track_enter_leave_lineno
    visit_With = track_enter_leave_lineno
    visit_TryExcept = track_enter_leave_lineno
    visit_TryFinally = track_enter_leave_lineno
    visit_Assert = track_enter_leave_lineno
    visit_Import = track_enter_leave_lineno
    visit_ImportFrom = track_enter_leave_lineno
    visit_Exec = track_enter_leave_lineno
    #Global
    visit_Expr = track_enter_leave_lineno
    visit_Pass = track_enter_leave_lineno


    def track_reached_lineno(self, node):
        node = self.generic_visit(node)
        id = next(self.counter)
        reach = parse("ast_reached[%d] += 1" % id).body[0]
        self.reach_linenos[id] = (node.lineno, node.col_offset)
        copy_location(reach, node)

        n = Num(n=1)
        copy_location(n, node)
        if_node = If(test=n, body=[reach, node], orelse=[])
        copy_location(if_node, node)
        return if_node

    visit_Return = track_reached_lineno
    visit_Raise = track_reached_lineno
    visit_Break = track_reached_lineno
    visit_Continue = track_reached_lineno

old_compile = __builtin__.compile

def compile(source, filename, mode, flags=0):
    if flags == PyCF_ONLY_AST:
        return old_compile(source, filename, mode, flags)
    assert mode == "exec"
    #traceback.print_stack()
    code = open(filename).read()
    tree = parse(code, filename)
    tree = RewriteInterpolation(filename).visit(tree)
    code = old_compile(tree, filename, "exec")
    return code

__builtin__.compile = compile


filename = "../test/sample_py.py"
code = open(filename).read()
tree = parse(code, filename)
tree = RewriteInterpolation(filename).visit(tree)
code = old_compile(tree, filename, "exec")
exec(code, globals())

