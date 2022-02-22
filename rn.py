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


# convert 192.168.2.0 to binary representation
def ip_to_bin(emredev, cid, ip):
    emredev.send_message(
        cid,
        ".".join(format(int(x), "08b") for x in ip.split(".")),
    )


# convert binary representation to ip address
def bin_to_ip(emredev, cid, bin):
    emredev.send_message(
        cid,
        ".".join(str(int(x, 2)) for x in bin.split(".")),
    )

# bitwise and of two binary strings
def bitwise_and(emredev, cid, bin1, bin2):
    bin1 = "".join(bin1.split("."))
    bin2 = "".join(bin2.split("."))
    c = int(bin1, 2) & int(bin2, 2)
    d = bin(c)[2:]
    emredev.send_message(cid, d)