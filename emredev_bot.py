from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot
from threading import Thread
from time import sleep
from datetime import datetime
from keys import TELEGRAM_BOT_API_KEY as api, emre_telegram_id, teoman_telegram_id
import forsa as fs
import ds
import uni_klausur_functions as kf


emredev = Bot(api)

# update and context


def echo(u, c):
    msg = u.message.text
    if msg:
        msg = msg.lower()
    cid = u.message.chat.id
    username = u.message.chat.username
    first_name = u.message.chat.first_name
    is_group = u.message.chat.title is not None

    chat_member = u.message.new_chat_members

    if len(chat_member) > 0:
        for member in chat_member:
            if str(member.username) in "emredevbot":
                emredev.sendMessage(
                    cid, 'Moin, ich bin der krasse Bot! Schreibt "/help" um all meine Befehle zu erfahren!\n\nPS: Gern auch privat! 😉')
            else:
                title = u.message.chat.title
                emredev.sendMessage(
                    cid, f'Moin {member.first_name},\n\nWillkommen in der Gruppe "{title}"! 😉')
    if not msg:
        return

    # current time
    now = datetime.now()
    # convert time to german time
    now_german = now.strftime('%d.%m.%Y %H:%M:%S')

    with open('cache/log.txt', 'a+') as f:
        if is_group:
            first_name = u.message.from_user.first_name
            username = u.message.from_user.username
            title = u.message.chat.title
            f.write(
                f'{now_german} - {first_name} aka @{username} (Group: "{title}" {cid}): "{msg}"\n')
        else:
            f.write(
                f'{now_german} - {first_name} aka @{username} ({cid}): "{msg}"\n')

    if msg == '/start':
        intro = 'Hi! Ich bin ein unoffizieller Telegram-TUB-Bot, made by @emredev, der Dir vieles einfacher macht.\n'
        help = 'Schreibe /help um alle Befehle sehen zu können.\n'
        daten = 'Schreibe /daten, falls du weitere Infos zum Bot wissen möchtest.\n'
        emredev.send_message(cid, intro + help + daten)

    elif '/daten' in msg:
        text1 = 'Damit Fehler im Laufe der Entwicklung besser nachverfolgt werden können, werden alle Nachrichten mit diesem Bot mind. 7 Tage lang zwischengespeichert.\n\n'
        text2 = 'Du kannst jederzeit @emredev anschreiben und verlangen, dass Deine Daten sofort gelöscht werden sollen.\n'
        text3 = 'Den Source-Code von mir, findest Du auf Github: https://github.com/yurtemre7/pythonprojs'
        emredev.send_message(cid, text1 + text2 + text3)

    elif '/gruppe' in msg:
        emredev.send_message(
            cid, 'Du kannst mich gern in eine Gruppe hinzufügen.\n\nBedenke zusätzlich noch: /daten')

    elif '/emre' in msg:
        emredev.send_message(cid, "@emredev ist der Entwickler von mir!")

    elif 'java' in msg:
        emredev.send_message(cid, 'Manfred? 😊')

    elif 'ente' in msg:
        emredev.send_message(cid, 'Quack! 🦆')

    elif '/log' in msg and cid == emre_telegram_id:
        emredev.send_document(cid, open('cache/log.txt', 'rb'))

    elif '/help' in msg:
        emredev.send_message(
            cid, "Hier sind alle meine Befehle: /help, /daten, /gruppe, /emre, /minimize, /cyk, /crs und /prf")
    # minimize 5
    elif '/minimize' in msg:
        # parse string "minimize 5" to int 5
        i = msg.split(' ')
        if len(i) < 5:
            emredev.send_message(
                cid, "z.B.: /minimize 7 a,b q0 q3\n\nErklärung:\n7 = größter Index der Zustände zb q7 => 7\na,b = Eingabealphabet\nq0 = Startzustand / q0,q1 Startzustände\nq3 = Endzustand / q3,q5 Endzustände\n")
        else:
            fs.tschia_minimize(emredev, i, cid)
            emredev.send_message(
                cid, "Vergiss nicht das Delta anzupassen! zb. qA0 -> q0. Die 'A's sind zum Ersetzen da.")
    elif '/cyk' in msg:
        # parse string "minimize 5" to int 5
        i = msg.split(' ')
        e = msg.split("'")
        if len(i) < 2:
            emredev.send_message(
                cid, """Syntax-Error. z.B.: /cyk baaba
                        'S -> AB | BC\nA -> BA | a | b\nB -> CC | b\nC -> AB | a'""")
        else:
            # print(e[1].split("'")[0])
            fs.maxim_cyk(emredev, i[1], e[1].split("'")[0], cid)
    elif '/crs' in msg:
        # /crs 2,3 3,5 2,7
        i = msg.split(' ')
        if len(i) < 2:
            emredev.send_photo(
                cid, photo='https://cdn.discordapp.com/attachments/319066984748941312/871069126402142298/besteErklarung.jpg')
            emredev.send_message(
                cid, "Syntax-Error. z.B.: /crs 2,3 3,5 2,7")
            return
        a_s = []
        m_s = []
        firstTime = True
        for e in i:
            if firstTime:
                firstTime = False
                continue
            bndl = e.split(',')
            a_s.append(int(bndl[0]))
            m_s.append(int(bndl[1]))
        ds.crs(emredev, cid, a_s, m_s)

    elif '/prf' in msg:
        i = msg.split(' ')
        if len(i) < 2:
            emredev.send_message(
                cid, "Syntax-Error. z.B.: /prf 10")
        else:
            ds.tschia_phi(emredev, cid, int(i[1]))


def delete_in_7_days(emredev):
    sleep(7*24*60*60)
    emredev.send_message(emre_telegram_id, 'Dein Log wurde gelöscht.')
    with open('cache/log.txt', 'w') as f:
        f.write('')


def main():
    updater = Updater(api, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.all, echo))
    updater.start_polling()
    emredev.send_message(emre_telegram_id, 'emredev.py startet!')
    # emredev.send_message(teoman_telegram_id, 'emredev.py startet!')
    # Thread(target=kf.look, args=(emredev,)).start()
    Thread(target=delete_in_7_days, args=(emredev,)).start()


if __name__ == '__main__':
    main()
