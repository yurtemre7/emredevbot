

def inputToGrammar(inp):
    res = {}
    for line in inp.split("\n"):
        if line == "\n":
            continue
        line = line.replace(" ", "")
        splitted = line.split("->")
        if len(splitted) < 2:
            continue
        v = splitted[0]
        right = splitted[1]
        res[v] = [possibility for possibility in right.split("|")]
    return res


def printer(word, table):
    sol = ''
    space = 30
    sol += "CYK".ljust(space) + "|  \n"
    for i in range(len(word)):
        sol += str(i+1).ljust(space) + "\n"
    sol += "\n"
    sol += "-"*((len(word)+1)*space+2) + "\n"
    for i in range(len(word)):
        sol += (str(i+1) + ": " + word[i]).ljust(space) + "|  \n"
        for j in range(len(word)):
            if i + j <= len(word)-1:
                string = table[i][j].__repr__()
                if string == "set()":
                    sol += "{}".ljust(space) + "\n"
                else:
                    sol += string.ljust(space) + "\n"
            else:
                sol += " "*space + "\n"
        sol += "\n"

    return sol
