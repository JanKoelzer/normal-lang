from Parser import Parser
from Tree import Application, LambdaX, LambdaY, IfStmt, X, Y, Numeral, Sum, Product
from PiDigitStream import Pi
import sys
import re


class Interpreter:
    def __init__(self, code, numbers = None):
        ''' Create an interpreter for the given source code.
            CODE is an offset in the digit stream (given as chars) provided by NUMBERS.
            If NUMBERS is omit, use the digits of PI.
        '''
        self._code = code
        if numbers is None:
            self._numbers = Pi.stream()
        else:
            self._numbers = numbers
        # _tree has not been set up yet, set to None
        self._tree = None

        
    def _read(self):
        '''
            Recursively build a tree by reading the digit stream.
            Returns a tree of nodes defined by Tree.Node.
            May diverge, if the digits appear inconveniently.
        '''
        # Note that productions are ordered sucht that a lot of
        # "useful" programs occur  among the first possible codes (0, 1, 2, 3, …)

        # Get the next number and map it to a production rule.
        # Then, _read() recursivly to complete the tree.
        n = int(next(self._numbers))

        rules = [
            # 0
            lambda: Application(self._read(), self._read()), 
            # 1
            lambda: Numeral(1),
            # 2
            lambda: LambdaX(self._read()),
            # 3
            lambda: LambdaY(self._read()),
            # 4
            lambda: Numeral(0),
            # 5
            lambda: X,
            # 6
            lambda: Y,
            # 7
            lambda: Sum(self._read(), self._read()),
            # 8
            lambda: Product(self._read(), self._read()),
            # 9
            lambda: IfStmt(self._read(), self._read(), self._read()),
        ]

        return rules[n]()

    def create_tree(self):
        '''
            Convert the source code into tree of nodes (see Tree.Node).
            Returns a lambda expression with variable x and a body defined by the digit stream, and source, naturally.
            May diverge, if the digits appear inconveniently.
        '''
        if self._tree is None:
            # the CODE is just the offset in the stream of digits
            # so skip the first value
            for _ in range(self._code - 1):
                next(self._numbers)

            # now parse following digits and surround it by a lambda
            self._tree = LambdaX(self._read())       
        
    def run(self, arg: int):
        '''
            Run the program defined by the source code passing ARG to it.
        '''
        if self._tree is None:
            self.create_tree()

        return Application(self._tree, Numeral(arg)).evaluate({})



if __name__ == '__main__':
    try:
        # parse the code
        code_str = sys.argv[1]
        code = Parser.parse(code_str)

        # parse an argument or use default "0"
        arg = int(sys.argv[2])

        # create an AST
        interpreter = Interpreter(code)
        interpreter.create_tree()
        print(f"{interpreter._tree}")

        # run the interpreter
        res = interpreter.run(arg)

        print(f"{interpreter._tree} {arg} => {res}")
    except IndexError as e:
        print(f"Please provide two integers: your code and your input argument. Usage: Interpreter.py 77 42, where 77 is your code an 42 is the argument.")
    except SyntaxError as e:
        print(e, f"Your code was '{code_str}'")
    except ValueError:
        print(f"Please provide an integer as input argument. Usage: Interpreter.py 77 42, where 77 is your code an 42 is the argument. Your argument was '{sys.argv[2]}'.")
 
