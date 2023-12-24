use crate::api::queries::get_query;
use num_format::{Locale, ToFormattedString};
use serde_json::json;
use std::{collections::HashMap, cmp};
use tracing::info;

// ------------------------------------------------------------------------------------------------------------------------ //

pub async fn relation_names(media_name: String, media_type: String) -> (Vec<String>, HashMap<String, String>) {
    let client = reqwest::Client::new();
    let query = get_query("relation_stats");
    let json = json!({"query": query, "variables": {"search": media_name}});
    info!("Query has been inserted into JSON");

    let res = client
        .post("https://graphql.anilist.co")
        .json(&json)
        .send()
        .await;

    info!("Sent request to AniList | RELATION SEARCH");
    let res = res.unwrap().json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["Page"]["media"];
    info!("Received response from AniList | RELATIONS SEARCH");

    let mut relations_array = HashMap::new();
    let mut relations_list = Vec::new();
    let mut duplicates = Vec::new();
    info!("Created relations array, list and duplicate list");

    let media_name = media_name.to_lowercase();
    for media_item in data.as_array().unwrap().iter().rev() {
        let title_romaji = media_item["title"]["romaji"].as_str().unwrap_or_default().to_lowercase();
        let title_english = media_item["title"]["english"].as_str().unwrap_or_default().to_lowercase();
        let title_native = media_item["title"]["native"].as_str().unwrap_or_default().to_lowercase();
        let synonyms = media_item["synonyms"].as_str().unwrap_or_default().to_lowercase();

        if (title_romaji.contains(&media_name) || title_english.contains(&media_name) || title_native.contains(&media_name) || synonyms.contains(&media_name)) && media_item["type"].as_str().unwrap_or_default().to_uppercase() == media_type.to_uppercase() {
            if duplicates.contains(&title_romaji) {
                relations_list.push(format!("[{}]", &title_romaji[..cmp::min(title_romaji.len(), 95)]));
                relations_array.insert(format!("[{}]", &title_romaji[..cmp::min(title_romaji.len(), 95)]), media_item["id"].as_str().unwrap_or_default().to_string());
            } else {
                duplicates.push(title_romaji.clone());
                relations_list.push(title_romaji[..cmp::min(title_romaji.len(), 98)].to_string());
                relations_array.insert(title_romaji[..cmp::min(title_romaji.len(), 98)].to_string(), media_item["id"].as_str().unwrap_or_default().to_string());
            }
        }
    }

    info!("Returning relations list: {:?}\n", relations_list);

    (relations_list, relations_array)
}

// ------------------------------------------------------------------------------------------------------------------------ //

pub async fn user_scores(user_name: String, media_id: i64) -> HashMap<String, String> {
    // Insert GrahpQL Query and Variables
    // Query: Search
    // Variables: "userName": user_name, "mediaId": media_id
    let client = reqwest::Client::new();
    let query = get_query("user_stats");
    let mut user_data: HashMap<String, String> = HashMap::new();
    let json = json!({"query": query, "variables": {"userName": user_name, "mediaId": media_id}});
    info!("Query has been inserted into JSON");

    let res = client
        .post("https://graphql.anilist.co")
        .json(&json)
        .send()
        .await;

    info!("Sent request to AniList | USER SEARCH");
    let res = res.unwrap().json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["MediaList"];
    info!("Received response from AniList | USER SEARCH");

    info!("Checking to see if data is null");
    match data {
        serde_json::Value::Null => {
            info!("Data is null, returning null hashmap\n");
            user_data.insert("status".to_string(), "null".to_string());
            return user_data;
        }
        _ => {
            info!("Data is not null, inserting data into hashmap");
            user_data.insert("progress".to_string(), data["progress"].to_string());
            user_data.insert("status".to_string(), data["status"].to_string());
            user_data.insert("score".to_string(), data["score"].to_string());
            user_data.insert(
                "progressVolumes".to_string(),
                data["progressVolumes"].to_string(),
            );
            user_data.insert("repeat".to_string(), data["repeat"].to_string());
        }
    };

    info!("Returning user data: {:?}\n", user_data);

    user_data
}

// ------------------------------------------------------------------------------------------------------------------------ //

pub async fn search(
    media_name: String,
    media_type: String,
    member_db: Vec<String>,
) -> (Vec<String>, Vec<String>) {
    info!("Searching for {} in {}", media_name, media_type);
    let client = reqwest::Client::new();
    let query = get_query("search");
    let json = json!({"query": query, "variables": {"search": media_name, "type": media_type.to_uppercase()}});
    info!("Query has been inserted into JSON");

    let res = client
        .post("https://graphql.anilist.co")
        .json(&json)
        .send()
        .await;

    info!("Sent request to AniList | SEARCH");
    let res = res.unwrap().json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["Media"];
    info!("Received response from AniList | SEARCH");

    // Anime Information | Try to find a better alternative to joining genres (IF POSSIBLE)
    let anime_id = &data["id"];
    let title = &data["title"]["romaji"];
    let status = &data["status"].to_string().replace('\"', "");
    let episodes = &data["episodes"];
    let genres: Vec<String> = data["genres"]
        .as_array()
        .expect("Failed to convert genres to array")
        .iter()
        .map(|v| {
            v.as_str()
                .expect("Failed to convert genre to string")
                .to_owned()
        })
        .collect();

    let genres_str = genres.join(", ");
    let mean_score = &data["meanScore"];
    let average_score = &data["averageScore"];
    let popularity = &data["popularity"]
        .as_i64()
        .unwrap()
        .to_formatted_string(&Locale::en);
    let favourites = &data["favourites"]
        .as_i64()
        .unwrap()
        .to_formatted_string(&Locale::en);
    let url = &data["siteUrl"];
    let avatar = &data["coverImage"]["extraLarge"];
    let banner = &data["bannerImage"];

    let new_avatar = match avatar {
        serde_json::Value::Null => "https://i.imgur.com/8QlQWvT.png",
        _ => avatar.as_str().unwrap(),
    };

    let new_banner = match banner {
        serde_json::Value::Null => "https://i.imgur.com/8QlQWvT.png",
        _ => banner.as_str().unwrap(),
    };

    info!("Creating hashmap of vecs");
    let mut lists: HashMap<&str, Vec<String>> = HashMap::new();
    lists.insert("Repeating", Vec::new());
    lists.insert("Current", Vec::new());
    lists.insert("Completed", Vec::new());
    lists.insert("Planning", Vec::new());
    lists.insert("Paused", Vec::new());
    lists.insert("Dropped", Vec::new());

    info!("Iterating through member list");
    for member in member_db {
        let user_data = user_scores(member.clone(), anime_id.as_i64().unwrap()).await;
        info!("User Data: {:?}", user_data);

        match user_data["status"].as_str() {
            "\"REPEATING\"" | "\"CURRENT\"" | "\"COMPLETED\"" | "\"PLANNING\"" | "\"PAUSED\""
            | "\"DROPPED\"" => {
                let status = match user_data["status"].as_str() {
                    "\"REPEATING\"" => "Repeating",
                    "\"CURRENT\"" => "Current",
                    "\"COMPLETED\"" => "Completed",
                    "\"PLANNING\"" => "Planning",
                    "\"PAUSED\"" => "Paused",
                    "\"DROPPED\"" => "Dropped",
                    _ => continue,
                };

                if let Some(list) = lists.get_mut(status) {
                    if status == "Completed" && user_data["repeat"] != "0" {
                        list.push(format!(
                            "**{}** - `{} repeat(s) | {}/10`",
                            member, user_data["repeat"], user_data["score"]
                        ));
                    } else if status == "Repeating" || status == "Current" {
                        list.push(format!(
                            "**{}** - `{} | {}/10`",
                            member, user_data["progress"], user_data["score"]
                        ));
                    } else {
                        list.push(format!("**{}** - `{}/10`", member, user_data["score"]));
                    }
                }
            }
            _ => continue,
        }
    }

    info!("Creating anime results");
    let mut anime_results: Vec<String> = [
        format!("`All Episodes :` **{}**", episodes),
        format!("`Status       :` **{}**", status),
        format!("`Avg Score    :` **{}%**", average_score),
        format!("`Mean Score   :` **{}%**", mean_score),
        format!("`Popularity   :` **{}**", popularity),
        format!("`Favourites   :` **{}**", favourites),
        format!("`Genres       :` **{}**\n", genres_str),
    ]
    .iter()
    .map(|x| x.trim_matches('"').to_string())
    .filter(|x| !x.contains("null"))
    .collect();

    let labels = [
        "Repeating",
        "Current",
        "Completed",
        "Planning",
        "Paused",
        "Dropped",
    ];

    info!("Iterating through labels and adding any that contain data");
    for label in &labels {
        if let Some(vec) = lists.get_mut(*label) {
            info!("{}: {:?}", label, vec);
            if !vec.is_empty() {
                anime_results.push(format!("`{}    :`\n> {}\n", label, vec.join("\n> ")));
            }
        }
    }

    let anime_info: Vec<String> = [
        title.to_string(),
        url.to_string(),
        new_avatar.to_string(),
        new_banner.to_string(),
    ]
    .iter()
    .map(|x| x.trim_matches('"').to_string())
    .collect();

    info!("Returning Information For {}", title);
    (anime_results, anime_info)
}

// ------------------------------------------------------------------------------------------------------------------------ //


pub async fn user_search(username: String) -> (Vec<String>, Vec<String>) {
    let client = reqwest::Client::new();
    let query = get_query("user");
    let json = json!({"query": query, "variables": {"name": username}});
    info!("Query has been inserted into JSON");

    let res = client
        .post("https://graphql.anilist.co")
        .json(&json)
        .send()
        .await;

    info!("Sent request to AniList | USER SEARCH");
    let res = res.unwrap().json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["User"];
    info!("Received response from AniList | USER SEARCH");

    let user_name = &data["name"];
    let user_url = &data["siteUrl"];
    let user_banner = &data["bannerImage"];
    let user_avatar = &data["avatar"]["large"];

    let new_avatar = match user_avatar {
        serde_json::Value::Null => "https://i.imgur.com/8QlQWvT.png",
        _ => user_avatar.as_str().unwrap(),
    };

    let new_banner = match user_banner {
        serde_json::Value::Null => "https://i.imgur.com/8QlQWvT.png",
        _ => user_banner.as_str().unwrap(),
    };

    let anime_stats = &data["statistics"]["anime"];
    let anime_count = &anime_stats["count"];
    let anime_mean_score = &anime_stats["meanScore"];
    let anime_minutes_watched = &anime_stats["minutesWatched"].as_u64().unwrap() * 60;
    let (hrs, _min, _sec) = hrtime::to_time(anime_minutes_watched);

    let anime_episodes_watched = &anime_stats["episodesWatched"];

    let manga_stats = &data["statistics"]["manga"];
    let manga_count = &manga_stats["count"];
    let manga_mean_score = &manga_stats["meanScore"];
    let manga_chapters_read = &manga_stats["chaptersRead"];
    let manga_volumes_read = &manga_stats["volumesRead"];

    info!("Creating first vector of user results");
    let user_results: Vec<String> = [
        format!("**[Anime Information](https://anilist.co/user/{}/animelist)**", user_name),
        format!("`Anime Count   :` {}", anime_count),
        format!("`Mean Score    :` {}%", anime_mean_score),
        format!("`Watch Time    :` {} hours", hrs),
        format!("`Episodes Watch:` {}\n", anime_episodes_watched),
        format!("**[Manga Information](https://anilist.co/user/{}/mangalist)**", user_name),
        format!("`Manga Count   :` {}", manga_count),
        format!("`Mean Score    :` {}%", manga_mean_score),
        format!("`Chapters Read :` {}", manga_chapters_read),
        format!("`Volumes Read  :` {}", manga_volumes_read),
    ].iter()
    .map(|x| x.trim_matches('"').to_string())
    .collect();

    info!("Vec 1: {:?}", user_results);

    info!("Creating second vector of user results");
    let user_info: Vec<String> = [
        user_name.to_string(),
        user_url.to_string(),
        new_banner.to_string(),
        new_avatar.to_string(),
    ].iter()
    .map(|x| x.trim_matches('"').to_string())
    .collect();

    info!("Returning results for : {}", username);
    (user_results, user_info)
}

// ------------------------------------------------------------------------------------------------------------------------ //