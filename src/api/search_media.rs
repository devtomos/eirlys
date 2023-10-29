use std::collections::HashMap;
use crate::api::queries::get_query;
use tracing::info;
use serde_json::json;

pub async fn search(media_name: String, media_type: String) -> Vec<String> {
    info!("Searching for {} in {}", media_name, media_type);
    let client = reqwest::Client::new();
    let mut map = HashMap::new();
    let query = get_query("search");

    map.insert("query", query);
    map.insert("variables", format!("{{\"search\": \"{}\", \"type\": \"{}\"}}", media_name, media_type.to_uppercase()));
    info!("Inserted values into map");

    let res = client.post("https://graphql.anilist.co")
                                    .json(&map)
                                    .send()
                                    .await;

    info!("Sent request to AniList");
    let res = json![res.unwrap().json::<serde_json::Value>().await.unwrap()];
    let data = &res["data"]["Media"];
    info!("Received response from AniList");

    // Anime Information
    let title = &data["title"]["romaji"];
    let format = &data["format"];
    let status = &data["status"];
    let episodes = &data["episodes"];
    let duration = &data["duration"];
    let genres = &data["genres"];
    let mean_score = &data["meanScore"];
    let popularity = &data["popularity"];
    let season = &data["season"];
    let url = &data["siteUrl"];

    vec![title, format, status, episodes, duration, genres, mean_score, popularity, season, url]
        .iter()
        .map(|x| x.to_string())
        .collect::<Vec<String>>()
}