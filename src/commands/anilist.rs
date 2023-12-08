use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::model::prelude::*;
use serenity::prelude::*;
use crate::api::search_media::search;
use tracing::info;
use crate::api::access_db::anilist_user_search;

#[command]
pub async fn anime(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let media_name = args.message().to_string();
    info!("Got Anime: {}", media_name);
    let _database = anilist_user_search(msg.author.id.0.try_into().unwrap()).await?;
    let search = search(media_name, "ANIME".to_string()).await;
    info!("Information Received From Search Function\nVector 1:\n{}\n\nVector 2:\n{}", search.0.join("\n"), search.1.join("\n"));

    msg.channel_id.send_message(&ctx.http, |m| {
        m.embed(|e| { 
            e.title(&search.1[0])
            .url(&search.1[1])
            .thumbnail(&search.1[2])
            .image(&search.1[3])
            .description(format!("{}", search.0.join("\n")))
        })
    }).await?;

    Ok(())
}