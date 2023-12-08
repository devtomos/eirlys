use std::collections::HashMap;
use crate::api::queries::get_query;
use tracing::info;
use num_format::{Locale, ToFormattedString};

pub async fn search(media_name: String, media_type: String) -> (Vec<String>, Vec<String>) {
    info!("Searching for {} in {}", media_name, media_type);
    let client = reqwest::Client::new();
    let mut map = HashMap::new();
    let query = get_query("search");

    // Insert GrahpQL Query and Variables
    // Query: Search
    // Variables: "Search": Anime_Name, "Type": Anime_Type
    map.insert("query", query);
    map.insert("variables", format!("{{\"search\": \"{}\", \"type\": \"{}\"}}", media_name, media_type.to_uppercase()));
    info!("Inserted values into map");

    let res = client.post("https://graphql.anilist.co")
                                        .json(&map)
                                        .send()
                                        .await;

    info!("Sent request to AniList");
    let res = res.unwrap().json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["Media"];
    info!("Received response from AniList");

    // Anime Information | Try to find a better alternative to joining genres (IF POSSIBLE)
    let title = &data["title"]["romaji"];
    let status = &data["status"];
    let episodes = &data["episodes"];
    let genres: Vec<String> = data["genres"].as_array().expect("Failed to convert genres to array").iter()
            .map(|v| v.as_str().expect("Failed to convert genre to string").to_owned())
            .collect();
    let genres_str = genres.join(", ");
    let mean_score = &data["meanScore"];
    let average_score = &data["averageScore"];
    let popularity = &data["popularity"].as_i64().unwrap().to_formatted_string(&Locale::en);
    let favourites = &data["favourites"].as_i64().unwrap().to_formatted_string(&Locale::en);
    let url = &data["siteUrl"];
    let avatar = &data["coverImage"]["extraLarge"];
    let banner = &data["bannerImage"];

    info!("Returning Information For {}", title);
    (vec![
        format!("`All Episodes :` **{}**", episodes),
        format!("`Status       :` **{}**", status), 
        format!("`Avg Score    :` **{}%**", average_score), 
        format!("`Mean Score   :` **{}%**", mean_score),
        format!("`Popularity   :` **{}**", popularity), 
        format!("`Favourites   :` **{}**", favourites),
        format!("`Genres       :` **{}**", genres_str),
        ].iter().map(|x| x.trim_matches('"').to_string()).collect(),

        vec![
            title.to_string(),
            url.to_string(),
            avatar.to_string(),
            banner.to_string(),
        ].iter().map(|x| x.trim_matches('"').to_string()).collect())
        // Try to find an alternative way (only way I could think of right now)
}