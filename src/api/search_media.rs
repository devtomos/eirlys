use std::collections::HashMap;
use crate::api::queries::get_query;
use tracing::info;

pub async fn search(media_name: String, media_type: String) -> String {
    info!("Searching for {} in {}", media_name, media_type);
    let client = reqwest::Client::new();
    let mut map = HashMap::new();
    let query = get_query("search");

    map.insert("query", query);
    map.insert("variables", format!("{{\"search\": \"{}\", \"type\": \"{}\"}}", media_name, media_type.to_uppercase()));
    info!("Inserted values into map: {:?}", map);

    let res = client.post("https://graphql.anilist.co")
                                    .json(&map)
                                    .send()
                                    .await;

    info!("Response: {:?}", res);
    res.unwrap().text().await.unwrap()
}