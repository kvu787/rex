import copy

class Rex(object):
    @classmethod
    def from_character(cls, char):
        assert type(char) == str
        assert len(char) == 0 or len(char) == 1

        final = _Node(True, [])
        start = _Node(False, [(char, final)])

        return cls(start, final)

    def run(self, strng):
        assert type(strng) == str

        return self.__start.run(strng)

    def concat(self, other):
        assert type(other) == Rex

        self_copy = copy.deepcopy(self)
        other_copy = copy.deepcopy(other)
        self_copy.__final.is_final = False
        self_copy.__final.transitions.append(('', other.__start))
        new_start = self_copy.__start
        new_final = other_copy.__final

        return Rex(new_start, new_final)

    def altern(self, other):
        assert type(other) == Rex

        self_copy = copy.deepcopy(self)
        other_copy = copy.deepcopy(other)
        new_start = _Node(
                False,
                [('', self_copy.__start), ('', other_copy.__start)])
        new_final = _Node(True, [])
        self_copy.__final.is_final = False
        other_copy.__final.is_final = False
        self_copy.__final.transitions.append(('', new_final))
        other_copy.__final.transitions.append(('', new_final))

        return Rex(new_start, new_final)

    def star(self):
        self_copy = copy.deepcopy(self)
        self_copy.__final.transitions.append(('', self_copy.__start))
        self_copy.__final.is_final = False
        self_copy.__start.is_final = True
        self_copy.__final = self_copy.__start

        return self_copy

    def __init__(self, start, final):
        assert type(start) == _Node
        assert type(final) == _Node

        self.__start = start
        self.__final = final

    def __deepcopy__(self, memo):
        assert type(memo) == dict

        new_start = copy.deepcopy(self.__start, memo)
        new_final = memo[self.__final]
        shallow_copy = copy.copy(self)
        shallow_copy.__start = new_start
        shallow_copy.__final = new_final

        return shallow_copy

class _Node(object):
    def __init__(self, is_final, transitions):
        assert type(is_final) == bool
        assert type(transitions) == list

        self.is_final = is_final
        self.transitions = transitions  # (char, node)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)

    def run(self, strng):
        return self.run_bfs(strng)

    def run_dfs(self, strng):
        assert type(strng) == str

        if self.is_final and len(strng) == 0:
            return True
        else:
            nonepsilon_transitions = [t for t in self.transitions if t[0] != '']
            epsilon_transitions = [t for t in self.transitions if t[0] == '']
            for transition in epsilon_transitions:
                _, node = transition
                if node.run(strng):
                    return True
            if len(strng) != 0:
                for transition in nonepsilon_transitions:
                    char, node = transition
                    if char == strng[0] and node.run(strng[1:]):
                        return True
            return False

    def run_bfs(self, strng):
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

    def __deepcopy__(self, memo):
        assert type(memo) == dict
        new_node = _Node(self.is_final, [])
        memo[self] = new_node
        for transition in self.transitions:
            char, node = transition
            if node in memo.keys():
                new_node.transitions.append((char, memo[node]))
            else:
                new_node.transitions.append((char, copy.deepcopy(node, memo)))
        return new_node
