class Query:
    """
    Store all queries in a string for easy access.
    e..g Query.search, Query.user, Query.relations
    """

    url: str = "https://graphql.anilist.co"

    search: str = """
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
            coverImage{
                extraLarge
            }
            title{
                romaji
                native
            }
        }
    }
    """

    user: str = """
    query ($id: Int, $name: String) {
    User(id: $id, name: $name) {
        id
        name
        siteUrl
        updatedAt
        bannerImage
        avatar {
            large
            medium
        }
        statistics {
            anime {
                count
                meanScore
                minutesWatched
                episodesWatched
                scores {
                    score
                    count
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
                scores {
                    score
                    count
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

    stats: str = """
    query ($userName: String, $mediaId: Int) {
    MediaList(userName: $userName, mediaId: $mediaId) {
        progressVolumes
        status
        score(format: POINT_10)
        progress
        repeat
        }
    }"""

    relations: str = """
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
    Page (page: $page, perPage: $perPage) {
        media (id: $id, search: $search) {
            id
            type
            synonyms
            title {
                romaji
                english
                native
                }
            }
        }
    }"""

    affinity: str = """
    query ($userName: String, $perChunk: Int, $type: MediaType) {
    MediaListCollection (userName: $userName, perChunk: $perChunk, type: $type) {
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

    staff: str = ""
