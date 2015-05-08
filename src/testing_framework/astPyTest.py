import ast
from src.ast_pprint import parseprint
from types import *

class PyUnitAssertionError(AssertionError):
    pass


def assert_equal(a, b):
    if a != b:
        raise AssertionError("{0} is not equal to {1}".format(a, b))


def assert_not_equal(a, b):
    if a == b:
        raise AssertionError("{0} is actually equal to {1}".format(a, b))


test_namespace = {'assert_equal': assert_equal, 'assert_not_equal': assert_not_equal}


class AssertCmpTransformer(ast.NodeTransformer):
    """Transform 'assert a==b' into 'assert_equal(a, b)'
    """

    def generate_assert_equal(self, node):
        call = ast.Call(func=ast.Name(id='assert_equal', ctx=ast.Load()),
                        args=[node.test.left, node.test.comparators[0]],
                        keywords=[])
        return call

    def generate_assert_not_equal(self, node):
        call = ast.Call(func=ast.Name(id='assert_not_equal', ctx=ast.Load()),
                        args=[node.test.left, node.test.comparators[0]],
                        keywords=[])
        return call

    def visit_Assert(self, node):
        dispatch = {ast.Eq: self.generate_assert_equal, ast.NotEq: self.generate_assert_not_equal}
        if isinstance(node.test, ast.Compare) and \
                        len(node.test.ops) == 1:

            for key, value in dispatch.items():
                if isinstance(node.test.ops[0], key):
                    call = value(node)
                    # Wrap the call in an Expr node, because the return value isn't used.
                    newnode = ast.Expr(value=call)
                    ast.copy_location(newnode, node)
                    ast.fix_missing_locations(newnode)
                    return newnode
        # Return the original node if we don't want to change it.
        return node


class Runner(object):
    def __init__(self):
        self.reset_tests_results()

    def report(self):
        for result in self.results:
            result.report()

    def reset_tests_results(self):
        self.methods_to_run = []
        self.results = []

    def run_tests(self, file):
        self.parse_code(file)
        self.modify_tree()
        self.inspect_clases()

    def parse_code(self, filename):
        with open(filename) as f:
            code = f.read()
        self.ast_tree = ast.parse(code)
        self.code_lines = [None] + code.splitlines()

    def modify_tree(self):
        self.ast_tree = AssertCmpTransformer().visit(self.ast_tree)

    def inspect_clases(self):
        for node in self.ast_tree.body:
            if (isinstance(node, ast.ClassDef)):
                self.search_def_methods(node)
            if (isinstance(node, ast.Import)):
                self.import_node(node)
        self.execute_tests()

    def import_node(self, node):
        wrapper = ast.Module(body=[node])
        co = compile(wrapper, '<string>', 'exec')
        exec(co, globals(), test_namespace)

    def search_def_methods(self, class_node):
        for node in class_node.body:
            if (isinstance(node, ast.FunctionDef)):
                if (self.is_method(node.name)):
                    newnode = ast.arguments(args=[], vararg=None, kwarg=None, defaults=[])
                    ast.copy_location(newnode, node.args)
                    node.args = newnode
                    self.methods_to_run.append(node)

    def is_method(self, method_name):
        return method_name.startswith('test_')

    def execute_test(self, test_node):
        test_name = test_node.name
        wrapper = ast.Module(body=[test_node])
        try:
            co = compile(wrapper, '<string>', 'exec')
            exec(co, test_namespace)
            test_namespace[test_name]()
            self.results.append(SuccessFulResult(test_name))
        except AssertionError as e:
            self.results.append(FailedResult(test_name, e, test_node.lineno, self.code_lines[test_node.lineno]))
        except Exception as e:
            self.results.append(ErrorResult(test_name, e, test_node.lineno, self.code_lines[test_node.lineno]))

    def execute_tests(self):
        for test in self.methods_to_run:
            self.execute_test(test)

class Result(object):
    def report(self):
        pass

class SuccessFulResult(Result):
    def __init__(self, test_name):
        self.test_name = test_name

    def report(self):
        print('Test {0} run successfully'.format(self.test_name))

class FailedResult(Result):
    def __init__(self, test_name, exception, lineno, message):
        self.test_name = test_name
        self.exception = exception
        self.lineno = lineno
        self.message = message

    def report(self):
        print("{0} Failed:{1} on line {2}".format(self.test_name, self.message, self.lineno))
        print("Cause: {0}".format(self.exception))

class ErrorResult(Result):
    def __init__(self, test_name, exception, lineno, message):
        self.test_name = test_name
        self.exception = exception
        self.lineno = lineno
        self.message = message

    def report(self):
        print("{0} Errored:{1} on line {2}".format(self.test_name, self.message, self.lineno))
        print("Cause: {0}".format(self.exception))