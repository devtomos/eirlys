import nextcord, json, requests, pprint
from nextcord.ext import commands
from decimal import Decimal
from statistics import mean

#To Grab Colour
privateFile = open('private.json'); col = json.loads(privateFile.read())

url = 'https://graphql.anilist.co' #Default URL for Anilist
checkFor = ['`Chapter          :` **None**\n', '`Volumes          :` **None**\n', '`All Episodes     :` **None**\n', '`Start Date       :` **None**\n', '`End Date         :` **None**\n', '`Popularity       :` **0**\n', '`Favourites       :` **0**\n', '`Genres           :` ****\n\n', '`Repeating        :`\n> ****\n\n', '`Completed        :`\n> ****\n\n', '`Current          :`\n> ****\n\n', '`Dropped          :`\n> ****\n\n', '`Planning         :`\n> ****\n\n']
affs = {}

async def AniClassDB(connect):
    global sql
    sql = connect
    return


#Original Code
#https://github.com/jerome-ceccato/andre/blob/1ac2500605c18e9da6cc044793af157d8d40fc73/commands/mal.py
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

class Viewing(nextcord.ui.View):
    def __init__(self, options, optionsID, members, type):
        super().__init__()
        self.ooptions = options
        self.members = members
        self.optionsID = optionsID
        self.ttype = type
        self.add_item(Selection(self.ooptions[:24], self.optionsID, self.members, self.ttype))

class Selection(nextcord.ui.Select):
    def __init__(self, options, optionsID, members, type):
        self.ooptions = options
        self.dict = optionsID
        self.members = members
        self.ttype = type
        super().__init__(placeholder="Choose a title", min_values=1, max_values=1, options=self.ooptions)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if self.values[0] != '' or None:
            anilist = await Functions.Search(self.dict[self.values[0]], self.ttype, self.members, True)
            embed = nextcord.Embed(title=anilist[0]['name'], url=anilist[0]['url'], description=''.join(anilist[2]), colour=int(col['Miumi']['Colour'], 16) + 0x200)
            embed.set_image(url=anilist[0]['banner'])
            embed.set_thumbnail(url=anilist[0]['avatar'])
            await interaction.edit(embed=embed)

class Queries():
    user = """
    query ($id: Int, $name: String) {
    User(id: $id, name: $name) {
        id
        name
        about
        siteUrl
        updatedAt
        bannerImage
        avatar {
            large
            medium
        }
        favourites{
            studios{
                nodes{
                    name
                }
            }
            staff{
                nodes{
                    name{
                        full
                        native
                    }
                }
            }
            characters{
                nodes{
                    name{
                        full
                        native
                        }
                    }
                }
            manga{
                nodes{
                    title{
                        romaji
                        native
                    }
                    type
                }
            }
            anime{
                nodes{
                    title{
                        romaji
                        native
                        }
                        type
                    }
                }
        }
        statistics {
            anime {
                count
                meanScore
                minutesWatched
                episodesWatched
                scores{
                    count
                    meanScore
                    score
                }
                formats {
                    count
                    format
                }
                statuses {
                    count
                    status
                }
                releaseYears {
                    count
                    releaseYear
                    }
                startYears {
                    count
                    startYear
                }
                genres {
                    count
                    genre
                    meanScore
                    minutesWatched
                }
            }
            manga {
                count
                meanScore
                standardDeviation
                chaptersRead
                volumesRead
                scores{
                    count
                    meanScore
                    score
                }
                formats {
                    count
                    format
                }
                statuses {
                    count
                    status
                }
                releaseYears {
                    count
                    releaseYear
                    }
                startYears {
                    count
                    startYear
                }
                genres {
                    count
                    genre
                    meanScore
                    minutesWatched
                }
                }
            }
        }
    }"""

    search = '''
    query ($id: Int, $search: String, $type: MediaType) {
    Media (id: $id, search: $search, type: $type) {
            id
            season
            format
            episodes
            chapters
            volumes
            duration
            description
            status
            genres
            averageScore
            meanScore
            popularity
            siteUrl
            favourites
            bannerImage
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            airingSchedule(notYetAired: true){
                nodes{
                    timeUntilAiring
                    episode
                    }
            }
            relations{
                    nodes{
                        type
                        format
                        title{
                            romaji
                        }
                        siteUrl
                    }
                }
            characters(sort: ROLE){
                edges{
                    role
                    node{
                        name{
                            full
                        }
                        siteUrl
                    }
                }
            }
            studios(sort: NAME){
                nodes{
                    name
                }
            }
            rankings{
                rank
                context
                season
                year
            }
            startDate{
                year
                month
                day
            }
            endDate{
                year
                month
                day
            }
            coverImage{
                extraLarge
            }
            trailer{
                id
                site
            }
            title{
                romaji
                native
            }
        }
    }
    '''

    compare = '''
    query ($userName: String, $mediaId: Int) {
    MediaList(userName: $userName, mediaId: $mediaId) {
        progressVolumes
        status
        score(format: POINT_10)
        progress
        repeat
        }
    }
    '''
    
    staff = '''
        query($search: String) {
        Staff(search: $search) {
            id
            name { full }
            image { large }
            primaryOccupations
            siteUrl
            favourites
            staffMedia { nodes {
                title { romaji }
                siteUrl
            }}
            characters { edges {
                name
                media { title {romaji} siteUrl }
            }}
            }
        }'''
    
    relations = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
    Page (page: $page, perPage: $perPage) {
        media (id: $id, search: $search) {
            id
            type
            title {
                romaji
                english
                native
                }
            }
        }
    }'''

    review = """
    query ($id: Int) {
    Review(id: $id) {
        body(asHtml: false)
        summary
        rating
        ratingAmount
        score
        siteUrl
        media {
            coverImage {
                large
            }
            title {
                romaji
            }
        }
        user {
            siteUrl
            name
            avatar {
                large
            }
        }
    }
}
"""

    affinity = """
    query ($userId: Int, $perChunk: Int, $type: MediaType) {
    MediaListCollection (userId: $userId, perChunk: $perChunk, type: $type) {
        user {
            name
            avatar { large }
            siteUrl
        }
        lists {
            entries {
            status
            mediaId
            score(format: POINT_100)
        }}
        }
    }"""

class Functions():
    async def User(username):
        response = requests.post(url, json={'query': Queries.user, 'variables': {'name': username}})
        request = response.json()
        data = request['data']['User']

        if response.status_code != 200:
            userDict = {'errorCode': response.status_code}; placeHolderDict = {'errorCode': response.status_code}; return userDict, placeHolderDict
        #Using placeHolderDict because I'm lazy

        userDict = {
            'id': data['id'],
            'name': data['name'],
            'about': data['about'],
            'url': data['siteUrl'],
            'banner': data['bannerImage'],
            'avatar': data['avatar']['large'],
            'updated': data['updatedAt'],
            'errorCode': response.status_code}

        if userDict['avatar'] == None:
            userDict['avatar'] = "https://i.imgur.com/FdFIkxG.png"

        if userDict['banner'] == None:
            userDict['banner'] = "https://i.imgur.com/FdFIkxG.png"

        informationDict = {
            'animeCount': data['statistics']['anime']['count'],
            'animeMean': data['statistics']['anime']['meanScore'],
            'animeTime': data['statistics']['anime']['minutesWatched'],
            'animeWatch': data['statistics']['anime']['episodesWatched'],

            'mangaCount': data['statistics']['manga']['count'],
            'mangaMean': data['statistics']['manga']['meanScore'],
            'mangaChapt': data['statistics']['manga']['chaptersRead'],
            'mangaVolume': data['statistics']['manga']['volumesRead']}

        return userDict, informationDict
    
    async def Relations(name, type):
        response = requests.post(url, json={'query': Queries.relations, 'variables': {'search': name}})
        request = response.json()
        data = request['data']['Page']['media']

        relationID, relations, dups, amount = {}, [], [], 0

        clamp = len(data)-1
        totalClamp = max([clamp])
        while totalClamp >= 0:
            if clamp >= 0:
                if name.split()[0].lower() in str(data[clamp]['title']['romaji']).lower() or name.split()[0].lower() in str(data[clamp]['title']['english']).lower() or name.split()[0].lower() in str(data[clamp]['title']['native']).lower():
                    if data[clamp]['type'].upper() == type.upper():
                        if data[clamp]['title']['romaji'] in dups:
                            relations.append(nextcord.SelectOption(label=data[clamp]['title']['romaji'][:95] + f' | {amount}'))
                            relationID[data[clamp]['title']['romaji'][:95] + f' | {amount}'] = data[clamp]['id']
                            amount += 1
                        else:
                            dups.append(data[clamp]['title']['romaji'])
                            relations.append(nextcord.SelectOption(label=data[clamp]['title']['romaji'][:98]))
                            relationID[data[clamp]['title']['romaji'][:98]] = data[clamp]['id']
                clamp -= 1
            totalClamp -= 1

        if relations == []:
            relations.append(404)
        relations.reverse()

        return relationID, relations

    async def SearchUser(name, mediaID: int):
        request = requests.post(url, json={'query': Queries.compare, 'variables': {'userName': name, 'mediaId': mediaID}})
        response = request.json()
        data = response['data']['MediaList']

        if data is None:
            data = {
                'progress': 0,
                'status': 0,
                'score': 0,
                'progressVolumes': 0,
                'repeat': 0}

        userDict = {
            'progress': data['progress'],
            'status': data['status'],
            'score': data['score'],
            'volume': data['progressVolumes'],
            'repeat': data['repeat']}

        return userDict

    async def Search(name, type: str, members, id: False):
        if id == True:
            response = requests.post(url, json={'query': Queries.search, 'variables': {'id': name, 'type': type.upper()}})
        else:
            response = requests.post(url, json={'query': Queries.search, 'variables': {'search': name, 'type': type.upper()}})
        request = response.json()
        data = request['data']['Media']

        if response.status_code != 200:
            informationDict = {'errorCode': response.status_code}; placeHolderDict = {'errorCode': response.status_code}; return informationDict, placeHolderDict

        id = data['id']
        informationDict = {
            'id': data['id'],
            'url': data['siteUrl'],
            'name': data['title']['romaji'],
            'avatar': data['coverImage']['extraLarge'],
            'banner': data['bannerImage'],
            'status': data['status'].capitalize(),
            'chapter': data['chapters'],
            'volumes': data['volumes'],
            'episodes': data['episodes'],
            'description': 'None',
            'startDate': f"{data['startDate']['day']}/{data['startDate']['month']}/{data['startDate']['year']}",
            'endDate': f"{data['endDate']['day']}/{data['endDate']['month']}/{data['endDate']['year']}",
            'popularity': data['popularity'],
            'avgScore': f"{data['averageScore']}%",
            'meanScore': f"{data['meanScore']}%",
            'genres': ', '.join(data['genres']),
            'favourites': data['favourites'],
            'errorCode': response.status_code}

        userDict = {
            'repeating': [],
            'completed': [],
            'current': [],
            'dropped': [],
            'paused': [],
            'planning': []}

        if members != []:
            for member in members:
                data = await Functions.SearchUser(member, id)

                if data['status'] == 'REPEATING':
                    userDict['repeating'].append(f"{member}: Current - {data['progress']} | {data['score']}/10")

                if data['status'] == 'COMPLETED':
                    if data['repeat'] != 0:
                        userDict['completed'].append(f"{member}: Repeats - {data['repeat']} | {data['score']}/10")
                    else:
                        userDict['completed'].append(f"{member}: {data['score']}/10")

                if data['status'] == 'CURRENT':
                    userDict['current'].append(f"{member}: Current - {data['progress']} | {data['score']}/10")

                if data['status'] == 'DROPPED':
                    userDict['dropped'].append(f"{member}: Last - {data['progress']}")

                if data['status'] == 'PAUSED':
                    userDict['paused'].append(f"{member}: Last - {data['progress']}")

                if data['status'] == 'PLANNING':
                    userDict['planning'].append(f"{member}")

        #'airingEpisode': data['airingSchedule']['nodes'][0]['episode'],
        #'airingTime': data['airingSchedule']['nodes'][0]['timeUntilAiring']
        #Add in the future ^^^

        #|----------Remove/Alter some Keys within the dict----------|
        if informationDict['avatar'] == None:
            informationDict['avatar'] = "https://i.imgur.com/FdFIkxG.png"

        if informationDict['banner'] == None:
            informationDict['banner'] = "https://i.imgur.com/FdFIkxG.png"

        if informationDict['status'] == 'Not_yet_released':
            informationDict['status'] = 'Not Yet Released'

        if informationDict['avgScore'] == 'None%':
            informationDict['avgScore'] = '0%'

        if informationDict['meanScore'] == 'None%':
            informationDict['meanScore'] = '0%'

        if informationDict['endDate'].startswith('None'):
            informationDict['endDate'] = 'None'
        
        if informationDict['startDate'].startswith('None'):
            informationDict['startDate'] = 'None'

        description = [
            '`All Episodes     :` **{}**\n'.format(informationDict['episodes']),
            '`Status           :` **{}**\n'.format(informationDict['status']),
            '`Start Date       :` **{}**\n'.format(informationDict['startDate']),
            '`End Date         :` **{}**\n'.format(informationDict['endDate']),
            '`Avg Score        :` **{}**\n'.format(informationDict['avgScore']),
            '`Mean Score       :` **{}**\n'.format(informationDict['meanScore']),
            '`Popularity       :` **{:,}**\n'.format(informationDict['popularity']),
            '`Favourites       :` **{}**\n'.format(informationDict['favourites']),
            '`Genres           :` **{}**\n\n'.format(informationDict['genres']),
            '`Repeating        :`\n> **{}**\n\n'.format('\n> '.join(userDict['repeating'])),
            '`Completed        :`\n> **{}**\n\n'.format('\n> '.join(userDict['completed'])),
            '`Current          :`\n> **{}**\n\n'.format('\n> '.join(userDict['current'])),
            '`Dropped          :`\n> **{}**\n\n'.format('\n> '.join(userDict['dropped']),
            '`Paused           :`\n> **{}**\n\n'.format('\n> '.join(userDict['paused']))),
            '`Planning         :`\n> **{}**\n\n'.format('\n> '.join(userDict['planning']))]
        
        for key, value in enumerate(description):
            if value in checkFor:
                description[key] = ''
        #Using the checkFor list to remove anything that is Empty, makes the embed look nicer and less compact.

        return informationDict, userDict, description
    
    async def Staff(name):
        response = requests.post(url, json={'query': Queries.staff, 'variables': {'search': name}})
        request = response.json()
        data = request['data']['Staff']

        characters = data['characters']['edges']
        staffMedia = data['staffMedia']['nodes']
        staffDict = {
            'id': data['id'],
            'name': data['name']['full'],
            'occupations': data['primaryOccupations'],
            'favourites': data['favourites'],
            'url': data['siteUrl'],
            'avatar': data['image']['large'],
            'voiced': characters,
            'directed': [],
            'character': staffMedia}

        return staffDict

    async def Affinity(OGUser, loop_member, allIDs: list):
        response = requests.post(url, json={'query': Queries.affinity, 'variables': {'userId': loop_member, 'perChunk': 500, 'type': 'ANIME'}})
        request = response.json()
        data = request['data']['MediaListCollection']['lists']
        userInfo = request['data']['MediaListCollection']['user']

        if OGUser not in affs:
            affs[OGUser] = {}
            affs[OGUser]['ids'] = {}
            affs[OGUser]['all'] = []

        if loop_member != OGUser:
            if loop_member not in affs:
                affs[loop_member] = {}
                affs[loop_member]['ids'] = {}
                affs[loop_member]['all'], affs[loop_member]['shares'] = [], []

        dataClamp = len(data)-1
        totalClamp = max([dataClamp])
        while totalClamp >= 0:
            if dataClamp >= 0:
                lists = data[totalClamp]['entries']
                for entry in lists:
                    if entry['score'] == 0 or entry['status'] == 'PLANNING':
                        pass
                    else:
                        if loop_member == OGUser:
                            affs[OGUser]['all'].append(entry['mediaId'])
                            affs[OGUser]['ids'][entry["mediaId"]] = entry['score']
                        else:
                            affs[loop_member]['all'].append(entry['mediaId'])
                            affs[loop_member]['ids'][entry['mediaId']] = entry['score']
                dataClamp -= 1
            totalClamp -= 1
        
        if loop_member == OGUser:
            dicts = {'name': userInfo['name'], 'url': userInfo['siteUrl'], 'avatar': userInfo['avatar']['large']}
            return dicts
        
        if loop_member != OGUser:
            for key in list(affs[loop_member]['ids']):
                if key in affs[OGUser]['all']:
                    affs[loop_member]['ids'][key] = [affs[OGUser]['ids'][key], affs[loop_member]['ids'][key]]
                    affs[loop_member]['shares'].append(key)
                else:
                    del affs[loop_member]['ids'][key]
            
            del affs[loop_member]['all']
            values = affs[loop_member]['ids'].values()
            try: score1, score2 = list(zip(*values)); affinity = pearson(score1, score2)
            except: affinity = 0.0
            userDict = {'details': {'aff': affinity, 'name': userInfo['name'], 'url': userInfo['siteUrl'], 'shares': len(affs[loop_member]['shares'])}}
            del affs[loop_member]
            return userDict
    