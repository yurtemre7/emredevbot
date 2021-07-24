from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot
from threading import Thread
from keys import TELEGRAM_BOT_API_KEY as api
import forsa as fs
import uni_klausur_functions as kf


emredev = Bot(api)

# update and context


def echo(u, c):
    msg = u.message.text.lower()
    cid = u.message.chat.id

    if 'emre' in msg:
        emredev.send_message(cid, "@emredev ist der Entwickler von mir!")

    if 'teo' in msg:
        emredev.send_message(cid, "@teomandev ist so ein Lappen :P")

    if 'isda' in msg:
        emredev.send_message(
            cid, "Ich halte ausschau nach der ISDA Note von Emre!")
    # minimize 5
    if '/minimize' in msg:
        # parse string "minimize 5" to int 5
        i = msg.split(' ')
        if len(i) < 5:
            emredev.send_message(
                cid, "Schreibe bitte den Index des größten Zustandes. z.B.: /minimize 8 a,b q0 q1")
        else:
            fs.tschia_minimize(emredev, i, cid)
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
    print('emredev.py startet!')
    # Thread(target=kf.look, args=(emredev,)).start()


if __name__ == '__main__':
    main()
