from Tree import Application, LambdaX, LambdaY, IfStmt, X, Y, Numeral, Sum, Product
from PiDigitStream import Pi
import sys


class Interpreter:
    def __init__(self, code, numbers = None):
        self._code = code
        if numbers is None:
            self._numbers = Pi.stream()
        else:
            self._numbers = numbers
        self._tree = None

        
    def _read(self):
        n = int(next(self._numbers))
        if n == 1:  # DONE
            return Application(self._read(), self._read())
        elif n == 2: # DONE
            return LambdaY(self._read())
        elif n == 3:
            return LambdaX(self._read())
        elif n == 4:
            return Numeral(1)
        elif n == 5: # DONE
            return Numeral(0) # DONE
        elif n == 6: # DONE
            return Y
        elif n == 7:
            return IfStmt(self._read(), self._read(), self._read())
        elif n == 8:
            return Sum(self._read(), self._read())
        elif n == 9: # DONE
            return X
        else:
            return Product(self._read(), self._read())

    def create_tree(self):
        if self._tree is None:
            # the CODE is just the offset in the stream of digits
            # so skip the first value
            for _ in range(self._code):
                next(self._numbers)

            # now parse following digits and surround it by a lambda
            self._tree = LambdaX(self._read())       
        

    def run(self, arg: int):
        if self._tree is None:
            self.create_tree()

        return Application(self._tree, Numeral(arg)).evaluate({})



if __name__ == '__main__':
    try:        
        code = int(sys.argv[1])
        print(code)
    except:
        raise SyntaxError("Invalid code syntax")         

    try:
        arg = int(sys.argv[2])
    except:        
        arg = 0

    interpreter = Interpreter(code)
    interpreter.create_tree()
    print(f"{interpreter._tree}")
    
    res = interpreter.run(arg)

    print(f"{interpreter._tree} {arg} => {res}")
 
