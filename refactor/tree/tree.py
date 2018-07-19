from node import Node


class Tree:

    def __init__(self, degree):
        self.nodes = [Node(node_id=0, data=None)]   # list of nodes
        self.degree = degree    # int, number of children per node
        self.leaf_leader = 0    # int, index of first leaf in tree

    def __str__(self):
        string = ""
        string += self.pretty_print(self.get_root())
        return string

    def get_root(self):
        """fetches the tree's root node"""
        return self.nodes[0]

    def get_node(self, node_id):
        """fetches a node by its id"""
        return self.nodes[node_id]

    def get_children(self, parent_node):
        """
        fetches the children nodes of a given parent node
        :param parent_node: Node object, parent of target children
        :return: list of node objects, returns an empty list of no children exist
        """
        # check if parent_node is a branch
        if parent_node.id < self.leaf_leader:   # if it is a branch
            # find sector of children
            child_id = self.degree * parent_node.id

            # find the child nodes
            children = []
            for i in range(1, self.degree + 1):
                children.append(self.get_node(child_id + i))
            return children

        else:   # if it is a leaf
            return []

    def get_parent(self, child_node):
        """
        fetches the parent node of a given node
        :param child_node: node object, child of target parent
        :return: node object, returns None if the root is given
        """
        if child_node.id == 0:
            return None
        parent_id = child_node.id // self.degree
        return parent_id

    def insert_node(self, node, node_id):
        """inserts node at the given index, node_id"""
        self.nodes[node_id] = node

    def expand_tree(self):
        """
        generates a new layer of the tree
        :return: None
        """
        for node in self.nodes[self.leaf_leader:]:
            for i in range(1, self.degree + 1):
                node_id = node.id * self.degree + i
                self.nodes.append(Node(node_id=node_id, data=None))

        self.leaf_leader = self.leaf_leader * self.degree + 1

    @ staticmethod
    def pretty_tabs(bits):
        """helper function for pretty_print, handles spacing and vertical lines"""
        s = ""
        for b in bits:
            if b:
                s += "  \u2502"
            else:
                s += "   "
        return s

    def pretty_print(self, node, bits=[]):
        """
        prints the tree in an easy to read and pleasant looking manner
        pretty_print() can also print subtrees
        :param node: root node of tree you wish to print
        :param bits: not for user, passed through for spacing purposes
        :return: str
        """
        string = ""

        if node:
            children = self.get_children(node)

            string += str(node) + '\n'

            if children:
                string += self.pretty_tabs(bits)
                string += "  \u251c"
                bits.append(True)
                string += self.pretty_print(children[0], bits)
                bits.pop(-1)

                string += self.pretty_tabs(bits)
                string += "  \u251c"
                bits.append(True)
                string += self.pretty_print(children[1], bits)
                bits.pop(-1)

                string += self.pretty_tabs(bits)
                string += "  \u251c"
                bits.append(True)
                string += self.pretty_print(children[2], bits)
                bits.pop(-1)

                string += self.pretty_tabs(bits)
                string += "  \u2514"
                bits.append(False)
                string += self.pretty_print(children[3], bits)
                bits.pop(-1)

        return string


def test():
    t = Tree(degree=4)
    t.expand_tree()
    t.expand_tree()
    print(t)


test()
