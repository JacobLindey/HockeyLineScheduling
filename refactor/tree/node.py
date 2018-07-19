
class Node:

    def __init__(self, node_id, data):
        self.id = node_id
        self.data = data

    def __str__(self):
        return f"[{self.id}, {self.data}]"
