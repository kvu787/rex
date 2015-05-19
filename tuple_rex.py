from rex import Rex, parse

class TupleRex(Rex):
    @classmethod
    def from_string(cls, strng):
        if type(strng) != str:
            raise ValueError()

        ast = parse(strng)
        if ast is None:
            raise ValueError()
        return TupleRex.from_ast(ast)

    @classmethod
    def from_ast(cls, ast):
        if type(ast) != tuple:
            raise ValueError()

        if len(ast) == 1:
            return TupleRex.from_character(ast[0])
        else:
            operation = ast[0]
            if operation == 'concat':
                return TupleRex.from_ast(ast[1]).concat(TupleRex.from_ast(ast[2]))
            elif operation == 'altern':
                return TupleRex.from_ast(ast[1]).altern(TupleRex.from_ast(ast[2]))
            elif operation == 'star':
                return TupleRex.from_ast(ast[1]).star()

    @classmethod
    def from_character(cls, char):
        assert type(char) == str
        assert len(char) == 0 or len(char) == 1

        return cls((char,))

    def match(self, strng):
        assert type(strng) == str

        return '' in self.__match(strng)

    def concat(self, other):
        assert type(other) == TupleRex

        return TupleRex(('concat', self, other))

    def altern(self, other):
        assert type(other) == TupleRex

        return TupleRex(('altern', self, other))

    def star(self):
        return TupleRex(('star', self))

    def __match(self, strng):
        """
        Returns set of suffixes such that for each suffix strng:
            There exists some prefix p such that:
                Regular expression matches p
                p + s = strng

        A set containing the empty string means that 'strng' was fully match.
        The empty set means that this regular expression cannot match any prefix
        of 'strng'.
        """
        tup = self.tup
        if len(tup) == 1:
            char = tup[0]
            if strng == '':
                if char == '':
                    return [strng]
                else:
                    return []
            else:
                if char == '':
                    return [strng]
                elif char == strng[0]:
                    return [strng[1:]]
                else:
                    return []
        else:
            op = tup[0]
            if op == 'concat':
                _, rex1, rex2 = tup
                result = []
                for suffix1 in rex1.__match(strng):
                    for suffix2 in rex2.__match(suffix1):
                        result.append(suffix2)
                return result
            elif op == 'altern':
                _, rex1, rex2 = tup
                return rex1.__match(strng) + rex2.__match(strng)
            elif op == 'star':
                result = [strng]
                _, rex = tup
                current_rex = rex
                while True:
                    suffixes = current_rex.__match(strng)
                    if len(suffixes) == 0:
                        break
                    else:
                        result += suffixes
                        current_rex = current_rex.concat(rex)
                return result

    def __init__(self, tup):
        self.tup = tup

if __name__ == '__main__':
    main()
