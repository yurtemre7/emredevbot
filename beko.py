import numpy as np


def isPrefixFree(dominos) -> bool:
    n = len(dominos)
    for i in range(n):
        xi = dominos[i][0]
        yi = dominos[i][1]
        if xi == yi:
            return False
        if (len(xi) < len(yi)) and (yi[: len(xi)] == xi):
            return False
        if (len(yi) < len(xi)) and (xi[: len(yi)] == yi):
            return False

    return True


def isSuffixFree(dominos) -> bool:
    n = len(dominos)
    for i in range(n):
        xi = dominos[i][0]
        yi = dominos[i][1]
        if xi == yi:
            return False
        if (len(xi) > len(yi)) and (xi[-len(yi) :] == yi):
            return False
        if (len(yi) > len(xi)) and (yi[-len(xi) :] == xi):
            return False

    return True


def isLaengenmonoton(dominos):
    n = len(dominos)
    res = False
    for i in range(n):
        xi = dominos[i][0]
        yi = dominos[i][1]
        res = len(xi) < len(yi)
        if not res or xi == yi or len(xi) == len(yi):
            res = False
            break
    res2 = False
    for i in range(n):
        xi = dominos[i][0]
        yi = dominos[i][1]
        res2 = len(xi) > len(yi)
        if not res2 or xi == yi or len(xi) == len(yi):
            res2 = False
            break
    return res or res2


def pcp_solver(dominos, max_depth):
    solutions = []
    n = len(dominos)
    for i in range(n):
        xi = dominos[i][0]
        yi = dominos[i][1]
        if xi == yi:
            return dominos[i]
        if (len(xi) < len(yi)) and (yi[: len(xi)] == xi):
            solutions.append([dominos[i]])
        if (len(yi) < len(xi)) and (xi[: len(yi)] == yi):
            solutions.append([dominos[i]])

    for _ in range(max_depth):
        new_solutions = []
        for solution in solutions:
            for j in range(n):
                new_solution = solution.copy()
                xj = dominos[j][0]
                yj = dominos[j][1]
                new_solution.append([xj, yj])
                xlist = ""
                ylist = ""
                for domino in new_solution:
                    xlist += domino[0]
                    ylist += domino[1]
                if (len(xlist) == len(ylist)) and (xlist == ylist):
                    new_solutions += [new_solution]
                if (len(xlist) < len(ylist)) and (ylist[: len(xlist)] == xlist):
                    new_solutions += [new_solution]
                if (len(ylist) < len(xlist)) and (xlist[: len(ylist)] == ylist):
                    new_solutions += [new_solution]
        if not new_solutions:
            return []
        xlength = 0
        ylength = 0
        for solution in new_solutions:
            xlength = 0
            ylength = 0
            for domino in solution:
                xlength += len(domino[0])
                ylength += len(domino[1])
            if xlength == ylength:
                return solution
        solutions = new_solutions.copy()
    return []


def pcp(emredev, cid, dominos, max_depth):
    a = ""
    if isPrefixFree(dominos):
        a += "Dieses PCP ist Präfixfrei, es hat also keine Lösungen. 🙁"
        emredev.send_message(cid, a)
        return
    if isSuffixFree(dominos):
        a += "Dieses PCP ist Suffixfrei, es hat also keine Lösungen. 🙁"
        emredev.send_message(cid, a)
        return
    if isLaengenmonoton(dominos):
        a += "Dieses PCP ist Längenmonoton, es hat also keine Lösungen. 🙁"
        emredev.send_message(cid, a)
        return
    if 50 * np.log(3)/np.log(len(dominos)) <= 50:
        a += "Tut mir leid aber mit solch großen Zahlen kann ich nicht rechnen 😢"
        emredev.send_message(cid, a)
        return
    res = pcp_solver(dominos, max_depth)

    if res != []:
        a += "Lösung für dieses PCP 😃👌: \n" + str(res) + "\n\n"
        xlist = ""
        ylist = ""
        indexes = []
        for domino in res:
            xlist += domino[0]
            ylist += domino[1]
            indexes.append(dominos.index(domino) + 1)
        a += f"{xlist} <--- Obere Zeile\n"
        a += f"{ylist} <--- Untere Zeile\n"
        a += f"Die folgenden Strings wurden benutzt: (Indezes beginnend bei 1): \n{indexes}"
    else:
        a += f"Keine Lösung für dieses PCP in {max_depth} Iterationen gefunden. 🦆"
    emredev.send_message(cid, a)
