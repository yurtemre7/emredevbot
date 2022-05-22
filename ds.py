from sympy import factorint, mod_inverse


def crs(emredev, cid, a_s, m_s,):
    M = 1

    ant = ''
    for i in range(len(m_s)):
        M *= m_s[i]
        if i + 1 == len(m_s):
            ant += f'{m_s[i]}'
            continue
        ant += f'{m_s[i]} *'

    ant = '\n\n'

    # find M1, M2, M3 and their respective inverses
    M_s = [int(M / i) for i in m_s]
    y_s = None
    try:
        y_s = [pow(M_s[i], -1, m_s[i]) for i in range(len(M_s))]
    except:
        # print(M_s, m_s)
        emredev.send_message(cid, 'Deine Eingabe ist nicht lösbar.')
        return

    for i in range(len(y_s)):
        if i+1 == len(y_s):
            ant += f'M{i+1} = {M_s[i]}'
            continue
        ant += f'M{i+1} = {M_s[i]}, '

    ant += '\nKehrwerte: '
    for i in range(len(y_s)):
        if i+1 == len(y_s):
            ant += f'y{i+1} = {y_s[i]}'
            continue
        ant += f'y{i+1} = {y_s[i]}, '
    ant += '\n'

    # 'a_s[0] * y1 * M1 + a_s[1] * y2 * M2 + a_s[2] * y3 * M3' to string
    sol = 0
    ant += 'a = '
    e = 0
    for i in range(len(y_s)):
        sol += a_s[i] * y_s[i] * M_s[i]
        if i+1 == len(y_s):
            ant += f'{a_s[i]} * {M_s[i]} * {y_s[i]}'
            continue
        ant += f'{a_s[i]} * {M_s[i]} * {y_s[i]} + '
    ant += '\n'

    if sol >= M:
        sol2 = sol % M
        ant += f'Also ist x mod M = {sol} mod {M} = {sol2} die kleinste positive Lösung des obigen Systems.\n'
    else:
        ant += f'Also ist {sol} die Lösung des obigen Systems.\n'

    emredev.send_message(cid, ant)


def tschia_phi(emredev, cid, number):
    # eulers phi function of prime factorization
    # n = prime factors

    emredev.send_message(
        cid, "Berechnet phi(n) für natürliche Zahl n mit Rechenweg by Tschia")
    copy = number
    # calculate prime factors idiotisch :D, ja ich weiß, ich geh jede zahl durch

    primefactorsSTRING = f"Primfaktorzerlegung:\n{copy} ="
    factors = factorint(number)
    factors1 = list(factors.keys())
    factors2 = list(factors.values())
    solsf = ''
    for i in range(len(factors1)):
        primefactorsSTRING += f' * {factors1[i]}^{factors2[i]}'

    solsf += primefactorsSTRING.replace(" *", "", 1)

    emredev.send_message(cid, solsf)

    # calculate phi(n)
    phi = 1
    sols = ''
    sols += f"Berechnung von phi({copy}):\n"
    phiSTRING1 = "= "
    phiSTRING2 = "= "
    phiSTRING3 = "= "
    for p, e in factors.items():
        phi *= (p-1)*p**(e-1)
        phiSTRING1 += f" * (({p}-1) * {p}^({e}-1))"
        phiSTRING2 += f" * ({p-1} * {p}^{e-1})"
        phiSTRING3 += f" * {(p-1)*p**(e-1)}"

    sols += phiSTRING1.replace(" * ", "", 1) + '\n'
    sols += phiSTRING2.replace(" * ", "", 1) + '\n'
    sols += phiSTRING3.replace(" * ", "", 1) + '\n'

    emredev.send_message(cid, f"{sols}= {phi}")

    
def convertToCycles(permutation):
    myCycles = []
    while permutation:
        newCycle = []
        newCycle += [permutation[0]]
        permutation.pop(0)
        i = 0
        while newCycle[0][0] != newCycle[-1][1]:
            if permutation[i][0]==newCycle[-1][1]:
                newCycle += [permutation[i]]
                permutation.pop(i)
                i = 0
            else:
                i+=1
        myCycles += [newCycle]
    return myCycles

def displayCycle(cycle):
    return "(" + " ".join([cycle[0][0]] + [i[1] for i in cycle[:-1]]) + f") with length of {len(cycle)}"

def displayPermutation(permutation):
    return "\n".join([" \t".join([f"{permutation[j][i]:>{max(map(len, [item[0] for item in permutation]))}}" for j in range(len(permutation))]) for i in [0,1]])

def tschia_permutationOrdered(emredev, cid, str1):
    permutation = list(zip(map(str, sorted(map(int, str1.split(" ")))) if all(i.isdigit() for i in str1.split(" ")) else sorted(str1.split(" ")), str1.split(" ")))
    cycles = convertToCycles(permutation.copy())
    answer = "\n".join(["The permutation:",displayPermutation(permutation),f"contains {len(cycles)} cycles:",  ",\n".join(map(displayCycle, cycles)) + "." ])
    emredev.send_message(cid, answer)
    

def tschia_permutation(emredev, cid, str1, str2):
    permutation = list(zip(str1.split(" "), str2.split(" ")))
    cycles = convertToCycles(permutation.copy())
    answer = "\n".join(["The permutation:",displayPermutation(permutation),f"contains {len(cycles)} cycles:",  ",\n".join(map(displayCycle, cycles)) + "." ])
    emredev.send_message(cid, answer)
    
# euclidean algorithm inverse
def euk(emredev, cid, a, b):
    sol = None
    try:
        sol = pow(a, -1, b)
        emredev.send_message(cid, sol)
    except:
        emredev.send_message(cid, "Die Zahl ist nicht invertierbar.")

def p_euk(emredev, cid, a, b):
    sol = None
    try:
        sol = pow(a, -1, b)
        return sol
    except:
        return -1


def rsa_pkey(emredev, cid, p, q, e):
    phi = (p-1)*(q-1)
    # get private key
    d = p_euk(emredev, cid, e, phi)
    if d == -1:
        # return error message
        emredev.send_message(
            cid, "Privater Schlüssel kann nicht ermittelt werden.")
    # decrypt
    emredev.send_message(cid, f'Der Private Schlüssel ist: {d}')


def rsa_decrypt(emredev, cid, n, e, c):
    # decrypt
    factors = factorint(n)
    factors = list(factors.keys())
    p = factors[0]
    q = factors[1]

    phi = (p-1)*(q-1)
    d = mod_inverse(e, phi)
    if d == -1:
        # return error message
        emredev.send_message(
            cid, "Privater Schlüssel kann nicht ermittelt werden.")
    m = pow(c, d, n)
    # return decrypted message
    emredev.send_message(cid, f'Der verschlüsselte Text ist: {m}')
