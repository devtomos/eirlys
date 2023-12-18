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
    }";

    match query_name {
        "search" => search.to_string(),
        "user_stats" => user_stats.to_string(),
        "relation_stats" => relation_stats.to_string(),
        _ => panic!("Invalid Query Name"),
    }
}
