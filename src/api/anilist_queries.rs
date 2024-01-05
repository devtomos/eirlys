pub const QUERY_URL: &str = "https://graphql.anilist.co";

pub fn get_query(query_name: &str) -> String {
    let search: &str = "
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
    ";

    let user: &str = "
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
    }";

    let user_stats: &str = "
    query ($userName: String, $mediaId: Int) {
        MediaList(userName: $userName, mediaId: $mediaId) {
            progressVolumes
            status
            score(format: POINT_10)
            progress
            repeat
        }
    }";

    let relation_stats: &str = "
    query ($id: Int, $page: Int, $perPage: Int, $search: String, $type: MediaType) {
    Page (page: $page, perPage: $perPage) {
        media (id: $id, search: $search, type: $type) {
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
    }";

    match query_name {
        "search" => search.to_string(),
        "user_stats" => user_stats.to_string(),
        "relation_stats" => relation_stats.to_string(),
        "user" => user.to_string(),
        _ => panic!("Invalid Query Name"),
    }
}



pub fn return_time(mut seconds: u64, granularity: usize) -> String {
    let intervals = [
        ("weeks", 604800),
        ("days", 86400),
        ("hours", 3600),
        ("minutes", 60),
        ("seconds", 1),
    ];

    let mut result = Vec::new();
    for &(name, count) in &intervals {
        let value = seconds / count;
        if value > 0 {
            seconds -= value * count;
            let name = if value == 1 {
                name.trim_end_matches('s')
            } else {
                name
            };
            result.push(format!("{} {}", value, name));
        }
    }
    result.into_iter().take(granularity).collect::<Vec<_>>().join(", ")
}