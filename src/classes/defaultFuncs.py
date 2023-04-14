import asyncpg
import os
import re
import logging
import sys
from decimal import Decimal
from statistics import mean

# [+] Setup Logging for Nextcord [+]#
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s:%(levelname)s:%(name)s]: %(message)s'))
logger.addHandler(handler)


# [+] Connect To Database [+]#
async def sql_func():
    if os.getenv('DB_URL') is not None:
        try:
            sql_func.sql = await asyncpg.connect(os.getenv('DB_URL'))
            logger.info(f'Connected to Database')
        except:
            logger.critical(f'Could not load Database from URL')
    else:
        return logger.critical(f'Could not load Database')


# [+] Return Fixed List [+]#
def atoi(text):
    return int(text) if text.isdigit() else text


# [+] Return Fixed List [+]#
def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


# [+] Calculate The Pearson For Users [+]#
def pearson(x, y):
    """
    Pearson's correlation implementation without scipy or numpy.
    :param list x: Dataset x
    :param list y: Dataset y
    :return: Population pearson correlation coefficient
    :rtype: float
    """
    mx = Decimal(mean(x))
    my = Decimal(mean(y))

    xm = [Decimal(i) - mx for i in x]
    ym = [Decimal(j) - my for j in y]

    sx = [i ** 2 for i in xm]
    sy = [j ** 2 for j in ym]

    num = sum([a * b for a, b in zip(xm, ym)])
    den = Decimal(sum(sx) * sum(sy)).sqrt()

    # Stdev of one (or both) of the scores is zero if the
    # denominator is zero. Dividing by zero is impossible, so
    # just check if it is zero before we tell it to divide.
    if den == 0.0:
        raise Exception()

    return round(float(num / den) * 100, 2)


# [+] Return Time From Seconds [+]#
def returnTime(seconds, granularity=2):
    intervals = (
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1),
    )

    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])
