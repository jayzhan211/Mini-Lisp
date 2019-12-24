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


class Environment(dict):
    def __init__(self, symbol_names=None, symbol_values=None, outer=None):
        super(Environment, self).__init__()
        if symbol_names is None:
            symbol_names = tuple()
            symbol_values = tuple()
        self.update(zip(symbol_names, symbol_values))
        self.outer = outer

    def find(self, name):
        logging.debug('self: {}'.format(self))
        if name not in self and self.outer is None:
            raise NameError('{} is not founded'.format(name))
        return self if name in self else self.outer.find(name)


class GlobalEnvironment(Environment):
    def __init__(self):
        super(GlobalEnvironment, self).__init__()
        self.update({
            'print_num': print,
            'print_bool': lambda x: print('#t' if x else '#f'),
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
        return reduce(lambda x, y: x == y, args)

    def and_op(self, *args):
        self.type_checker(bool, args)
        return all(args)

    def or_op(self, *args):
        self.type_checker(bool, args)
        return any(args)

    def not_op(self, arg):
        self.type_checker(bool, arg)
        return not arg

    @staticmethod
    def type_checker(dtype, args):
        for arg in args:
            if type(arg) != dtype:
                raise TypeError('Expect {} but got {}'.format(dtype, type(arg)))


def interpret_AST(node, environment=None):
    logging.debug('node: {}'.format(node))
    logging.debug('type(node): {}'.format(type(node)))

    if environment is None:
        environment = GlobalEnvironment()

    try:  # convert SIGNED_INT to int
        return int(node)
    except (TypeError, ValueError):
        # convert '#t' to Python True
        if node == '#t':
            return True

        # convert '#f' to Python False
        if node == '#f':
            return False

        if isinstance(node, str):
            logging.debug('node: {} is str'.format(node))
            return environment.find(node)[node]

        logging.debug('node.data: {}'.format(node.data))

        if node.data == 'program':
            result = list()
            for child in node.children:
                res = interpret_AST(child, environment)
                if res is not None:
                    result.append(res)
            return result
        else:
            logging.debug('type(node): {}'.format(type(node)))
            logging.debug('node.data: {}'.format(node.data))
            logging.debug('node.children: {}'.format(node.children))
            proc = interpret_AST(node.data, environment)
            args = tuple(interpret_AST(expr, environment)
                         for expr in node.children)
            return proc(*args)
