use sqlx::postgres::PgPool;
use sqlx::Row;
use tracing::info;

// ------------------------------------------------------------------------------------------------------------------------ //

pub async fn anilist_user_search(
    user_id: i64, 
    pool: PgPool,
) -> Result<String, sqlx::Error> {

    let handle_conn = tokio::spawn(async move {
        info!("Searching for user with ID: {}", user_id);

        let row = match sqlx::query("SELECT anilist_name FROM tblanilist INNER JOIN tblinfo ON tblanilist.anilist_id = tblinfo.anilist_id WHERE tblinfo.discord_id = $1")
            .bind(user_id)
            .fetch_one(&pool).await {
                Ok(row) => row,
                Err(_) => {
                    info!("User was not found in Database\n");
                    return String::new();
                }
        };
    
    info!("Found user in Database");
    row.get("anilist_name")
    });

    info!("Returning database query");    
    let handle_output = handle_conn.await.unwrap();
    Ok(handle_output)
}

// ------------------------------------------------------------------------------------------------------------------------ //

pub async fn anilist_guild_search(
    guild_id: i64,
    pool: PgPool,
) -> Result<Vec<String>, sqlx::Error> {

    let handle_user = tokio::spawn(async move {
        info!("Searching for guild with ID: {}", guild_id);

        let rows = match sqlx::query("SELECT anilist_name FROM tblanilist INNER JOIN tblinfo ON tblanilist.anilist_id = tblinfo.anilist_id INNER JOIN tblguild ON tblinfo.discord_id = tblguild.discord_id WHERE tblguild.guild_id = $1")
                .bind(guild_id)
                .fetch_all(&pool).await {
                    Ok(rows) => rows,
                    Err(_) => {
                        info!("Guild was not found in Database\n");
                        return Vec::new();
                }
            };

        info!("Guild Found in Database");

        let all_members: Vec<String> = rows.iter().map(|row| row.get("anilist_name")).collect();
        info!("Returning database query: {:?}\n", all_members);

        all_members
    });

    let handle_output = handle_user.await.unwrap();

    Ok(handle_output)
}

// ------------------------------------------------------------------------------------------------------------------------ //