import logging
from functools import reduce
from lark import Lark, UnexpectedInput, UnexpectedToken, UnexpectedCharacters


class Interpreter:
    def __init__(self):
        self.tree = None
        with open('grammar.lark') as larkfile:
            self.parser = Lark(larkfile, start='program', parser='lalr', lexer='contextual')

    def interpret(self, code):
        try:
            self.tree = self.parser.parse(code)
        except (UnexpectedInput, UnexpectedToken, UnexpectedCharacters):
            raise SyntaxError('Mini-lisp syntax error.')
        else:
            return interpret_AST(self.tree)


# class Table(dict):
#     def __init__(self, symbol_names=None, symbol_values=None, outer=None):
#         super(Table, self).__init__()
#         if symbol_names is None:
#             symbol_names = tuple()
#             symbol_values = tuple()
#         self.update(zip(symbol_names, symbol_values))
#         self.outer = outer
class Table(dict):
    def __init__(self):
        super(Table, self).__init__()
        self.update({
            'print_num': self.print_num,
            'print_bool': self.print_bool,
            'plus': self.plus,
            'minus': self.minus,
            'multiply': self.multiply,
            'divide': self.divide,
            'modulus': self.modulus,
            'greater': self.greater,
            'smaller': self.smaller,
            'equal': self.equal,
            'and_op': self.and_op,
            'or_op': self.or_op,
            'not_op': self.not_op
        })

    def print_bool(self, *args):
        self.type_checker(bool, args)
        print(['#f', '#t'][args[0]])

    def print_num(self, *args):
        self.type_checker(int, args)
        print(*args)

    def plus(self, *args):
        logging.debug(args)
        self.type_checker(int, args)
        return sum(args)

    def minus(self, *args):
        self.type_checker(int, args)
        return args[0] - args[1]

    def multiply(self, *args):
        self.type_checker(int, args)
        return reduce(lambda x, y: x * y, args)

    def divide(self, *args):
        self.type_checker(int, args)
        return args[0] // args[1]

    def modulus(self, *args):
        self.type_checker(int, args)
        return args[0] % args[1]

    def greater(self, *args):
        self.type_checker(int, args)
        return args[0] > args[1]

    def smaller(self, *args):
        self.type_checker(int, args)
        return args[0] < args[1]

    def equal(self, *args):
        self.type_checker(int, args)
        return args.count(args[0]) == len(args)

    def and_op(self, *args):
        self.type_checker(bool, args)
        return all(args)

    def or_op(self, *args):
        self.type_checker(bool, args)
        return any(args)

    def not_op(self, *arg):
        self.type_checker(bool, arg)
        return not arg

    @staticmethod
    def type_checker(dtype, args):
        logging.debug('type-checker => args: {}'.format(args))
        for arg in args:
            if type(arg) != dtype:
                raise TypeError('Expect {} but got {}'.format(dtype, type(arg)))

    def find(self, name):
        if name not in self:
            raise NameError('{} is not founded'.format(name))
        return self

    def add_define(self, symbol_names=None, symbol_values=None):
        self.update(zip(symbol_names, symbol_values))


class Function:
    def __init__(self, args, body, environment=None):
        if environment is None:
            environment = Table()
        self.args = args
        self.body = body
        self.environment = environment

    def __call__(self, *params):
        table = self.environment
        table.add_define(self.args, params)
        return interpret_AST(self.body, table)


def interpret_AST(node, environment=None):
    if environment is None:
        environment = Table()

    try:
        return int(node)
    except (TypeError, ValueError):
        if node == '#t':
            return True

        if node == '#f':
            return False

        if isinstance(node, str):
            return environment.find(node)[node]

        if node.data == 'program':
            result = list()
            for child in node.children:
                res = interpret_AST(child, environment)
                if res is not None:
                    result.append(res)
            return result
        elif node.data == 'if_exp':
            (test, then, els) = node.children
            test_res = interpret_AST(test, environment)
            if not isinstance(test_res, bool):
                raise TypeError("Expect 'boolean' but got 'number'.")
            expr = [els, then][test_res]
            return interpret_AST(expr, environment)
        elif node.data == 'def_stmt':
            logging.debug('def_stmt => node.children: {}'.format(node.children))
            (var, expr) = node.children
            environment[var] = interpret_AST(expr, environment)
        elif node.data == 'fun_exp':
            logging.debug('fun_exp => node.children: {}'.format(node.children))
            assert len(node.children) == 2
            args = interpret_AST(node.children[0], environment)
            body = interpret_AST(node.children[1], environment)
            return Function(args, body, environment)
        elif node.data == 'fun_ids':
            logging.debug('node.children: {}'.format(node.children))
            return node.children
        elif node.data == 'fun_body':
            logging.debug('fun_body => node.children: {}'.format(node.children))
            # def_stmts + expr
            for def_stmt in node.children[:-1]:
                interpret_AST(def_stmt, environment)
            return node.children[-1]
        elif node.data == 'fun_call':
            logging.debug('fun_call => node.children: {}'.format(node.children))
            func = interpret_AST(node.children[0], environment)
            params = tuple(interpret_AST(expr, environment)
                           for expr in node.children[1:])
            return func(*params)
        else:
            logging.debug('type(node): {}'.format(type(node)))
            logging.debug('node.data: {}'.format(node.data))
            logging.debug('node.children: {}'.format(node.children))
            func = interpret_AST(node.data, environment)
            args = tuple(interpret_AST(expr, environment)
                         for expr in node.children)
            logging.debug('proc -> args: {}'.format(args))
            return func(*args)
