use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::model::prelude::*;
use serenity::prelude::*;
use crate::api::search_media::search;
use tracing::info;
use crate::api::access_db::anilist_user_search;

#[command]
pub async fn anime(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    info!("Running Anime Command -> Arguments Parsed: {}", args.message());
    let guild = msg.guild(&ctx.cache).unwrap();
    let mut store_member: Vec<String> = Vec::new();
    let media_name = args.message().to_string();

    info!("Looping all members in guild");
    for (key, _value) in guild.members.iter() {
        // FIXME: This is too slow for now
        // TODO: Include Guild ID in Database, check to see where command was called and only grab users within that guild.
        // TODO: Either do all of that ^ or connect to the database ONCE and then grab users to speed up the process.
        let db_check = anilist_user_search(key.0.try_into().unwrap()).await?;
        if db_check != "None" {
            store_member.push(db_check);
        }
    }

    info!("DB Vector: {:?}", store_member);
    let search = search(media_name, "ANIME".to_string(), store_member).await;
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