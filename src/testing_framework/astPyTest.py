import ast


class PyUnitAssertionError(AssertionError):
    pass


def assert_equal(a, b):
    if a != b:
        raise AssertionError("{0} is not equal to {1}".format(a, b))


def assert_not_equal(a, b):
    if a == b:
        raise AssertionError("{0} is actually equal to {1}".format(a, b))


test_namespace = {'assert_equal': assert_equal, 'assert_not_equal': assert_not_equal}


class Runner(object):
    def report(self):
        pass

    def run_tests(self, file):
        self.parse_code(file)

    def parse_code(self, filename):
        with open(filename, encoding='utf-8') as f:
            code = f.read()
        self.ast_tree = ast.parse(code)
        self.code_lines = [None] + code.splitlines()
