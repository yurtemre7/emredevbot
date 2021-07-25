from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot
from threading import Thread
from keys import TELEGRAM_BOT_API_KEY as api, emre_telegram_id, teoman_telegram_id
import forsa as fs
import uni_klausur_functions as kf


emredev = Bot(api)

# update and context


def echo(u, c):
    msg = u.message.text.lower()
    cid = u.message.chat.id

    print(cid)

    if 'emre' in msg:
        emredev.send_message(cid, "@emredev ist der Entwickler von mir!")

    if 'teo' in msg:
        emredev.send_message(cid, "@teomandev ist so ein Lappen :P")

    if 'isda' in msg:
        emredev.send_message(
            cid, "Ich halte ausschau nach der ISDA Note von Emre!")

    if '/help' in msg:
        emredev.send_message(
            cid, "Hier sind alle meine Befehle: /help, /isda, /emre, /teo, /minimize und /cyk")
    # minimize 5
    if '/minimize' in msg:
        # parse string "minimize 5" to int 5
        i = msg.split(' ')
        if len(i) < 5:
            emredev.send_message(
                cid, "z.B.: /minimize 7 a,b q0 q3\n\nErklärung:\n7 = größter Index der Zustände zb q7 => 7\na,b = Eingabealphabet\nq0 = Startzustand / q0,q1 Startzustände\nq3 = Endzustand / q3,q5 Endzustände\n")
        else:
            fs.tschia_minimize(emredev, i, cid)
            emredev.send_message(
                cid, "Vergiss nicht das Delta anzupassen! zb. qA0 -> q0. Die 'A's sind zum Ersetzen da.")
    if '/cyk' in msg:
        # parse string "minimize 5" to int 5
        i = msg.split(' ')
        e = msg.split("'")
        if len(i) < 2:
            emredev.send_message(
                cid, """Syntax-Error. z.B.: /cyk baaba
                        'S -> AB | BC\nA -> BA | a | b\nB -> CC | b\nC -> AB | a'""")
        else:
            print(e[1].split("'")[0])
            fs.maxim_cyk(emredev, i[1], e[1].split("'")[0], cid)


def main():
    updater = Updater(api, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.all, echo))
    updater.start_polling()
    emredev.send_message(emre_telegram_id, 'emredev.py startet!')
    emredev.send_message(teoman_telegram_id, 'emredev.py startet!')
    # Thread(target=kf.look, args=(emredev,)).start()


if __name__ == '__main__':
    main()
