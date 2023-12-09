use sqlx::Connection;
use sqlx::Row;

use tracing::info;
use std::env;


pub async fn anilist_user_search(user: i64) -> Result<String, sqlx::Error> {
    // Spawn a new task to handle the database connection
    let handle_user = tokio::spawn(
        async move {
            // Grab the database URL from the environment file
            let db_url: &str = &env::var("DB_URL").expect("Failed to get DB_URL from environment file");
            info!("Connecting to database");

            // Connect to the database
            let mut conn = sqlx::postgres::PgConnection::connect(db_url).await.unwrap();
            info!("Connected to database",);
            info!("Searching for user with ID: {}", user);
            
            // Query the database for the user
            let row = match sqlx::query("SELECT anilist_name FROM anilist WHERE discord_id = $1")
                .bind(user)
                .fetch_one(&mut conn).await {
                    Ok(row) => row,
                    Err(_) => {
                        info!("User {} was not found in the database\n", user);
                        return String::from("None"); // Return if user is not found
                    }
            };
            
            // Grab the user from the database
            let user = row.get("anilist_name");

            info!("Found User: {:?}", user);
            info!("Returning query for {}\n", user);

            // Return User
            return user
        }
    );
    // Grab the output of the handle_user task
    let handle_output = handle_user.await.unwrap();

    // Return Result<String> of user grabbed from database
    Ok(handle_output)
}   