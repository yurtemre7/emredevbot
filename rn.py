def ntp(bot, cid, t1, t2, t3, t4):
    """
    t1 = time1
    t2 = time2
    t3 = time3
    t4 = time4

    returns the delay and offset
    """
    delay = (t4 - t1) - (t3 - t2)
    offset = ((t2 - t1) + (t3 - t4)) / 2
    bot.send_message(cid, f"Delay: {delay}, Offset: {offset}")


def berkley(emredev, cid, t1, t2, t3):
    """
    t1 = time1
    t2 = time2
    t3 = time3

    returns the new average time t1 should adapt to.
    """
    t_array = [t1, t2, t3]
    emredev.send_message(
        cid,
        f"Durchschnittszeit: {sum(t_array) / len(t_array)}. Setze t1 auf diesen Durchschnitt.",
    )
    return
