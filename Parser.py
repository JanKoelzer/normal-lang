import re

class Parser:
    @staticmethod
    def parse(code: str):
        '''
            Parse the source code, i.e. a number, of the form [+]?[1-9][0-9]*, possibly surrounded by whitespace.
            Every natural number is syntactically valid, for example 1, 2, 45, +789. 
        '''
  
        match = re.fullmatch(r"\s*\+?([1-9][0-9]*)\s*", code)

        if match is None:
            raise SyntaxError("Invalid code syntax. Your code should match [1-9][0-9]*")         

        return int(match.group(1)) 

