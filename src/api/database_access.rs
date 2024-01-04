use sqlx::postgres::PgPool;
use sqlx::Row;
use tracing::info;

// ------------------------------------------------------------------------------------------------------------------------ //

/*
Create_User: 
    Arguments - User_ID, Guild_ID, Anilist_Name, Anilist_ID, Pool
    Returns - Result<(), sqlx::Error>

HOW IT WORKS: 
    Creates a new user within the database.
    If the user is already present within the database, it'll skip.
    This is to make sure that if the user is within other guilds, it won't create a duplicate entry.
*/
pub async fn create_user(user_id: i64, guild_id: i64, anilist_name: String, anilist_id: i64, pool: PgPool) -> Result<(), sqlx::Error> {
    info!("Creating user with ID: {}", user_id);

    match sqlx::query("INSERT INTO tblanilist (anilist_id, anilist_name, anilist_url) VALUES ($1, $2, $3)")
        .bind(anilist_id)
        .bind(anilist_name)
        .bind(format!("https://anilist.co/user/{}", anilist_id))
        .execute(&pool).await {
            Ok(_) => info!("User successfully set in tblanilist"),
            Err(_) => {
                info!("User already exists in tblanilist");
            }
        }
    
    match sqlx::query("INSERT INTO tblinfo (discord_id, anilist_id) VALUES ($1, $2)")
        .bind(user_id)
        .bind(anilist_id)
        .execute(&pool).await {
            Ok(_) => info!("User successfully set in tblinfo"),
            Err(_) => {
                info!("User already exists in tblinfo");
            }
        }
    
    match sqlx::query("INSERT INTO tblguild (discord_id, guild_id) VALUES ($1, $2)")
        .bind(user_id)
        .bind(guild_id)
        .execute(&pool).await {
            Ok(_) => info!("User successfully set in tblguild"),
            Err(_) => {
                info!("User already exists in tblguild");
            }
        }

    info!("User created successfully\n");
    Ok(())

}

// ------------------------------------------------------------------------------------------------------------------------ //

/*
Update_User: 
    Arguments - User_ID, Anilist_ID, Anilist_Name, Pool
    Returns - Result<(), sqlx::Error>

HOW IT WORKS: 
    Updates the user's anilist name and anilist id.
    If the user is not present within the database it won't update.

COMMENT:
    Guild ID was not added as, if the user were to update his username, there would not be a need to update them all manually.
*/
pub async fn update_user(user_id: i64, anilist_id: i64, anilist_name: String, pool: PgPool) -> Result<(), sqlx::Error> {
    info!("Updating user with anilist ID: {}", anilist_id);

    info!("Updating tblanilist");
    match sqlx::query("UPDATE tblanilist SET anilist_name = $1 WHERE anilist_id IN ( SELECT tblinfo.anilist_id FROM tblinfo WHERE tblinfo.discord_id = $2) AND anilist_id = $3")
        .bind(anilist_name)
        .bind(user_id)
        .bind(anilist_id)
        .execute(&pool).await {
            Ok(_) => info!("User successfully updated in tblanilist"),
            Err(_) => {
                info!("User does not exist in the database");
                return Ok(())
            }
        }

    info!("User updated successfully\n");
    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

/*
Lookup_User: 
    Arguments - User_ID, Guild_ID, Pool
    Returns - Result<String, sqlx::Error>

HOW IT WORKS: 
    Looks up the user's anilist name. Though user must of used setup within that guild to be shown.
    If the user is not present within the database it won't return anything.
*/
pub async fn lookup_user(
    user_id: i64,
    guild_id: i64,
    pool: PgPool,
) -> Result<String, sqlx::Error> {
    

    let handle_conn = tokio::spawn(async move {
        info!("Searching for user with ID: {}", user_id);

        let row = match sqlx::query("SELECT anilist_name FROM tblanilist INNER JOIN tblinfo ON tblanilist.anilist_id = tblinfo.anilist_id INNER JOIN tblguild ON tblguild.discord_id = tblinfo.discord_id WHERE tblinfo.discord_id = $1 AND tblguild.guild_id = $2")
            .bind(user_id)
            .bind(guild_id)
            .fetch_one(&pool).await {
                Ok(row) => row,
                Err(_) => {
                    info!("User was not found in Database\n");
                    return String::new();
                }
        };

        info!("User was found in Database.");
        row.get("anilist_name")
    });

    info!("Returning database query\n");    
    let handle_output = handle_conn.await.unwrap();
    Ok(handle_output)
}

// ------------------------------------------------------------------------------------------------------------------------ //

/*
Lookup_Guild: 
    Arguments - Guild_ID, Pool
    Returns - Result<Vec<String>, sqlx::Error>

HOW IT WORKS:
    Looks up all the users within the guild and returns a vector of their anilist names.
    If the guild is not present within the database it won't return anything.
*/
pub async fn lookup_guild(
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

        info!("Guild was found in Database");
        let all_members: Vec<String> = rows.iter().map(|row| row.get("anilist_name")).collect();
        all_members
    });

    let handle_output = handle_user.await.unwrap();
    Ok(handle_output)
}

// ------------------------------------------------------------------------------------------------------------------------ //