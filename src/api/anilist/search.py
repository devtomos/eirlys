from typing import Dict
from typing import Tuple
from typing import List

import requests
import nextcord

from src.api.general.errors import *
from src.api.anilist.queries import Query
from src.api.general.wide_functions import *


async def search(media_name: str, media_type: str, db_members: list, is_component: bool) -> Tuple[Dict, List]:
    """
        Search for Anime and Manga based on given type and anime and extract data.

        :param media_name: str -- Name of media
        :param media_type: str  -- Type of media (ANIME or MANGA)
        :param db_members: list -- List of members in the database
        :param is_component: bool -- If the search is from a component or not
        RETURNS: Dict, List -- Returns a dictionary with the data and a ready-made list for the embed
    """

    if is_component:
        logger.info(f"Searching for media with ID {media_name} with type {media_type.upper()}")
        variable_array = {'id': media_name, 'type': media_type.upper()}
    else:
        logger.info(f"Searching for {media_name} with type {media_type.upper()}")
        variable_array = {'search': media_name, 'type': media_type.upper()}

    response = requests.post(Query.url,
                             json={'query': Query.search, 'variables': variable_array})
    request = response.json()
    data = request['data']['Media']

    if response.status_code != 200:
        logger.error(
            f"Ran into an error while searching for {media_name} with type {media_type.upper()} with "
            f"status code {response.status_code}")
        raise StatusCodeError(response.status_code, search.__name__)

    logger.info(f"Constructing array and list with Data from {media_name}")

    # Alter or fix data here
    if data['status'] == 'Not_yet_released':
        data['status'] = 'Not Yet Released'

    if not data['airingSchedule']['nodes']:
        data['airingSchedule']['nodes'] = [{'episode': 1, 'timeUntilAiring': 1}]

    search_data = {
        'id': data['id'],
        'url': data['siteUrl'],
        'name': data['title']['romaji'],
        'avatar': data['coverImage']['extraLarge'],
        'banner': data['bannerImage'],
        'status': data['status'].capitalize(),
        'chapters': data['chapters'],
        'volumes': data['volumes'],
        'episodes': data['episodes'],
        'currentEpisode': data['airingSchedule']['nodes'][0]['episode'] - 1,
        'airingDate': rtime(data['airingSchedule']['nodes'][0]['timeUntilAiring']),
        'startDate': f"{data['startDate']['day']}/{data['startDate']['month']}/{data['startDate']['year']}",
        'endDate': f"{data['endDate']['day']}/{data['endDate']['month']}/{data['endDate']['year']}",
        'popularity': data['popularity'],
        'avgScore': f"{data['averageScore']}%",
        'meanScore': f"{data['meanScore']}%",
        'genres': ', '.join(data['genres']),
        'favourites': data['favourites'],
        'repeating': [],
        'completed': [],
        'current': [],
        'dropped': [],
        'paused': [],
        'planning': [],
        'errorCode': response.status_code
    }

    # Get User Scores If Members Is Not Empty
    if db_members:
        for member in db_members:
            logger.info(f"Adding {member} to {media_name} array")
            user_stats = await stats(member, data['id'])

            if user_stats['status'] == 'REPEATING':
                search_data['repeating'].append(f"{member} - `{user_stats['progress']} | {user_stats['score']}/10`")

            if user_stats['status'] == 'COMPLETED':
                if user_stats['repeat'] != 0:
                    search_data['completed'].append(
                        f"{member} - `{user_stats['repeat']} repeats | {user_stats['score']}/10`")
                else:
                    search_data['completed'].append(f"{member} - `{user_stats['score']}/10`")

            if user_stats['status'] == 'CURRENT':
                search_data['current'].append(f"{member} - `{user_stats['progress']} | {user_stats['score']}/10`")

            if user_stats['status'] == 'DROPPED':
                search_data['dropped'].append(f"{member}")

            if user_stats['status'] == 'PAUSED':
                search_data['paused'].append(f"{member}")

            if user_stats['status'] == 'PLANNING':
                search_data['planning'].append(f"{member}")

    search_list = [
        '`All Episodes     :` **{}**\n'.format(search_data['episodes']),
        '`Current Episode  :` **{}**\n'.format(search_data['currentEpisode']),
        '`Chapters         :` **{}**\n'.format(search_data['chapters']),
        '`Volumes          :` **{}**\n'.format(search_data['volumes']),
        '`Airing Date      :` **{}**\n'.format(search_data['airingDate']),
        '`Status           :` **{}**\n'.format(search_data['status']),
        '`Start Date       :` **{}**\n'.format(search_data['startDate']),
        '`End Date         :` **{}**\n'.format(search_data['endDate']),
        '`Avg Score        :` **{}**\n'.format(search_data['avgScore']),
        '`Mean Score       :` **{}**\n'.format(search_data['meanScore']),
        '`Popularity       :` **{:,}**\n'.format(search_data['popularity']),
        '`Favourites       :` **{}**\n'.format(search_data['favourites']),
        '`Genres           :` **{}**\n\n'.format(search_data['genres']),
        '`Repeating        :`\n> **{}**\n\n'.format('\n> '.join(search_data['repeating'])),
        '`Completed        :`\n> **{}**\n\n'.format('\n> '.join(search_data['completed'])),
        '`Current          :`\n> **{}**\n\n'.format('\n> '.join(search_data['current'])),
        '`Dropped          :`\n> **{}**\n\n'.format('\n> '.join(search_data['dropped'])),
        '`Paused           :`\n> **{}**\n\n'.format('\n> '.join(search_data['paused'])),
        '`Planning         :`\n> **{}**\n\n'.format('\n> '.join(search_data['planning']))]

    for key, value in enumerate(search_list):
        if value in compare_search:
            search_list[key] = ''

    logger.info(f"Returning list with data from {media_name}")
    return search_data, search_list


async def relations(media_name: str, media_type: str) -> Tuple[list, dict]:
    """
            Search for Anime and Manga based on the given type and keywords used for the name.

            :param media_name: str -- Name of media
            :param media_type: str  -- Type of media (ANIME or MANGA)
    """
    response = requests.post(Query.url, json={'query': Query.relations, 'variables': {'search': media_name}})
    request = response.json()
    data = request['data']['Page']['media']
    relations_array, relations_list, duplicates = {}, [], []

    if response.status_code != 200:
        raise StatusCodeError(response.status_code, search.__name__)

    clamp = len(data) - 1
    totalClamp = max([clamp])
    while totalClamp >= 0:
        if clamp >= 0:
            # Splicing the media into parts and using the first word to grab the media name.
            if (media_name.split()[0].lower() in str(data[clamp]['title']['romaji']).lower()) or (
                    str(data[clamp]['title']['english']).lower()) or (str(data[clamp]['title']['native']).lower()) or \
                    (str(data[clamp]['synonyms']).lower()):

                # Check to see if the media type matches the one we are looking for.
                if data[clamp]['type'].upper() == media_type.upper():
                    # If media is a duplicate, then we will add brackets around the name.
                    if data[clamp]['title']['romaji'] in duplicates:
                        # Append the duplicate media to the list.
                        relations_list.append(
                            nextcord.SelectOption(label=f"[{data[clamp]['title']['romaji'][:95]}]"))
                        # Set the duplicate media with the ID as the value.
                        relations_array[f"[{data[clamp]['title']['romaji'][:95]}]"] = data[clamp]['id']
                    else:
                        # Append into the duplicates list. so it can no longer be used
                        duplicates.append(data[clamp]['title']['romaji'])
                        # Append the media to the list.
                        relations_list.append(nextcord.SelectOption(label=data[clamp]['title']['romaji'][:98]))
                        # Append the media with the ID as the value.
                        relations_array[data[clamp]['title']['romaji'][:98]] = data[clamp]['id']
            clamp -= 1
        totalClamp -= 1

    # Reverse the list so that the most reliable results are at the top.
    relations_list.reverse()

    logger.info(f"Returning list with amount of {len(relations_list)} and array with {len(relations_array)} items")

    return relations_list, relations_array


async def stats(username: str, series_id: int) -> Dict:
    """
        Get the user's stats for the given series ID.

        :param username: str -- Username of the user
        :param series_id: int -- ID of the series
    """

    request = requests.post(Query.url, json={'query': Query.stats,
                                             'variables': {'userName': username, 'mediaId': series_id}})

    response = request.json()
    data = response['data']['MediaList']

    # If no data is returned, then we will set the data to None.
    if data is None:
        data = {'progress': 0, 'status': 0, 'score': 0, 'progressVolumes': 0, 'repeat': 0}
    else:
        # If data is returned, then we will set the data to the correct values.
        data = {
            'progress': data['progress'], 'status': data['status'], 'score': data['score'],
            'volume': data['progressVolumes'], 'repeat': data['repeat']}
    return data
