from dataclasses import replace
import itertools


class Node:
    def __init__(self, value, weight, left=None, right=None):
        self.value = value
        self.weight = weight
        self.left = left
        self.right = right
        self.tiefe = 0

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return (
                self.value == __o.value
                and self.weight == __o.weight
                and self.left == __o.left
                and self.right == __o.right
            )
        return False

    def copy(self):
        return Node(
            self.value,
            self.weight,
            self.left.copy() if self.left else None,
            self.right.copy() if self.right else None,
        )

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

    def to_array(self):
        """
        return the tree as a list
        """
        liste = []
        self.traverse(liste=liste)
        return liste

    def traverse(self, liste=None, left=False, tiefe=0, bin=""):
        if liste is None:
            liste = []
        if self.left:
            self.left.traverse(liste=liste, left=True, tiefe=tiefe + 1, bin=f"{bin}0")
        if self.value:
            # print(f'{self.value} ({self.weight}) "{bin}" {tiefe} {left}')
            liste.append([self.value, self.weight, bin, tiefe, left])
        if self.right:
            self.right.traverse(liste=liste, left=False, tiefe=tiefe + 1, bin=f"{bin}1")

    def inverse(self):
        if self.left:
            self.left.inverse()
        if self.right:
            self.right.inverse()
        self.left, self.right = self.right, self.left

    def permute(self):
        copy = self.copy()
        perms = [copy]
        if copy.left and copy.right:
            a = copy.left.permute()
            b = copy.right.permute()
            for i in a:
                for j in b:
                    copy.right, copy.left = j, i
                    perms.append(copy.copy())
                    copy.right, copy.left = i, j
                    perms.append(copy.copy())
        elif copy.left:
            a = copy.left.permute()
            for i in a:
                copy.left = i
                perms.append(copy.copy())
                copy.right, copy.left = i, None
                perms.append(copy.copy())

        elif copy.right:
            b = copy.right.permute()
            for i in b:
                copy.right = i
                perms.append(copy.copy())
                copy.left, copy.right = i, None
                perms.append(copy.copy())
        return perms


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


def huffman_solver(emredev, cid, f):
    a = huffman_visualize(f)

    liste = []
    a.inverse()
    a.traverse(liste)

    liste = sorted(liste, key=lambda x: x[3])
    deep = liste[-1][3] + 1

    x = a.permute()
    emredev.send_message(cid, "Alle Permutationen:")

    for i in x:
        # print("Variante: ")
        listee = []
        i.traverse(liste=listee)
        listee = sorted(listee, key=lambda x: x[3])
        # stt = [j[2] for j in listee]
        a = "".join(
            f'{j[0]} ({j[1]}) "{j[2]}"\n'
            for i, j in itertools.product(range(deep), listee)
            if j[3] == i
        )
        emredev.send_message(cid, a)
    emredev.send_message(
        cid, "Suche jene aus, welche nach den Antwortmöglichkeiten passt :D"
    )


def calculate_inversions(emredev, cid, lista, listb):
    """
    calculate the number of inversions between two lists
    """
    a = sum(
        lista[i] > listb[j]
        for i, j in itertools.product(range(len(lista)), range(len(listb)))
    )
    emredev.send_message(cid, f"Es gibt {a} Inversionen.")


def calculate_own_inversions(emredev, cid, dominos):
    """
    calculate the number of inversions between two lists
    """
    inv_count = 0
    for i in range(len(dominos)):
        for j in range(i + 1, len(dominos)):
            if dominos[i] > dominos[j]:
                inv_count += 1

    emredev.send_message(cid, f"Es gibt {inv_count} Inversionen.")


def isPrefixFree(emredev, cid, dominos):
    """
    check if a list is prefix free
    """
    for i in range(len(dominos)):
        for j in range(i + 1, len(dominos)):
            if dominos[i] == dominos[j][: len(dominos[i])]:
                if emredev:
                    emredev.send_message(cid, "Es ist nicht präfixfrei.")
                else:
                    print("Es ist nicht präfixfrei.")
                return
    if emredev:
        emredev.send_message(cid, "Es ist präfixfrei.")
    else:
        print("Es ist präfixfrei.")


from itertools import permutations
from collections import namedtuple

Pair = namedtuple("Pair", ["student", "family"])


def pref_to_rank(pref):
    return {a: {b: idx for idx, b in enumerate(a_pref)} for a, a_pref in pref.items()}


def stable_matching_bf(*, students, families, student_pref, family_pref):
    """Solve the 'Stable Matching' problem using brute force.

    students -- set[str]. Set of students.
    families -- set[str]. Set of families.
    student_pref -- dict[str, list[str]]. Student preferences.
    family_pref -- dict[str, list[str]]. Family preferences.
    """
    s_rank = pref_to_rank(student_pref)
    f_rank = pref_to_rank(family_pref)
    s_seq = tuple(students)
    matchings = (
        [Pair(student=s, family=f) for s, f in zip(s_seq, f_seq)]
        for f_seq in permutations(families)
    )
    allres = []
    for matching in matchings:
        match_s = {pair.student: pair for pair in matching}
        match_f = {pair.family: pair for pair in matching}
        unstable = any(
            (
                s_rank[s][f] < s_rank[s][match_s[s].family]
                and f_rank[f][s] < f_rank[f][match_f[f].student]
            )
            for s in students
            for f in families
            if s != match_f[f].student
            if f != match_s[s].family
        )
        if not unstable:
            allres.append(matching)
    return allres


def stable_match_parser(emredev, cid, inp):
    """
    author : @petro ehrenmann
    """
    last = ""
    # clean input and add all to one dict
    mydict = {}
    mystr = inp.replace("/find_sm ", "")
    mystr = mystr.replace("\n", " ")
    mystr = mystr.replace(" ", "")
    mystr = mystr.replace(".", "")
    # print(mystr)
    mystr = mystr.split(",")
    for i in mystr:
        doppelpunkt = i.split(":")
        owner = doppelpunkt[0]
        pref = doppelpunkt[1].split("<")
        mydict[owner] = pref
        last = owner

    # init final vars
    st = set()
    fa = set()
    st_pref = {}
    fa_pref = {}

    # seperate 1 dict into bipartite parts
    tmp = ""
    for i in mydict[last]:
        st.add(i)
        st_pref[i] = mydict[i]
        tmp = mydict[i]

    for i in tmp:
        fa.add(i)
        fa_pref[i] = mydict[i]

    # submit request
    x = stable_matching_bf(
        students=st,
        families=fa,
        student_pref=st_pref,
        family_pref=fa_pref,
    )

    # print
    for m in x:
        a = "Stable Matching: \n"
        for p in m:
            a+= f"{p[0]} → {p[1]}\n"
        emredev.send_message(cid, a)
        
    return x


if __name__ == "__main__":
    stable_match_parser(
        """A
:
ω
<
χ
<
ψ
,
χ
:
C
<
B
<
A
,
B
:
χ
<
ψ
<
ω
,
ψ
:
A
<
C
<
B
,
C
:
ω
<
ψ
<
χ
,
ω
:
B
<
A
<
C
."""
    )
