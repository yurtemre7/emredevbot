import cyk
from itertools import product


def tschia_minimize(emredev, i, cid):
    sol = ''
    e = int(i[1])+1
    alphabet = i[2]
    startnode = i[3]
    endnodes = i[4]
    sol += "\n\n\nstates = {q0"
    for i in range(1, e):
        sol += ",q"+str(i)
    sol += "}\n"

    sol += "input_alphabet = {"+alphabet+"}\n"
    sol += "start_state = " + startnode + "\n"
    sol += "accept_states = {" + endnodes + "}\n"

    sol += "delta = \n"
    for i in range(e):
        for j in alphabet.split(","):
            sol += "    q"+str(i)+","+j+" -> qA"+str(i)+";\n"
    sol += "\n\n"

    emredev.send_message(cid, sol)


def maxim_cyk(emredev, word, input, cid):
    G = """
        'S -> AB | BC
        A -> BA | a | b
        B -> CC | b
        C -> AB | a'
    """

    format = cyk.inputToGrammar(input)
    table = [[set() for _ in range(len(word))] for __ in range(len(word))]

    for length in range(1, len(word)+1):
        for i in range(len(word)-length+1):
            searches = []
            if length == 1:
                searches.append(word[i])
            else:
                for newLength in range(1, length):
                    l1 = word[i:i+newLength]
                    l2 = word[i+newLength:i+length]

                    v1 = table[i][newLength-1]
                    v2 = table[i+newLength][length-newLength-1]

                    searches += [''.join(i) for i in product(*[v1, v2])]

            for k, v in format.items():
                for res in v:
                    for s in searches:
                        if s == res:
                            table[i][length-1].add(k)

    sol = cyk.printer(word, table)
    emredev.send_message(cid, sol)
