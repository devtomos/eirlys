"""
    Functions used throughout the entire bot will be stored here.
    Links and such go to the respected owners of code which was used, unless mine or could not be found.
"""
import asyncio
import re
import logging
import sys
import os
from typing import Any, Type, List

import asyncpg

from decimal import Decimal
from statistics import mean
from src.api.general.errors import *
from src.api.general.errors import NoDataBaseError

#%(asctime)s:%(levelname)s:%(name)s

# Setup Logging for all files
logger = logging.getLogger('eirlys')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(levelname)s:%(name)s]: %(message)s'))
logger.addHandler(handler)

# Not sure how else to really do this. If you have any other way let me know.
compare_search = [
    '`All Episodes     :` **None**\n', '`Current Episode  :` **0**\n', '`Chapters         :` **None**\n',
    '`Volumes          :` **None**\n', '`Airing Date      :` **1 second**\n',
    '`Status           :` **Not_yet_released**\n', '`Start Date       :` **None/None/None**\n',
    '`End Date         :` **None/None/None**\n', '`Avg Score        :` **None%**\n', '`Mean Score       :` **None%**\n',
    '`Popularity       :` **0**\n', '`Favourites       :` **0**\n', '`Genres           :` ****\n\n',
    '`Repeating        :`\n> ****\n\n', '`Completed        :`\n> ****\n\n', '`Current          :`\n> ****\n\n',
    '`Dropped          :`\n> ****\n\n', '`Paused           :`\n> ****\n\n', '`Planning         :`\n> ****\n\n']


# Connect to database
async def db_connect() -> Type[NoDataBaseError] | Any:
    if os.getenv("DB_URL") is not None:
        logger.info("Connection to PostgresSQL has been made.")
        return await asyncpg.connect(os.getenv("DB_URL"))
    else:
        return NoDataBaseError("Database URL is not working. Please update or add the Database URL to the .env file.")


# Return text
# Forgot where I got this from, but it was a while ago.
def atoi(text) -> int:
    return int(text) if text.isdigit() else text


# Sort List
# Forgot where I got this from, but it was a while ago.
def natural_keys(text) -> List:
    """
    alist.sort(key=natural_keys) sorts in human order
    """
    return [atoi(c) for c in re.split(r'(\d+)', text)]


# Calculate The Pearson For Users #
# https://github.com/jerome-ceccato/andre/blob/1ac2500605c18e9da6cc044793af157d8d40fc73/commands/mal.py#L695-L718
def pearson(x, y) -> float:
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

    if den == 0.0:
        raise Exception()

    return round(float(num / den) * 100, 2)


# Return readable time
# Forgot where I got this from, but it was a while ago.
def rtime(seconds, granularity=2) -> str:
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
