use crate::api::queries::get_query;
use num_format::{Locale, ToFormattedString};
use serde_json::json;
use std::collections::HashMap;
use tracing::info;
use std::collections::HashSet;

pub async fn relation_search(media_name: String, media_type: String) -> (Vec<String>, HashMap<String, i64>) {
    let client = reqwest::Client::new();
    let query = get_query("relation_search");
    let json = json!({"query": query, "variables": {"search": media_name}});
    let res = client
        .post("https://graphql.anilist.co")
        .json(&json)
        .send()
        .await;

    let res = res.unwrap().json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["Page"]["media"];
    let mut duplicates = HashSet::new();
    let media_name_first_word = media_name.split_whitespace().next().unwrap().to_lowercase();
    let mut relations_list = Vec::new();
    let mut relations_array = HashMap::new();

    for media in data.as_array().unwrap().iter().rev() {
        let title_romaji = media.get("title").and_then(|t| t.get("romaji")).and_then(|t| t.as_str()).unwrap_or("").to_lowercase();
        let title_english = media.get("title").and_then(|t| t.get("english")).and_then(|t| t.as_str()).unwrap_or("").to_lowercase();
        let title_native = media.get("title").and_then(|t| t.get("native")).and_then(|t| t.as_str()).unwrap_or("").to_lowercase();
        let synonyms = media.get("synonyms").and_then(|s| s.as_str()).unwrap_or("").to_lowercase();

        if title_romaji.contains(&media_name_first_word)
            || title_english.contains(&media_name_first_word)
            || title_native.contains(&media_name_first_word)
            || synonyms.contains(&media_name_first_word)
        {
            let media_types = media.get("type").and_then(|t| t.as_str()).unwrap_or("").to_uppercase();

            if media_type == media_types.to_uppercase() {
                let title = media.get("title").and_then(|t| t.get("romaji")).and_then(|t| t.as_str()).unwrap_or("");
                let id = media.get("id").and_then(|i| i.as_i64()).unwrap_or(0);

                if duplicates.contains(title) {
                    relations_list.push(format!("[{}]", &title[..std::cmp::min(title.len(), 95)]));
                    relations_array.insert(format!("[{}]", &title[..std::cmp::min(title.len(), 95)]), id);
                } else {
                    duplicates.insert(title.to_string());
                    relations_list.push(title[..std::cmp::min(title.len(), 98)].to_string());
                    relations_array.insert(title[..std::cmp::min(title.len(), 98)].to_string(), id);
                }
            }
        }
    }
    
    (relations_list[0..std::cmp::min(relations_list.len(), 24)].to_vec(), relations_array)
}

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
            info!("Data is not null, inserting data into hashmap\n");
            user_data.insert("progress".to_string(), data["progress"].to_string());
            user_data.insert("status".to_string(), data["status"].to_string());
            user_data.insert("score".to_string(), data["score"].to_string());
            user_data.insert(
                "progressVolumes".to_string(),
                data["progressVolumes"].to_string(),
            );
            user_data.insert("repeat".to_string(), data["repeat"].to_string());
        }
    }

    user_data
}

pub async fn search(
    media_name: String,
    media_type: String,
    member_db: Vec<String>,
) -> (Vec<String>, Vec<String>) {
    info!("Searching for {} in {}", media_name, media_type);
    let client = reqwest::Client::new();
    let query = get_query("search");

    // Insert GrahpQL Query and Variables
    // Query: Search
    // Variables: "Search": Anime_Name, "Type": Anime_Type
    let json = json!({"query": query, "variables": {"search": media_name, "type": media_type.to_uppercase()}});
    info!("Query has been inserted into JSON");

    let res = client
        .post("https://graphql.anilist.co")
        .json(&json)
        .send()
        .await;

    info!("Sent request to AniList");
    let res = res.unwrap().json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["Media"];
    info!("Received response from AniList");

    // Anime Information | Try to find a better alternative to joining genres (IF POSSIBLE)
    let anime_id = &data["id"];
    let title = &data["title"]["romaji"];
    let status = &data["status"].to_string().replace("\"", "");
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
        serde_json::Value::Null => {
            serde_json::Value::String("https://i.imgur.com/FdFIkxG.png".to_string())
        }
        _ => avatar.clone(),
    };

    let new_banner = match banner {
        serde_json::Value::Null => {
           serde_json::Value::String("https://i.imgur.com/FdFIkxG.png".to_string())
        }
        _ => banner.clone(),
    };


    let mut lists: HashMap<&str, Vec<String>> = HashMap::new();
    lists.insert("Repeating", Vec::new());
    lists.insert("Current", Vec::new());
    lists.insert("Completed", Vec::new());
    lists.insert("Planning", Vec::new());
    lists.insert("Paused", Vec::new());
    lists.insert("Dropped", Vec::new());

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

    info!("Returning Information For {}", title);
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

    (anime_results, anime_info)
}