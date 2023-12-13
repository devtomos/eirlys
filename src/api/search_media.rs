use std::collections::HashMap;
use crate::api::queries::get_query;
use tracing::info;
use serde_json::json;
use num_format::{Locale, ToFormattedString};

pub async fn user_scores(user_name: String, media_id: i64) -> HashMap<String, String> {
    // Insert GrahpQL Query and Variables
    // Query: Search
    // Variables: "userName": user_name, "mediaId": media_id
    let client = reqwest::Client::new();
    let query = get_query("user_stats");
    let mut user_data: HashMap<String, String> = HashMap::new();
    let json = json!({"query": query, "variables": {"userName": user_name, "mediaId": media_id}});
    info!("Query has been inserted into JSON");
    
    let res = client.post("https://graphql.anilist.co")
                    .json(&json)
                    .send()
                    .await;
    
    info!("Sent request to AniList | USER SEARCH");
    let res = res.unwrap().json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["MediaList"];
    info!("Received response from AniList | USER SEARCH");

    info!("Checking to see if data is null\n");
    let _hash_data = match data {
        serde_json::Value::Null => {
            info!("Data is null, returning null hashmap");
            user_data.insert("status".to_string(), "null".to_string());
            return user_data
        },
        _ => {
            info!("Data is not null, inserting data into hashmap");
            user_data.insert("progress".to_string(), data["progress"].to_string());
            user_data.insert("status".to_string(), data["status"].to_string());
            user_data.insert("score".to_string(), data["score"].to_string());
            user_data.insert("progressVolumes".to_string(), data["progressVolumes"].to_string());
            user_data.insert("repeat".to_string(), data["repeat"].to_string());
        }
    };

    return user_data
}


pub async fn search(media_name: String, media_type: String, member_db: Vec<String>) -> (Vec<String>, Vec<String>) {
    info!("Searching for {} in {}", media_name, media_type);
    let client = reqwest::Client::new();
    let query = get_query("search");

    // Insert GrahpQL Query and Variables
    // Query: Search
    // Variables: "Search": Anime_Name, "Type": Anime_Type
    let json = json!({"query": query, "variables": {"search": media_name, "type": media_type.to_uppercase()}});
    info!("Query has been inserted into JSON");

    let res = client.post("https://graphql.anilist.co")
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

    let mut repeating: Vec<String> = Vec::new();
    let mut planning: Vec<String> = Vec::new();
    let mut completed: Vec<String> = Vec::new();
    let mut paused: Vec<String> = Vec::new();
    let mut dropped: Vec<String> = Vec::new();
    let mut current: Vec<String> = Vec::new();

    for member in member_db {
        let user_data = user_scores(member.clone(), anime_id.as_i64().unwrap()).await;
        
        match user_data["status"].as_str() {
            "\"REPEATING\"" => repeating.push(format!("**{}** - `{} | {}/10`", member, user_data["progress"], user_data["score"])),
            "\"CURRENT\"" => current.push(format!("**{}** - `{} | {}/10`", member, user_data["progress"], user_data["score"])),
            "\"COMPLETED\"" => {
                if user_data["repeat"] != "0" {
                    repeating.push(format!("**{}** - `{} repeats | {}/10`", member, user_data["repeat"], user_data["score"]));
                } else {
                    completed.push(format!("**{}** - `{}/10`", member, user_data["score"]));
                }
            },

            "\"PLANNING\"" => planning.push(format!("**{}**", member)),
            "\"PAUSED\"" => paused.push(format!("**{}**", member)),
            "\"DROPPED\"" => dropped.push(format!("**{}**", member)),
            _ => (),
        }
    }

    // TODO: Loop through vec and removing any redudant data -> ONLY NEED TO DO THIS FOR  ALL EPS, STATUS, AVG SCORE ETC
    // TODO: Add current episode and when the next episode is due if it's currently airing

    info!("Returning Information For {}", title);
    let mut anime_results: Vec<String> = vec![
        format!("`All Episodes :` **{}**", episodes),
        format!("`Status       :` **{}**", status), 
        format!("`Avg Score    :` **{}%**", average_score), 
        format!("`Mean Score   :` **{}%**", mean_score),
        format!("`Popularity   :` **{}**", popularity), 
        format!("`Favourites   :` **{}**", favourites),
        format!("`Genres       :` **{}**\n", genres_str),
        ].iter().map(|x| x.trim_matches('"').to_string().replace("null", "N/A")).collect();

    let mut vecs = [&mut repeating, &mut current, &mut completed, &mut planning, &mut paused, &mut dropped];
    let labels = ["Repeating", "Current", "Completed", "Planning", "Paused", "Dropped"];
        
    for (vec, label) in vecs.iter_mut().zip(labels.iter()) {
        if !vec.is_empty() {
            anime_results.push(format!("`{}    :`\n> {}\n", label, vec.join("\n> ")));
        }
    }

    let anime_info: Vec<String> = vec![
        title.to_string(),
        url.to_string(),
        avatar.to_string(),
        banner.to_string(),
        ].iter().map(|x| x.trim_matches('"').to_string()).collect();

    return (anime_results, anime_info)

}