import itertools

class Node:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.left = None
        self.right = None
        self.tiefe = 0

    def my_tiefe(self, tiefe=0):
        """
        return the deepest node in the tree
        """
        if self.left:
            self.left.my_tiefe(tiefe=tiefe + 1)
        if self.right:
            self.right.my_tiefe(tiefe=tiefe + 1)
        if self.tiefe < tiefe:
            self.tiefe = tiefe
        return self.tiefe

    def traverse(self, liste=None, left=False, tiefe=0, bin=""):
        if liste is None:
            liste = []
        if self.left:
            self.left.traverse(liste=liste, left=True, tiefe=tiefe + 1, bin=f"{bin}1")
        if self.value:
            # print(f"{self.value} ({self.weight}) \"{bin}\" {tiefe} {left}")
            liste.append([self.value, self.weight, bin, tiefe, left])
        if self.right:
            self.right.traverse(liste=liste, left=False, tiefe=tiefe + 1, bin=f"{bin}0")


def huffman_visualize(f):
    nodes = [Node(k, v) for k, v in f.items()]
    nodes = sorted(nodes, key=lambda x: x.weight)
    while len(nodes) > 1:
        n1 = nodes.pop(0)
        n2 = nodes.pop(0)
        n3 = Node(None, n1.weight + n2.weight)
        n3.left = n1
        n3.right = n2
        nodes.append(n3)
        nodes = sorted(nodes, key=lambda x: x.weight)
    return nodes[0]


def huffman_solver(f):
    a = huffman_visualize(f)

    liste = []
    a.traverse(liste)

    liste = sorted(liste, key=lambda x: x[3])
    deep = liste[-1][3] + 1
    for i, j in itertools.product(range(deep), liste):
        if j[3] == i:
            print(f'{j[0]} ({j[1]}) "{j[2]}"')


def calculate_inversions(emredev, cid, lista, listb):
    """
    calculate the number of inversions between two lists
    """
    a = sum(
        lista[i] > listb[j]
        for i, j in itertools.product(range(len(lista)), range(len(listb)))
    )
    emredev.send_message(cid, f"Es gibt {a} Inversionen.")


def isPrefixFree(emredev, cid, dominos):
    """
    check if a list is prefix free
    """
    for i in range(len(dominos)):
        for j in range(i + 1, len(dominos)):
            if dominos[i] == dominos[j][:len(dominos[i])]:
                emredev.send_message(cid, "Es ist nicht präfixfrei.")
                return
    emredev.send_message(cid, "Es ist präfixfrei.")



# lista = [5, 2, 10, 4, 6]
# listb = [9, 3, 1, 7, 8]
# res = calculate_inversions(lista, listb)
# print(res)
