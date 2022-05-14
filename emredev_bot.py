from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot
from threading import Thread
from time import sleep
from datetime import datetime
from keys import TELEGRAM_BOT_API_KEY as api, deine_telegram_id
import forsa as fs
import ds
import rn
import beko
import uni_klausur_functions as kf
import algotheo as al

emredev = Bot(api)


def helping(cid, msg):
    i = msg.split(" ")
    if len(i) > 1:
        cmd_helps = {
            "minimize": "Minimiert einen DFA\nz.B.: /minimize 7 a,b q0 q3\n\nErklärung:\n7 = größter Index der Zustände zb q7 => 7\na,b = Eingabealphabet\nq0 = Startzustand / q0,q1 Startzustände\nq3 = Endzustand / q3,q5 Endzustände\n",
            "gruppe": "Information zu Gruppen.",
            "notify": "Erhalte globale Nachrichten",
            "denotify": "Erhalte keine weiteren globalen Nachrichten",
            "emre": "Information zum Erfinder.",
            "cyk": """CYK-Algorithmus von CNF-Grammatiken\nz.B.: /cyk baaba
                        'S -> AB | BC\nA -> BA | a | b\nB -> CC | b\nC -> AB | a'""",
            "crs": "Chinesischer Restsatz\nz.B.: /crs 2,3 3,5 2,7",
            "prf": "Primfaktorzerlegung einer Zahl (n) und seine Eulersche Phi-Funtion\nz.B.: /prf 10",
            "rsa_pkey": "Berechnet den privaten Schlüssel bei gegebenen p und q und e.\nz.B.: /rsa_pkey 11 37 37",
            "rsa_dec": "Berechnet die originale Nachricht anhand eines öffentlichen Schlüssels (e, n) und der verschlüsselten Nachricht (c).\nz.B.: /rsa_dec 299 5 60",
            "euk": "Führt den erweiterten euklidischen Algorithmus aus bei gegebenen a und b.\nz.B.: /euk 2 9",
            "berkley": "Führt den Berkley Algorithmus für Zeitsynchronisation aus.\nz.B.: /berkley 1 2 3",
            "ntp": "Führt den NTP-Algorithmus für Zeitsynchronisation aus.\nz.B.: /ntp 1 2 3 4",
            "ip": "Konvertiert eine IP-Adresse in eine Binärzahl.\nz.B.: /ip 192.168.0.2",
            "bin": "Konvertiert eine Binärzahl in eine IP-Adresse.\nz.B.: /bin 11000000.10101000.00000010.00000000",
            "and": "Bitweises Und zweier Binärzahlen.\nz.B.: /and 11000000.10101000.00000010.00000000 11000000.10101000.00000010.00000000",
            "pcp": "Führt den PCP Algorithmus aus.\nz.B.: /pcp 6 1#101 10#00 011#11",
            "inversion": "Findet alle Inversionen zwischen zwei Listen.\nz.B.: /inversion 1,2,3 ODER /inversion 1,2,3 4,2,6",
            "prae": "Validiert ob eine Kodierung praefixfrei ist.\nz.B.: /prae 001 0011",
            "huff" : "Findet alle Huffmankodierungen.\nz.B.: /huff a,0.6 b,0.4",
            "find_sm" : "Findet alle Stable Matchings. Du kannst einfach die Aufgabe kopieren und hier einfügen.\nz.B.: /find_sm A : Z < Y < X, X : A < B < C, B : Y < X < Z, Y : C < A < B, C : X < Z < Y, Z : B < C < A."
        }
        command = i[1]

        if command not in cmd_helps:
            emredev.send_message(cid, "Keine Erklärung.. 🙁")
            return

        if command == "crs":
            emredev.send_photo(
                cid,
                photo="https://cdn.discordapp.com/attachments/319066984748941312/871069126402142298/besteErklarung.jpg",
            )
        emredev.send_message(cid, cmd_helps[command])
    else:
        emredev.send_message(
            cid,
            'Hier sind alle meine Befehle: /help, /daten, /notify, /denotify, /gruppe, /emre, /minimize, /cyk, /crs, /rsa_dec, /rsa_pkey, /euk, /prf, /berkley, /ntp, /ip, /bin, /and, /pcp, /inversion, /prae, /huff, /find_sm.\nUm mehr über einen Befehl zu erfahren schreibe: z.B: /help prf\n\nZudem reagiere ich auf die Keywords "Java" und "Ente" sobald diese in einem Satz vorkommen. Probier es doch aus!',
        )


def cmd_handling(msg, cid, msg_orig, is_group):
    emredev.sendChatAction(chat_id=cid, action="typing")
    if msg == "/start":
        intro = "Hi! Ich bin ein unoffizieller Telegram-TUB-Bot, made by @emredev, der Dir vieles einfacher macht.\n"
        nachricht = 'Es wird in der Zukunft "Nachrichten an alle" geben. Du erhälst natürlich nur eine Nachricht, wenn Du dies willst. Schreibe /notify wenn Du dabei bist und ggf. /denotify wenn Du keine weiteren Nachrichten erhalten möchtest.'
        help = "Schreibe /help um alle Befehle sehen zu können.\n"
        daten = "Schreibe /daten, falls Du weitere Infos zum Bot wissen möchtest.\n"
        emredev.send_message(cid, intro + help + daten)

    elif "/daten" in msg:
        text1 = "Damit Fehler im Laufe der Entwicklung besser nachverfolgt werden können, werden alle Nachrichten mit diesem Bot mind. 7 Tage lang zwischengespeichert.\n\n"
        text2 = "Du kannst jederzeit @emredev anschreiben und verlangen, dass Deine Daten sofort gelöscht werden sollen.\n"
        text3 = "Den Source-Code von mir, findest Du auf Github: https://github.com/yurtemre7/pythonprojs"
        emredev.send_message(cid, text1 + text2 + text3)

    elif "/gruppe" in msg:
        emredev.send_message(
            cid,
            "Du kannst mich gern in eine Gruppe hinzufügen.\n\nBedenke zusätzlich noch: /daten",
        )

    elif "/emre" in msg:
        emredev.send_message(cid, "@emredev ist der Entwickler von mir!")

    elif "java" in msg and not is_group:
        emredev.send_message(cid, "Manfred? 😊")

    elif "ente" in msg and not is_group:
        emredev.send_message(cid, "Quack! 🦆")

    elif "/log" in msg and cid == deine_telegram_id:
        emredev.send_document(cid, open("cache/log.txt", "rb"))

    elif "/ids" in msg and cid == deine_telegram_id:
        emredev.send_document(cid, open("cache/unique_ids.txt", "rb"))

    elif msg == "/notify" and not is_group:
        with open("cache/unique_ids.txt", "r+") as f:
            # read file to list
            unique_ids = list(f.read().splitlines())
            # check if user is already in list
            if str(cid) not in unique_ids and not is_group:
                f.write(f"{cid}\n")
        emredev.send_message(
            cid,
            "Du erhältst nun globale Nachrichten. Schreibe /denotify, falls dies ausversehen war.",
        )

    elif msg == "/denotify" and not is_group:
        lines = None
        with open("cache/unique_ids.txt", "r") as f:
            lines = f.readlines()
        with open("cache/unique_ids.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != f"{cid}":
                    f.write(line)
        emredev.send_message(
            cid, "Du wirst ab sofort keine globalen Nachrichten erhalten."
        )

    elif "/sendall" in msg and cid == deine_telegram_id:
        i = msg_orig.split(" ")
        txt = " "
        txt = txt.join(i[1:])

        with open("cache/unique_ids.txt", "r+") as f:
            # read file to list
            unique_ids = f.read().splitlines()
            # check if user is already in list
            for id in unique_ids:
                emredev.send_message(id, txt)

    elif "/help" in msg:
        helping(cid, msg)

    elif "/minimize" in msg:
        # parse string "minimize 5" to int 5
        i = msg.split(" ")
        if len(i) < 5:
            emredev.send_message(
                cid,
                "z.B.: /minimize 7 a,b q0 q3\n\nErklärung:\n7 = größter Index der Zustände zb q7 => 7\na,b = Eingabealphabet\nq0 = Startzustand / q0,q1 Startzustände\nq3 = Endzustand / q3,q5 Endzustände\n",
            )
        else:
            fs.tschia_minimize(emredev, i, cid)
            emredev.send_message(
                cid,
                "Vergiss nicht das Delta anzupassen! zb. qA0 -> q0. Die 'A's sind zum Ersetzen da.\nhttps://web.cs.ucdavis.edu/~doty/automata/",
            )
    elif "/cyk" in msg:
        # parse string "minimize 5" to int 5
        i = msg.split(" ")
        e = msg.split("'")
        if len(i) < 2:
            emredev.send_message(
                cid,
                """Syntax-Error. z.B.: /cyk baaba
                        'S -> AB | BC\nA -> BA | a | b\nB -> CC | b\nC -> AB | a'""",
            )
        else:
            # print(e[1].split("'")[0])
            fs.maxim_cyk(emredev, i[1], e[1].split("'")[0], cid)
    elif "/crs" in msg:
        # /crs 2,3 3,5 2,7
        i = msg.split(" ")
        if len(i) < 2:
            emredev.send_photo(
                cid,
                photo="https://cdn.discordapp.com/attachments/319066984748941312/871069126402142298/besteErklarung.jpg",
            )
            emredev.send_message(cid, "Syntax-Error. z.B.: /crs 2,3 3,5 2,7")
            return
        a_s = []
        m_s = []
        firstTime = True
        for e in i:
            if firstTime:
                firstTime = False
                continue
            bndl = e.split(",")
            a_s.append(int(bndl[0]))
            m_s.append(int(bndl[1]))
        ds.crs(emredev, cid, a_s, m_s)

    elif "/prf" in msg:
        i = msg.split(" ")
        if len(i) < 2:
            emredev.send_message(cid, "Syntax-Error. z.B.: /prf 10")
        else:
            ds.tschia_phi(emredev, cid, int(i[1]))
    elif "/euk" in msg:
        # extended euclidean algorithm inverse
        i = msg.split(" ")
        if len(i) < 3:
            emredev.send_message(cid, "Syntax-Error. z.B.: /euk a b")
        else:
            a = int(i[1])
            b = int(i[2])
            ds.euk(emredev, cid, a, b)
    elif "rsa_pkey" in msg:
        i = msg.split(" ")
        if len(i) < 4:
            emredev.send_message(cid, "Syntax-Error. z.B.: /rsa_pkey 11 37 37")
        else:
            a = int(i[1])
            b = int(i[2])
            c = int(i[3])
            ds.rsa_pkey(emredev, cid, a, b, c)
    elif "rsa_dec" in msg:
        i = msg.split(" ")
        if len(i) < 4:
            emredev.send_message(cid, "Syntax-Error. z.B.: /rsa_dec 299 5 60")
        else:
            a = int(i[1])
            b = int(i[2])
            c = int(i[3])
            ds.rsa_decrypt(emredev, cid, a, b, c)
    elif "berkley" in msg:
        i = msg.split(" ")
        if len(i) < 4:
            emredev.send_message(cid, "Syntax-Error. z.B.: /berkley 1 2 3")
        else:
            a = float(i[1])
            b = float(i[2])
            c = float(i[3])
            rn.berkley(emredev, cid, a, b, c)
    elif "ntp" in msg:
        msg = msg.replace(",", ".")
        i = msg.split(" ")
        if len(i) < 5:
            emredev.send_message(cid, "Syntax-Error. z.B.: /ntp 1 2 3 4")
        else:
            a = float(i[1])
            b = float(i[2])
            c = float(i[3])
            d = float(i[4])
            rn.ntp(emredev, cid, a, b, c, d)
    elif "ip" in msg:
        i = msg.split(" ")
        if len(i) < 2:
            emredev.send_message(cid, "Syntax-Error. z.B.: /ip 192.168.0.2")
        else:
            a = i[1]
            rn.ip_to_bin(emredev, cid, a)
    elif "bin" in msg:
        i = msg.split(" ")
        if len(i) < 2:
            emredev.send_message(
                cid, "Syntax-Error. z.B.: /bin 11000000.10101000.00000010.00000000"
            )
        else:
            a = i[1]
            rn.bin_to_ip(emredev, cid, a)
    elif "and" in msg:
        i = msg.split(" ")
        if len(i) < 3:
            emredev.send_message(
                cid,
                "Syntax-Error. z.B.: /and 11000000.10101000.00000010.00000000 11111111.11111111.11111111.00000000",
            )
        else:
            a = i[1]
            b = i[2]
            rn.bitwise_and(emredev, cid, a, b)
    elif "pcp" in msg:
        i = msg.split(" ")
        if len(i) < 3:
            emredev.send_message(cid, "Syntax-Error. z.B.: /pcp 6 b#bab ba#aa abb#bb")
        else:
            depth = int(i[1])
            dominos = []
            for j in range(2, len(i)):
                domino = i[j].split("#")
                dominos.append(domino)
            beko.pcp(emredev, cid, dominos, depth)
    elif "inversion" in msg:
        i = msg.split(" ")
        if len(i) < 2:
            emredev.send_message(cid, "Syntax-Error. z.B.: /inversion 1,2,3 ODER /inversion 1,2,3 4,2,6")
        else:
            if len(i) == 2:
                lista = [int(a) for a in i[1].split(",")]
                al.calculate_own_inversions(emredev, cid, lista)
                return
            lista = [int(a) for a in i[1].split(",")]
            listb = [int(a) for a in i[2].split(",")]
            al.calculate_inversions(emredev, cid, lista, listb)
    elif "prae" in msg:
        i = msg.split(" ")
        if len(i) < 3:
            emredev.send_message(cid, "Syntax-Error. z.B.: /prae 001 01")
        else:
            dominos = []
            for j in range(1, len(i)):
                domino = i[j]
                dominos.append(domino)
            al.isPrefixFree(emredev, cid, dominos)
    elif "huff" in msg:
        # a,2/10 b,0.3 c,0.1 d,0.4 to map {a: 0.2, b: 0.3, c: 0.1, d: 0.4}
        i = msg.split(" ")
        mapf = {}
        for j in range(1, len(i)):
            domino = i[j].split(",")
            mapf[domino[0]] = eval(domino[1])
        al.huffman_solver(emredev, cid, mapf)
    elif "/find_sm" in msg_orig:
        al.stable_match_parser(emredev, cid, msg_orig)


def welcome(chat_member, cid, title):
    for member in chat_member:
        if str(member.username) in "emredevbot":
            emredev.sendMessage(
                cid,
                'Moin, ich bin der krasse Bot! Schreibt "/help" um all meine Befehle zu erfahren!\n\nPS: Gern auch privat! 😉',
            )
        else:
            emredev.sendMessage(
                cid,
                f'Moin {member.first_name},\n\nWillkommen in der Gruppe "{title}"! 😉',
            )


def logging(u, cid, is_group, now_german, msg):
    try:
        with open("cache/log.txt", "a+") as f:
            if is_group:
                first_name = u.message.from_user.first_name
                username = u.message.from_user.username
                title = u.message.chat.title
                f.write(f'{now_german} - Group: {cid}: "{msg}"\n')
            else:
                f.write(f'{now_german} - Person: {cid}: "{msg}"\n')
    except Exception:
        pass

def echo_thread(u, c):
    msg = u.message.text
    msg_orig = u.message.text
    if msg:
        msg = msg.lower()
    cid = u.message.chat.id
    username = u.message.chat.username
    first_name = u.message.chat.first_name
    is_group = u.message.chat.title is not None
    title = u.message.chat.title

    chat_member = u.message.new_chat_members

    if len(chat_member) > 0:
        welcome(chat_member, cid, title)
    if not msg:
        return

    # current time
    now = datetime.now()
    # convert time to german time
    now_german = now.strftime("%d.%m.%Y %H:%M:%S")

    if msg.startswith("/"):
        logging(u, cid, is_group, now_german, msg)
        if len(msg) >= 1000:
            emredev.send_message(
                cid, "Deine Nachricht >= 100 Zeichen!? Willst Du mich crashen? 😠"
            )

            return

    cmd_handling(msg, cid, msg_orig, is_group)


def echo(u, c):
    Thread(
        target=echo_thread,
        args=(
            u,
            c,
        ),
    ).start()


def delete_in_7_days(emredev):
    sleep(7 * 24 * 60 * 60)
    emredev.send_message(deine_telegram_id, "Dein Log wurde gelöscht.")
    with open("cache/log.txt", "w") as f:
        f.write("")


def main():
    updater = Updater(api, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.all, echo))
    updater.start_polling()
    emredev.send_message(deine_telegram_id, "emredev.py startet! 🤠")
    # emredev.send_message(teoman_telegram_id, 'emredev.py startet!')
    # Thread(target=kf.look, args=(emredev,)).start()
    Thread(target=delete_in_7_days, args=(emredev,)).start()


if __name__ == "__main__":
    main()
