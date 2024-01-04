use sqlx::postgres::PgPool;
use sqlx::Row;
use tracing::info;

pub async fn user_check(user_id: i64, guild_id: i64, anilist_name: String, anilist_id: i64, updated: bool, pool: PgPool) -> Result<(), sqlx::Error> {
    
    let _handle_conn: tokio::task::JoinHandle<Result<(), sqlx::Error>> = tokio::spawn(async move {
        info!("Checking if user exists in Database");

        if updated {
            info!("User already exists, updating Database entry");
            info!("Creating user with ID: {}", user_id);
            let old_user = match sqlx::query("SELECT anilist_name FROM tblanilist INNER JOIN tblinfo ON tblanilist.anilist_id = tblinfo.anilist_id INNER JOIN tblguild ON tblguild.discord_id = tbl.info.discord_id WHERE tblinfo.discord_id = $1")
                .bind(user_id)
                .fetch_one(&pool).await {
                    Ok(row) => row,
                    Err(_) => {
                        info!("User was not found in Database\n");
                        return Ok(());
                    }
                };
            let old_user: String = old_user.get("anilist_name");
            info!("Old User: {}", old_user);

            info!("Updating tblanilist");
            sqlx::query("UPDATE tblanilist SET anilist_name = $1 WHERE anilist_name = $2")
                .bind(old_user)
                .bind(anilist_name)
                .execute(&pool).await?;

            info!("User updated successfully");
        } else {
            info!("User is new, creating Database entry");
            info!("Adding to tblanilist");

            sqlx::query("INSERT INTO tblanilist (anilist_id, anilist_name, anilist_url) VALUES ($1, $2, $3)")
            .bind(anilist_id)
            .bind(anilist_name)
            .bind(format!("https://anilist.co/user/{}", anilist_id))
            .execute(&pool).await?;

            info!("Adding to tblinfo");
            sqlx::query("INSERT INTO tblinfo (discord_id, anilist_id) VALUES ($1, $2)")
                .bind(user_id)
                .bind(anilist_id)
                .execute(&pool).await?;
            
            info!("Adding to tblguild");
            sqlx::query("INSERT INTO tblguild (discord_id, guild_id) VALUES ($1, $2)")
                .bind(user_id)
                .bind(guild_id)
                .execute(&pool).await?;
            info!("User created successfully");
        }

        Ok(())
    });

    Ok(())
}


// ------------------------------------------------------------------------------------------------------------------------ //

pub async fn anilist_user_search(
    user_id: i64, 
    pool: PgPool,
) -> Result<String, sqlx::Error> {

    let handle_conn = tokio::spawn(async move {
        info!("Searching for user with ID: {}", user_id);

        let row = match sqlx::query("SELECT anilist_name FROM tblanilist INNER JOIN tblinfo ON tblanilist.anilist_id = tblinfo.anilist_id WHERE tblinfo.discord_id = $1 ")
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