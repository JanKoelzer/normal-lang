from typing import Dict, List


class EvaluationException(Exception):
    ''' Indicates some error while evaluating a term. '''
    pass

class UnboundVarException(EvaluationException):
    ''' Indicates that a variable should be resolved while it is not defined/in scope. '''
    def __init__(self, symbol):
        super().__init__(f"Undefined variable {symbol}")

class UnevaluatedArgumentException(EvaluationException):
    ''' Indicates that an argument to a lambda has not been evaluated to a value (lambda or numeral). Note: This is call by value. '''
    def __init__(self, arg):
        super().__init__(f"Argument must be a value but is {arg}")

class NotCallableException(EvaluationException):
    ''' Indicates that the left hand side of an application is not (evaluated to )a lambda expression and cannot be called. '''
    def __init__(self, func):
        super().__init__(f"{func} is not callable.")

class BinOpOperandException(EvaluationException):
    ''' Indicates that a binary operation should operate on something that is not a number. '''
    def __init__(self, opSymbol, pos, arg):
        if pos == 0:
            posStr = "First"
        else:
            posStr = "Second"
        super().__init__(f"{posStr} argument of {opSymbol} is not a number: {arg}")

class Node:
    ''' This abstract class represents any node of the syntax tree '''
    def __init__(self, *children: "Node"):
        self._children: List[Node] = list(children)

    def is_value(self) -> bool:
        return False

    def evaluate(self, ctx: Dict[str, "Node"]) -> "Node":
        raise NotImplementedError()

    def parse(self, pi) -> "Node":
        raise NotImplementedError()

    def debug(self, ctx):
        # print(f"Evaluating {self} with ctx={ctx}")
        pass


class Numeral(Node):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def evaluate(self, ctx):
        self.debug(ctx)
        return self

    def is_value(self):
        return True

    def __str__(self):
        return str(self.value)


class Var(Node):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def evaluate(self, ctx):
        self.debug(ctx)
        if self.symbol not in ctx:
            raise UnboundVarException(self.symbol)
        return ctx[self.symbol]


    def __str__(self):
        return self.symbol

# Convenience variables
X = Var("x")
Y = Var("y")
F = Var("f")



class Lambda(Node):
    def __init__(self, param: Var, body: Node):
        super().__init__(body)
        self.param = param.symbol
        self._closure = None

    def evaluate(self, ctx):
        # return a closure (copy of this lambda with its context captured)
        result = Lambda(
            Var(self.param),
            self._children[0]
        )
        result._closure = ctx.copy()
        return result

    def call(self, arg: Node):
        if not arg.is_value():
            raise UnevaluatedArgumentException(arg)

        new_ctx = self._closure.copy() | { self.param: arg }

        return self._children[0].evaluate(new_ctx)

    def is_value(self):
        return True

    def __str__(self):
        return f"(λ{self.param}.{self._children[0]})"


class LambdaX(Lambda):
    def __init__(self, body):
        super().__init__(X, body)

class LambdaY(Lambda):
    def __init__(self, body):
        super().__init__(Y, body)
class LambdaF(Lambda):
    def __init__(self, body):
        super().__init__(F, body)

class Application(Node):
    def evaluate(self, ctx):
        self.debug(ctx)

        func = self._children[0].evaluate(ctx)
        if not isinstance(func, Lambda):
            raise NotCallableException(func)

        arg = self._children[1].evaluate(ctx)

        return func.call(arg)

    def __str__(self):
        return f"({self._children[0]} {self._children[1]})"



class IfStmt(Node):
    def evaluate(self, ctx):
        self.debug(ctx)

        cond = self._children[0].evaluate(ctx)

        branch = 1 if not isinstance(cond, Numeral) or cond.value != 0 else 2
        return self._children[branch].evaluate(ctx)

    def __str__(self):
        return "(if {} then {} else {})".format(*self._children[0:3])


class BinOp(Node):  
    def op(self, a, b):
        raise NotImplementedError()

    
    def evaluate(self, ctx):
        self.debug(ctx)

        a = self._children[0].evaluate(ctx)

        if not isinstance(a, Numeral):
            raise BinOpOperandException(self._opSymbol, 0, a)

        b = self._children[1].evaluate(ctx)
        if not isinstance(b, Numeral):
            raise BinOpOperandException(self._opSymbol, 1, b)

        return Numeral(self.op(a.value, b.value))

    def __str__(self):
        return f"({self._children[0]} {self._opSymbol} {self._children[1]})"


class Sum(BinOp):
        _opSymbol = "+"      

        def op(self, a, b):
            return a + b


class Product(BinOp):
        _opSymbol = "*"

        def op(self, a, b):
            return a * b


