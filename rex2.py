class Rex(tuple):
    @classmethod
    def from_character(cls, char):
        assert type(char) == str
        assert len(char) == 0 or len(char) == 1

        return cls((char,))

    def run(self, s):
        assert type(s) == str

        return '' in self.__run(s)

    def concat(self, other):
        assert type(other) == Rex

        return Rex(('and', self, other))

    def altern(self, other):
        assert type(other) == Rex

        return Rex(('or', self, other))

    def star(self):
        return Rex(('star', self))

    """
    returns set of suffixes such
    - that there exists some prefix
    - nfa matches prefix
    - prefix + suffix = s

    note that the empty set means that this rex cannot match any prefix of s
    """
    def __run(self, s):
        if len(self) == 1:
            char = self[0]
            if s == '':
                if char == '':
                    return [s]
                else:
                    return []
            else:
                if char == '':
                    return [s]
                elif char == s[0]:
                    return [s[1:]]
                else:
                    return []
        else:
            op = self[0]
            if op == 'and':
                _, rex1, rex2 = self
                result = []
                for suffix1 in rex1.__run(s):
                    for suffix2 in rex2.__run(suffix1):
                        result.append(suffix2)
                return result
            elif op == 'or':
                _, rex1, rex2 = self
                return rex1.__run(s) + rex2.__run(s)
            elif op == 'star':
                result = [s]
                _, rex = self
                current_rex = rex
                while True:
                    suffixes = current_rex.__run(s)
                    if len(suffixes) == 0:
                        break
                    else:
                        result += suffixes
                        current_rex = current_rex.concat(rex)
                return result

if __name__ == '__main__':
    main()
