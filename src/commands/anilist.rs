use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::model::prelude::*;
use serenity::prelude::*;
use crate::api::search_media::search;
use tracing::info;

#[command]
pub async fn anime(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let media_name = args.message().to_string();
    let search = search(media_name, "ANIME".to_string()).await;
    info!("Information Received From Search Function\nVector 1: {}\n\nVector 2: {}", search.0.join("\n"), search.1.join("\n"));
    
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