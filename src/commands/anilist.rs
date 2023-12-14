use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::model::prelude::*;
use serenity::prelude::*;
use crate::api::search_media::search;
use tracing::info;
use crate::api::access_db::anilist_guild_search;
use std::sync::Arc;
use std::env;

#[command]
pub async fn anime(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    info!("Running Anime Command -> Arguments Parsed: {}", args.message());
    let guild = msg.guild(&ctx.cache).unwrap();
    let media_name = args.message().to_string();
    let guild_id = *guild.id.as_u64() as i64;

    let db_url = env::var("DB_URL").expect("Expected a DB URL in the environment file");
    let pool = sqlx::postgres::PgPool::connect(&db_url).await?; // Connect to the database
    let shared_pool = Arc::new(pool); // Create an Arc of the database connection

    info!("Grabbing all members in guild with ID: {}", guild_id);
    let db_check = anilist_guild_search(guild_id, shared_pool.clone()).await?;
    info!("All Members Found with Guild: {:?}", db_check);

    let search = search(media_name, String::from("ANIME"), db_check).await;
    info!("Information Received From Search Function\nVector 1:\n{}\n\nVector 2:\n{}", search.0.join("\n"), search.1.join("\n"));

    match msg.channel_id.send_message(&ctx.http, |m| {
        m.embed(|e| { 
            e.title(&search.1[0])
            .url(&search.1[1])
            .thumbnail(&search.1[2])
            .image(&search.1[3])
            .description(format!("{}", search.0.join("\n")))
        })
    }).await {
        Ok(_) => (),
        Err(e) => println!("Error sending message: {:?}", e),
    };

    Ok(())
}