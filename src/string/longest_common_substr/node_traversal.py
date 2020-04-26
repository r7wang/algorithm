class Node:
    def __init__(self, letter: str, depth: int, parent):
        self.letter = letter
        self.depth = depth
        self.parent = parent
        self.children = {}
        print('Node: {}, {}'.format(letter, depth))


def longest_common_substring(text_a: str, text_b: str) -> int:
    root_a = Node('', 0, None)
    active_nodes = [root_a]

    # At the end, we've built a graph with all substrings of text_a.
    for letter in text_a:
        for i in range(0, len(active_nodes)):
            active_node = active_nodes[i]
            if letter not in active_node.children:
                active_node.children[letter] = Node(letter, active_node.depth + 1, active_node)
            active_nodes[i] = active_node.children[letter]
        if letter not in root_a.children:
            root_a.children[letter] = Node(letter, root_a.depth + 1, root_a)
        active_nodes.append(root_a)

    # Traverse text_a graph for using letters from text_b.
    complete_nodes = []
    active_nodes = [root_a]
    for letter in text_b:
        old_active_nodes = active_nodes
        active_nodes = []
        while old_active_nodes:
            active_node = old_active_nodes.pop()
            if letter in active_node.children:
                child = active_node.children[letter]
                active_nodes.append(child)
                print('Activate Node: {}, {}'.format(child.letter, child.depth))
            else:
                complete_nodes.append(active_node)
                print('Complete Node: {}, {}'.format(active_node.letter, active_node.depth))
        active_nodes.append(root_a)
    for node in active_nodes:
        complete_nodes.append(node)
        print('Complete Node: {}, {}'.format(node.letter, node.depth))

    # Find longest substring.
    longest_substr_len = 0
    longest_substr_node = None
    for node in complete_nodes:
        if node.depth > longest_substr_len:
            longest_substr_len = node.depth
            longest_substr_node = node

    print(_substring(longest_substr_node))
    return longest_substr_len


def _substring(node: Node) -> str:
    longest_substr = []
    while node:
        longest_substr.append(node.letter)
        node = node.parent
    longest_substr.reverse()
    return ''.join(longest_substr)
