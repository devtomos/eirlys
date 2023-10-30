use tokio_postgres::NoTls;
use tracing::info;
use std::env;

pub async fn search_anilist(user: i64) -> String {
    let db_url: &str = &env::var("DB_URL").expect("Failed to get DB_URL from environment file");
    let (client, _connection) = tokio_postgres::connect(db_url, NoTls)
                                                                                        .await.expect("Failed to connect to database");

    info!("Connected to database -> Searching for user {}", user);
    let db_query = client.query("SELECT anilist_name FROM anilist WHERE discord_id = $1", &[&user])
                                    .await.expect("Failed to query database");

    info!("Returning query for {}", user);
    let result = db_query[0].get(0);
    //tokio_postgres::close(client).expect("Failed to close connection");
    result
}