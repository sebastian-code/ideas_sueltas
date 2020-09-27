# Random string generation time
from time import time
import string
import random


def classic(chars, length):
    tr = []
    l = len(chars) - 1
    for i in xrange(length):
        tr.append(chars[random.randint(0, l)])

    return "".join(tr)


def simpleSample(chars, length):
    return "".join(random.sample(chars * length, length))


def choice(chars, length):
    return "".join([random.choice(chars) for x in xrange(length)])


if __name__ == "__main__":
    chars = string.letters + string.digits
    times = 100
    print (
        "Random string generators comparison.\n"
        + "Dictionary length: %s\n"
        + "Times to test every algorithm: %s\n"
    ) % (len(chars), times)

    for size in (8, 16, 32, 64, 128, 256, 512, 1024):
        print "String size: %s" % size
        winnertime = None
        winner = None
        for i in (classic, simpleSample, choice):
            tf = 0
            tmin = None
            tmax = None
            for j in xrange(times):
                t0 = time()
                text = i(chars, size)
                t1 = time()
                t = t1 - t0
                tf += t / times
                if not tmin or t < tmin:
                    tmin = t
                if not tmax or t > tmax:
                    tmax = t
            # print "Algorithm: %s\nTime: %s\nGenerated: %s\n" % (str(i), t1-t0, text)
            print ("%s\n  (%fs, min %fs, max %fs)" % (repr(i), tf, tmin, tmax))
            if not winnertime or tf < winnertime:
                winnertime = tf
                winner = i
        print ("Winner: %s (%f seconds)" % (winner, winnertime))
