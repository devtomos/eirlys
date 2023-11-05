use tokio_postgres::{Error, NoTls};
use tracing::info;
use std::env;


pub async fn search_anilist(user: i64) -> Result<String, Error> {
    let db_url: &str = &env::var("DB_URL").expect("Failed to get DB_URL from environment file");
    let (client, connection) =
        tokio_postgres::connect(db_url, NoTls).await?;

    info!("Connected to database -> Searching for user {}", user);

    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });

    let row = client
        .query_one("SELECT anilist_name FROM anilist WHERE discord_id = $1::BIGINT", &[&user])
        .await?;
    
    info!("Found User: {:?}", row.get::<_, String>(0));

    info!("Returning query for {}", user);
    Ok(row.get::<_, String>(0))
}