import requests as r
from time import sleep
from keys import cookie, emre_telegram_id


def getHeaders():
    '''
    get your own cookie (F12 on ISIS) and save it in a file called keys.py as a string.
    '''
    return {
        'Cookie': cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }


def look(emredev):
    while True:
        resp = ''
        try:
            resp = r.get(
                "https://isis.tu-berlin.de/mod/quiz/view.php?id=1144126",
                headers=getHeaders())
        except:
            emredev.send_message(
                emre_telegram_id,
                "Es ist ein Fehler aufgetreten. (Cookie expired ?)"
            )
            return

        txt = resp.text
        print(len(txt.split('Nicht erlaubt')))
        if len(txt.split('Nicht erlaubt')) < 2:
            emredev.send_message(
                emre_telegram_id,
                "Es gibt eine Note!\nHier der Link:\n\nhttps://isis.tu-berlin.de/mod/quiz/view.php?id=1144126"
            )
            break

        print("Noch nicht..")

        sleep(15)
    emredev.send_message(
        emre_telegram_id,
        "Es gibt eine Note!\nHier der Link:\n\nhttps://isis.tu-berlin.de/mod/quiz/view.php?id=1144126"
    )
