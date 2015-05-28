# rex

`rex` contains libraries and tools for using regular expressions.

## Usage

### As a Python library

`rex.py` is an abstract class that specifies the `Rex` regular expression
class. `node_rex.py` and `tuple_rex.py` are implementations of `Rex`. Import
an implementation of `Rex` as follows:

```
from node_rex import NodeRex as Rex
```

or

```
from tuple_rex import TupleRex as Rex
```

### As a Python command line tool

`rex` is a Python script built with `Rex`. See its usage by running:

```
python rex -h
```
