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
    y_s = [pow(M_s[i], -1, m_s[i]) for i in range(len(M_s))]

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
