use sqlx::postgres::PgPool;
use sqlx::Row;
use std::sync::Arc;
use tracing::info;

pub async fn anilist_guild_search(
    guild_id: i64,
    pool: Arc<PgPool>,
) -> Result<Vec<String>, sqlx::Error> {
    // Spawn a new task to handle the database connection
    let handle_user = tokio::spawn(async move {
        // Connect to the database
        info!("Searching for guild with ID: {}", guild_id);

        // Query the database for the user
        let rows = match sqlx::query("SELECT anilist_name FROM tblanilist INNER JOIN tblinfo ON tblanilist.anilist_id = tblinfo.anilist_id INNER JOIN tblguild ON tblinfo.discord_id = tblguild.discord_id WHERE tblguild.guild_id = $1")
                .bind(guild_id)
                .fetch_all(&*pool).await {
                    Ok(rows) => rows,
                    Err(_) => {
                        info!("Guild was not found in Database\n");
                        return Vec::new();
                }
            };

        info!("Guild Found in Database");
        // Store all users within a vector
        let all_members: Vec<String> = rows.iter().map(|row| row.get("anilist_name")).collect();
        info!("Returning query \n");

        all_members
    });
    // Grab the output of the handle_user task
    let handle_output = handle_user.await.unwrap();

    // Return Result<i64> of user grabbed from database
    Ok(handle_output)
}
