use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::model::prelude::*;
use serenity::prelude::*;

// Fix this

/*
enum Games {
    RainbowSixSiege = 0.00572957795,
    Valorant = 0.07,
    CS2 = 0.022,
    ApexLegends = 0.022,
    Fortnite = 0.005555,
    Overwatch = 0.0066,
    Rust = 0.1125,
    Destiny = 0.022,
}*/

#[command]
pub async fn avatar(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {

    let user = if args.is_empty() {
        msg.author.clone() 
    } else {
            match args.single::<UserId>()?.to_user(&ctx.http).await {
                Ok(user) => user,
                Err(_) => msg.author.clone(),
            }
    };

    msg.channel_id.send_message(&ctx.http, |m| {
        m.embed(|e| e.title(format!("{}'s Avatar", user.name)).image(user.face()))
    }).await?;

    Ok(())
}

#[command]
pub async fn banner(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {

        let user = if args.is_empty() {
            msg.author.clone()
        } else {
            match args.single::<UserId>()?.to_user(&ctx.http).await {
            Ok(user) => user,
            Err(_) => msg.author.clone(),
            }
        };
    
        let banner = match user.banner_url() {
            Some(banner) => banner,
            None => {
                msg.channel_id.say(&ctx.http, format!("{} has no banner.", user.name)).await?;
                return Ok(());
            }
        };
    
        msg.channel_id.send_message(&ctx.http, |m| {
            m.embed(|e| e.title(format!("{}'s Banner", user.name)).image(banner))
        }).await?;
    
        Ok(())
}
