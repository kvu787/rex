from rex import Rex, parse

import copy

class NodeRex(Rex):
    @classmethod
    def from_string(cls, strng):
        if type(strng) != str:
            raise ValueError()

        ast = parse(strng)
        if ast is None:
            raise ValueError()
        return cls.from_ast(ast)

    @classmethod
    def from_character(cls, char):
        if type(char) != str:
            raise ValueError()
        if len(char) > 1:
            raise ValueError()

        final = Node(True, [])
        start = Node(False, [(char, final)])

        return cls(start, final)

    def match(self, strng):
        assert type(strng) == str

        return self.start.match(strng)

    def concat(self, other):
        assert type(other) == NodeRex

        self_copy = copy.deepcopy(self)
        other_copy = copy.deepcopy(other)
        self_copy.final.is_final = False
        self_copy.final.transitions.append(('', other_copy.start))
        new_start = self_copy.start
        new_final = other_copy.final

        return NodeRex(new_start, new_final)

    def altern(self, other):
        assert type(other) == NodeRex

        self_copy = copy.deepcopy(self)
        other_copy = copy.deepcopy(other)
        new_start = Node(
                False,
                [('', self_copy.start), ('', other_copy.start)])
        new_final = Node(True, [])
        self_copy.final.is_final = False
        other_copy.final.is_final = False
        self_copy.final.transitions.append(('', new_final))
        other_copy.final.transitions.append(('', new_final))

        return NodeRex(new_start, new_final)

    def star(self):
        self_copy = copy.deepcopy(self)
        new_final = Node(True, [])
        new_start = Node(False, [('', self_copy.start), ('', new_final)])
        self_copy.final.is_final = False
        self_copy.final.transitions.append(('', new_start))
        
        return NodeRex(new_start, new_final)

    def __init__(self, start, final):
        assert type(start) == Node
        assert type(final) == Node

        self.start = start
        self.final = final

    def __deepcopy__(self, memo):
        assert type(memo) == dict

        new_start = copy.deepcopy(self.start, memo)
        new_final = memo[self.final]
        shallow_copy = copy.copy(self)
        shallow_copy.start = new_start
        shallow_copy.final = new_final

        return shallow_copy

class Node(object):
    def __init__(self, is_final, transitions):
        assert type(is_final) == bool
        assert type(transitions) == list

        self.is_final = is_final
        self.transitions = transitions  # (char, node)

    def match(self, strng):
        return self.match_bfs(strng)

    def match_dfs(self, strng):
        assert type(strng) == str

        if self.is_final and len(strng) == 0:
            return True
        else:
            nonepsilon_transitions = [t for t in self.transitions if t[0] != '']
            epsilon_transitions = [t for t in self.transitions if t[0] == '']
            for transition in epsilon_transitions:
                _, node = transition
                if node.match(strng):
                    return True
            if len(strng) != 0:
                for transition in nonepsilon_transitions:
                    char, node = transition
                    if char == strng[0] and node.match(strng[1:]):
                        return True
            return False

    def match_bfs(self, strng):
        assert type(strng) == str

        """
        invariants:
            substring s[0:i] has been matched

            q1 contains all the next possible states. It is not guaranteed
            that these states are fully reduced (they may be epsilon
            transitions).

            success is True if and only if the set of current states includes
            a final state
        """
        i = 0
        q1 = [self]
        success = False
        while len(q1) > 0:
            success = False
            q2 = []
            if i == len(strng):
                while len(q1) > 0:
                    state = q1.pop()
                    if state.is_final: # final state
                        success = True
                        continue
                    for transition in state.transitions:
                        char, node = transition
                        if char == '':
                            q1.insert(0, node)
                        else:
                            pass
                q1 = q2
                if len(q1) == 0:
                    pass
                    # inv reestablished
                else:
                    raise Exception('impossible condition')
            else:
                while len(q1) > 0:
                    state = q1.pop()
                    if state.is_final: # final state
                        success = True
                    for transition in state.transitions:
                        char, node = transition
                        if char == '':
                            q1.insert(0, node)
                        else:
                            if strng[i] == char:
                                q2.insert(0, node)
                            else:
                                pass
                q1 = q2
                if len(q1) == 0:
                    pass
                    # inv reestablished
                else:
                    i = i + 1
                    # inv reestablished

        if i == len(strng):
            # s[0:len(s)] has been matched
            return success
        else:
            # s did not fully match
            return False

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)

    def __deepcopy__(self, memo):
        assert type(memo) == dict
        new_node = Node(self.is_final, [])
        memo[self] = new_node
        for transition in self.transitions:
            char, node = transition
            if node in memo.keys():
                new_node.transitions.append((char, memo[node]))
            else:
                new_node.transitions.append((char, copy.deepcopy(node, memo)))
        return new_node
