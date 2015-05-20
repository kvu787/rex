class Rex(object):
    """Represents a regular expression ('Rex') from formal language theory.

    'Rex' is an interface class that provides methods to construct and
    compose regular expressions.
    These regular expressions can be used to analyze text.
    'Rex' is an immutable class.

    See http://en.wikipedia.org/wiki/Regular_expression for more background
    on regular expressions.
    """

    @classmethod
    def from_string(cls, strng):
        """Creates a 'Rex' out of a string describing a regular expression.
        
        Args:
            strng: A string representation of a regular expression. See the
                   documentation for the 'parse' function for the format.

        Returns:
            A 'Rex' object.

        Raises:
            ValueError: If 'strng' does not represent a valid regular
                        expression.
        """
        
        raise NotImplementedError('Rex.from_string')

    @classmethod
    def from_ast(cls, ast):
        """Creates a 'Rex' out of an abstract syntax tree (AST) describing a regular expression.
        
        Args:
            ast: An AST representation of a regular expression in the form of a
            'tuple'. See the documentation for the 'parse' function for the
            format.

        Returns:
            A 'Rex' object.

        Assumes:
            'ast' is a valid AST for a regular expression as specified in the
            return value for the 'parse' function
        """
        if type(ast) != tuple:
            raise ValueError()

        if len(ast) == 1:
            return cls.from_character(ast[0])
        else:
            operation = ast[0]
            if operation == 'concat':
                return cls.from_ast(ast[1]).concat(cls.from_ast(ast[2]))
            elif operation == 'altern':
                return cls.from_ast(ast[1]).altern(cls.from_ast(ast[2]))
            elif operation == 'star':
                return cls.from_ast(ast[1]).star()

    @classmethod
    def from_character(cls, char):
        """Creates a 'Rex' out of a single character.
        
        Args:
            char: A string of length 1, or 0 for the empty string. 

        Returns:
            A 'Rex' object.

        Raises:
            ValueError: If 'char' is not a valid string character.
        """

    def match(self, strng):
        """Returns True if this 'Rex' can produce 'strng'."""
        
        raise NotImplementedError('Rex.match')

    def concat(self, other):
        """Returns a 'Rex' that is the concatenation of 'this' and 'other'."""
        
        raise NotImplementedError('Rex.concat')

    def altern(self, other):
        """Returns a 'Rex' that is the alternation of 'this' and 'other'."""
        
        raise NotImplementedError('Rex.from_string')

    def star(self):
        """Returns a 'Rex' that is the Kleene star (optional repetition) of 'this'."""

        raise NotImplementedError('Rex.from_string')

def parse(strng):
    """Parses a regular expression string into an abstract syntax tree.

    Args:
        strng: A string representation of a regular expression.

        The grammar for a regular expression is:

        regex = regex regex
                regex "|" regex
                regex "*"
                "(" regex ")"
                escape_sequence
                non_meta_character
        escape_sequence = "\|" | "\*" | "\(" | "\)" | "\\"
        non_meta_character = any character other than * | ( ) \

        Note that the grammar does not include the empty string.

    Returns:
        The abstract syntax tree representation of the string. The AST is a
        tuple of the form:

        AST = ("concat", AST, AST)
              ("altern", AST, AST)
              ("star", AST)
              (terminal character, )

        The AST may contain empty strings as terminal symbols.

        If 'strng' cannot be parsed into a valid regular expression,
        returns None.
    """
    assert type(strng) == str

    # reject empty strings
    if len(strng) == 0:
        return None

    # try concat
    for i in range(1, len(strng)):
        first = parse(strng[:i])
        second = parse(strng[i:])
        if (first is not None) and (second is not None):
            return ('concat', first, second)

    # try altern
    for i in find_all(strng, '|'):
        first = parse(strng[:i])
        second = parse(strng[i+1:])
        if (first is not None) and (second is not None):
            return ('altern', first, second)

    # try star
    body = strng[:len(strng)-1]
    last = strng[len(strng)-1]
    if (last == '*') and (parse(body) is not None):
        return ('star', parse(body))

    # try parens
    if len(strng) >= 3:
        first = strng[0]
        last = strng[len(strng)-1]
        if first == '(' and last == ')':
            return parse(body[1:len(strng)-1])

    if len(strng) == 1:
        # must be non-meta character
        if strng in '*|()\\':
            return None
        else:
            return (strng,)
    elif len(strng) == 2:
        # must be escaped meta character
        if strng[0] == '\\' and strng[1] in '*|()\\':
            return (strng[1],)
        else:
            return None
    else:
        return None

def find_all(strng, c):
    assert type(strng) == str

    retval = []
    for i in range(len(strng)):
        if strng[i] == c:
            retval.append(i)
    return retval
