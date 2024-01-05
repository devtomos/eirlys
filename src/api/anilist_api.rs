use crate::api::anilist_queries::{get_query, QUERY_URL, return_time};
use num_format::{Locale, ToFormattedString};
use serde_json::json;
use std::{collections::HashMap, cmp};
use tracing::info;

// ------------------------------------------------------------------------------------------------------------------------ //

/*
Relation_names: 
    Arguments - Media_Name, Media_Type
    Returns - Vec<String>, HashMap<String, String>

HOW IT WORKS: 
    Takes in two arguments, the media name and the media type (anime/manga).
    It sends a request to anilist api and returns a vector of the most relevant results and a hashmap of the results
    The hashmap is used when a user picks an option from the dropdown menu, within discord.
*/
pub async fn relation_names(media_name: String, media_type: String) -> (Vec<String>, HashMap<String, String>) {
    let client = reqwest::Client::new();
    let query = get_query("relation_stats");

    let json = json!({"query": query, "variables": {"search": media_name, "type": media_type.to_uppercase()}});
    let res = client
        .post(QUERY_URL)
        .json(&json)
        .send()
        .await;
    let res = res.unwrap();

    if res.status() != 200 {
        info!("Anilist API returned a non-200 status code: {}", res.status());
        return (Vec::new(), HashMap::new()); // Add check in anilist_commands to see if vec is empty
    }

    info!("Received a response from Anilist API.");
    info!("Now parsing response.");
    let res = res.json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["Page"]["media"];

    let mut relations_array = HashMap::new();
    let mut relations_list = Vec::new();
    let mut duplicates = Vec::new();
   
    info!("Adding results to the relations list and hashmap.");
    let media_name = media_name.to_uppercase();
    let media_name_uppercase: Vec<_> = media_name.split(" ").collect();
    for media_item in data.as_array().unwrap().iter().rev() {
        let title_romaji = media_item["title"]["romaji"].as_str().unwrap_or_default().to_uppercase();
        let title_english = media_item["title"]["english"].as_str().unwrap_or_default().to_uppercase();
        let title_native = media_item["title"]["native"].as_str().unwrap_or_default().to_uppercase();
        let synonyms = media_item["synonyms"].as_str().unwrap_or_default().to_uppercase();

        if title_romaji.contains(&media_name_uppercase[0]) || title_english.contains(&media_name_uppercase[0]) || title_native.contains(&media_name_uppercase[0]) || synonyms.contains(&media_name_uppercase[0]) {
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
    info!("Finished adding all results, now returning the relations list and hashmap.\n");

    relations_list.reverse(); // Reverse the list to keep the most relevant results at the top
    relations_list.truncate(25); // Truncate the list to 25 results
    (relations_list, relations_array)
}

// ------------------------------------------------------------------------------------------------------------------------ //

/*
User_Scores: 
    Arguments - User_Name, Media_ID
    Returns - HashMap<String, String>

HOW IT WORKS: 
    Takes in two arguments, the users anilist name and the media_ID of the anime/manga.
    It sends a request to anilist api and returns a hashmap with the users scores, progress, status, etc.
*/
pub async fn user_scores(user_name: String, media_id: i64) -> HashMap<String, String> {
    let client = reqwest::Client::new();
    let query = get_query("user_stats");
    let mut user_data: HashMap<String, String> = HashMap::new();
    let json = json!({"query": query, "variables": {"userName": user_name, "mediaId": media_id}});

    let res = client
        .post(QUERY_URL)
        .json(&json)
        .send()
        .await;

    let res = res.unwrap().json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["MediaList"];

    info!("Parsing the response from Anilist API.\nMatching data to see if the data is invalid or not.");
    match data {
        serde_json::Value::Null => {
            info!("NULL data, returning empty hashmap.");
            user_data.insert("status".to_string(), "null".to_string());
            return user_data;
        }
        _ => {
            info!("Data is not NULL, adding data to hashmap.");
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

    user_data
}

// ------------------------------------------------------------------------------------------------------------------------ //

/*
Search_Media: 
    Arguments - Media_Name, Media_Type, Member_DB
    Returns - Vec<String>, Vec<String>

HOW IT WORKS: 
    Takes in 3 arguments, the media name, the media type (anime/manga), and a vector of members within the database.
    It sends a request to anilist api and returns a vector of the anime/manga information and a vector for general use information (title, url, avatar, banner, etc.)
*/
pub async fn search_media(
    media_name: String,
    media_type: String,
    member_db: Vec<String>,
) -> (Vec<String>, Vec<String>) {

    let client = reqwest::Client::new();
    let query = get_query("search");
    let json = json!({"query": query, "variables": {"search": media_name, "type": media_type.to_uppercase()}});


    let res = client
        .post(QUERY_URL)
        .json(&json)
        .send()
        .await;
    let res = res.unwrap();

    if res.status() != 200 {
        info!("Anilist API returned a non-200 status code: {}", res.status());
        return (Vec::new(), Vec::new());
    }

    info!("Received a response from Anilist API.");
    info!("Now parsing response.");
    let res = res.json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["Media"];
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

    info!("Packing up the data into two vectors.");
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

    let anime_info: Vec<String> = [
        title.to_string(),
        url.to_string(),
        new_avatar.to_string(),
        new_banner.to_string(),
    ]
    .iter()
    .map(|x| x.trim_matches('"').to_string())
    .collect();

    info!("Packed both Vectors. Checking to see if Member_db is empty.");
    if !member_db.is_empty() {
        info!("Member_db is not empty.");
        info!("Creating a hashmap for the lists.\nLooping through all members within the member_db list.");
        let mut lists: HashMap<&str, Vec<String>> = HashMap::new();
        lists.insert("Repeating", Vec::new());
        lists.insert("Current", Vec::new());
        lists.insert("Completed", Vec::new());
        lists.insert("Planning", Vec::new());
        lists.insert("Paused", Vec::new());
        lists.insert("Dropped", Vec::new());
        let labels = [
        "Repeating",
        "Current",
        "Completed",
        "Planning",
        "Paused",
        "Dropped",
        ];

        for member in member_db {
            let user_data = user_scores(member.clone(), anime_id.as_i64().unwrap()).await;

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
                        } else if status == "Dropped" || status == "Paused" {
                            list.push(format!("**{}** - `{} | {}/10`", member, user_data["progress"], user_data["score"]));
                        } else {
                            list.push(format!(
                                "**{}** - `{}/10`",
                                member, user_data["score"]
                            ));
                        
                        }
                    }
                }
                _ => continue,
            }
        }


        for label in &labels {
            if let Some(vec) = lists.get_mut(*label) {
                if !vec.is_empty() {
                    anime_results.push(format!("`{}    :`\n> {}\n", label, vec.join("\n> ")));
                }
            }
        }
    }

    info!("Returning the anime results and anime info.\n");
    (anime_results, anime_info)
}

// ------------------------------------------------------------------------------------------------------------------------ //

/*
User_Search: 
    Arguments - User_Name
    Returns - Vec<String>, Vec<String>

HOW IT WORKS: 
    Takes in only the anilist username, of the user or what they have inputted.
    It sends a request to anilist api and returns a vector of the users anime/manga information and a vector for general use information (name, url, avatar, banner, etc.)
*/
pub async fn user_search(username: String) -> (Vec<String>, Vec<String>) {
    let client = reqwest::Client::new();
    let query = get_query("user");
    let json = json!({"query": query, "variables": {"name": username}});
    let res = client
        .post(QUERY_URL)
        .json(&json)
        .send()
        .await;
    let res = res.unwrap();

    if res.status() != 200 {
        info!("Anilist API returned a non-200 status code: {}", res.status());
        return (Vec::new(), Vec::new());
    }

    info!("Received a response from Anilist API.");
    info!("Now parsing response.");
    let res = res.json::<serde_json::Value>().await.unwrap();
    let data = &res["data"]["User"];

    let user_id = &data["id"];
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
    let anime_seconds = &anime_stats["minutesWatched"].as_u64().unwrap() * 60;
    let get_time = return_time(anime_seconds, 2);

    let anime_episodes_watched = &anime_stats["episodesWatched"];

    let manga_stats = &data["statistics"]["manga"];
    let manga_count = &manga_stats["count"];
    let manga_mean_score = &manga_stats["meanScore"];
    let manga_chapters_read = &manga_stats["chaptersRead"];
    let manga_volumes_read = &manga_stats["volumesRead"];

    info!("Packing up the data into two vectors.");

    let user_results: Vec<String> = [
        format!("**[Anime Information](https://anilist.co/user/{}/animelist)**", user_name),
        format!("`Anime Count   :` {}", anime_count),
        format!("`Mean Score    :` {}%", anime_mean_score),
        format!("`Watch Time    :` {}", get_time),
        format!("`Episodes Watch:` {}\n", anime_episodes_watched),
        format!("**[Manga Information](https://anilist.co/user/{}/mangalist)**", user_name),
        format!("`Manga Count   :` {}", manga_count),
        format!("`Mean Score    :` {}%", manga_mean_score),
        format!("`Chapters Read :` {}", manga_chapters_read),
        format!("`Volumes Read  :` {}", manga_volumes_read),
    ].iter()
    .map(|x| x.trim_matches('"').to_string())
    .collect();

    let user_info: Vec<String> = [
        user_name.to_string(),
        user_url.to_string(),
        new_banner.to_string(),
        new_avatar.to_string(),
        user_id.to_string(),
    ].iter()
    .map(|x| x.trim_matches('"').to_string())
    .collect();

    info!("Returning the user results and user info.\n");
    (user_results, user_info)
}

// ------------------------------------------------------------------------------------------------------------------------ //