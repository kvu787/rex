#!/usr/bin/python3

import sys

from node_rex import NodeRex as Rex

usage = """rex [-h] pattern

Rex reads standard input and prints the lines that can be produced from the
given regular expression pattern."""

def main():
    if not(len(sys.argv) == 2 or len(sys.argv) == 3):
        print("wrong number of arguments") # this should to go stderr
        return

    if sys.argv[1] == '-h':
        print(usage)
        return

    pattern = sys.argv[1]

    try:
        rex = Rex.from_string(pattern)
        for line in sys.stdin:
            # chop newline
            if line[-1] == '\n':
                line = line[:len(line)-1]
            if rex.match(line):
                print(line)
    except ValueError:
        print("invalid pattern")

if __name__ == '__main__':
    main()
