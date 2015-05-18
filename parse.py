"""
Parses a string representation of a regular expression into an abstract
syntax tree.

The metacharacters are: * | ( ) \
Metacharacters can be escaped with \ like \* and \(. \\ is an escaped backslash.

Returns
- Abstract syntax tree if s is valid regular expression
- None if s is not a valid regular expression
"""
def parse(s):
    """
    grammar:
    rex = rex rex
          rex "|" rex
          rex "*"
          "(" rex ")" 
          character
    """
    assert type(s) == str

    # reject empty strings
    if len(s) == 0:
        return None

    # try concat
    for i in range(1, len(s)):
        first = parse(s[:i])
        second = parse(s[i:])
        if (first is not None) and (second is not None):
            return ('concat', first, second)

    # try altern
    for i in find_all(s, '|'):
        first = parse(s[:i])
        second = parse(s[i+1:])
        if (first is not None) and (second is not None):
            return ('altern', first, second)

    # try star
    body = s[:len(s)-1]
    last = s[len(s)-1]
    if (last == '*') and (parse(body) is not None):
        return ('star', parse(body))

    # try parens
    if len(s) >= 3:
        first = s[0]
        last = s[len(s)-1]
        if first == '(' and last == ')':
            return parse(body[1:len(s)-1])

    if len(s) == 1:
        # must be non-meta character
        if s in '*|()\\':
            return None
        else:
            return s
    elif len(s) == 2:
        # must be escaped meta character
        if s[0] == '\\' and s[1] in '*|()\\':
            return s[1]
        else:
            return None
    else:
        return None

def find_all(s, c):
    assert type(s) == str

    retval = []
    for i in range(len(s)):
        if s[i] == c:
            retval.append(i)
    return retval
