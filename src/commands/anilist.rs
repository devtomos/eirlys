use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::model::prelude::*;
use serenity::prelude::*;
use crate::api::search_media::search;

#[command]
pub async fn anime(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let media_name = args.single::<String>()?.to_string();
    let search = search(media_name, "ANIME".to_string()).await;

    msg.reply(&ctx.http, search.join("\n")).await?;

    Ok(())
}