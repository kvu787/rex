#!/usr/bin/python3

def main():
    test_copy()
    test_make_nfa()
    test_concat()
    test_altern()
    test_star()

class Nfa(object):
    def __init__(self, start, final):
        self.start = start
        self.final = final

    def run(self, s):
        return self.start.run(s)

    def copy(self):
        new_start, mapping = self.start.copy()
        new_final = mapping[self.final]
        return Nfa(new_start, new_final)

class Node(object):
    def __init__(self, is_final, transitions):
        self.is_final = is_final
        self.transitions = transitions  # (char, node)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)

    def run(self, s):
        if self.is_final and len(s) == 0:
            return True
        else:
            nonepsilon_transitions = filter(lambda t: t[0] != None, self.transitions)
            epsilon_transitions = filter(lambda t: t[0] == None, self.transitions)

            # try epsilon transitions
            for transition in epsilon_transitions:
                _, node = transition
                if node.run(s):
                    return True
            if len(s) != 0:
                for transition in nonepsilon_transitions:
                    char, node = transition
                    if char == s[0] and node.run(s[1:]):
                        return True
            return False

    def copy(self):
        def _copy(node, mapping):
            new_node = Node(node.is_final, [])
            mapping[node] = new_node
            for transition in node.transitions:
                char, node = transition
                if node in mapping.keys():
                    new_node.transitions.append((char, mapping[node]))
                else:
                    new_node.transitions.append((char, _copy(node, mapping)))
            return new_node
        mapping = {}
        node_copy = _copy(self, mapping)
        return node_copy, mapping

# char must be a string of length 1
def make_nfa(char):
    end = Node(True, [])
    start = Node(False, [(char, end)])
    return Nfa(start, end)

def concat(nfa1, nfa2):
    nfa1_copy = nfa1.copy()
    nfa2_copy = nfa2.copy()
    nfa1_copy.final.is_final = False
    nfa1_copy.final.transitions.append((None, nfa2_copy.start))
    return nfa1_copy

def altern(nfa1, nfa2):
    nfa1_copy = nfa1.copy()
    nfa2_copy = nfa2.copy()
    new_final = Node(True, [])
    nfa1_copy.final.is_final = False
    nfa2_copy.final.is_final = False
    nfa1_copy.final.transitions = [(None, new_final)]
    nfa2_copy.final.transitions = [(None, new_final)]
    return Nfa(
        Node(False, [(None, nfa1_copy.start), (None, nfa2_copy.start)]),
        new_final)

def star(nfa):
    nfa_copy = nfa.copy()
    nfa_copy.start.is_final = True
    nfa_copy.final.transitions.append((None, nfa_copy.start))
    return nfa_copy

def test_make_nfa():
    nfa = make_nfa('a')
    assert nfa.run('a') == True
    assert nfa.run('') == False
    assert nfa.run('b') == False
    assert nfa.run('aa') == False

def test_concat():
    nfa = concat(make_nfa('a'), make_nfa('b'))
    assert nfa.run('ab') == True
    assert nfa.run('a') == False
    assert nfa.run('') == False
    assert nfa.run('b') == False
    assert nfa.run('aa') == False

def test_altern():
    nfa = altern(make_nfa('a'), make_nfa('b'))
    assert nfa.run('ab') == False
    assert nfa.run('a') == True
    assert nfa.run('') == False
    assert nfa.run('b') == True
    assert nfa.run('aa') == False

def test_star():
    nfa = star(make_nfa('a'))
    assert nfa.run('ab') == False
    assert nfa.run('a') == True
    assert nfa.run('') == True
    assert nfa.run('b') == False
    assert nfa.run('aa') == True

def test_copy():
    # build simple nfa: 'a*b'
    two = Node(True, [])
    one = Node(False, [('b', two)])
    zero = Node(False, [('a', one)])
    one.transitions.append((None, zero))

    # make copy
    zero_copy, mapping = zero.copy()
    one_copy = zero_copy.transitions[0][1]
    two_copy = one_copy.transitions[0][1]

    # verify mapping contains all nodes
    assert len(mapping.keys()) == 3

    # verify references are different
    assert not (zero_copy is zero)
    assert not (one_copy is one)
    assert not (two_copy is two)

    # verify is_final for each copy
    assert not zero_copy.is_final
    assert not one_copy.is_final
    assert two_copy.is_final

    # verify transition lengths
    assert len(zero_copy.transitions) == 1
    assert len(one_copy.transitions) == 2
    assert len(two_copy.transitions) == 0

    # verify transition contents
    assert zero_copy.transitions[0] == ('a', one_copy)
    assert one_copy.transitions[0] == ('b', two_copy)
    assert one_copy.transitions[1] == (None, zero_copy)

if __name__ == '__main__':
    main()
