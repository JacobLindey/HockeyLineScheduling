
class Path:

    def __init__(self, nodes=None, value=0):
        self.nodes = nodes
        self.value = value

    def evaluate(self):
        # TODO: implement path evaluation
        if self.nodes is not None:
            print(f"Evaluating path from {self.nodes[0]} to {self.nodes[-1]}")
        else:
            print("Evaluating empty path")
        return
