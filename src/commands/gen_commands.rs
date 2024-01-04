use rand::Rng;
use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::model::prelude::*;
use serenity::prelude::*;


// ------------------------------------------------------------------------------------------------------------------------ //

#[command]
#[aliases("50", "8ball", "8")]
pub async fn fifty(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let answers: [&str; 2] = ["Yes", "No"];
    let user_input = args.message().to_string();
    let random_num = rand::thread_rng().gen_range(0..2);

    msg.reply(
        &ctx.http,
        format!("{}: {}", user_input, answers[random_num]),
    )
    .await?;
    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

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

    msg.channel_id
        .send_message(&ctx.http, |m| {
            m.embed(|e| {
                e.title(format!("{}'s Avatar", user.name))
                    .image(user.face())
            })
        })
        .await?;

    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

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
            msg.channel_id
                .say(&ctx.http, format!("{} has no banner.", user.name))
                .await?;
            return Ok(());
        }
    };

    msg.channel_id
        .send_message(&ctx.http, |m| {
            m.embed(|e| e.title(format!("{}'s Banner", user.name)).image(banner))
        })
        .await?;

    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

#[command]
#[aliases("serveravatar", "serverav", "sav")]
pub async fn server_avatar(ctx: &Context, msg: &Message) -> CommandResult {
    let guild = match msg.guild(&ctx.cache) {
        Some(guild) => guild,
        None => {
            msg.channel_id
                .say(&ctx.http, "Groups and DMs don't have avatars.")
                .await?;
            return Ok(());
        }
    };

    let icon_url = match guild.icon_url() {
        Some(url) => format!("{}?size=1024", url), // Hack way to increase the size of the image
        None => {
            msg.channel_id
                .say(&ctx.http, "Server has no icon.")
                .await?;
            return Ok(());
        }
    };

    msg.channel_id
        .send_message(&ctx.http, |m| {
            m.embed(|e| e.title(format!("{}'s Icon", guild.name)).image(icon_url))
        })
        .await?;

    Ok(())
}

#[command]
#[aliases("serverinfo", "si")]
pub async fn server_info(ctx: &Context, msg: &Message) -> CommandResult {
    let guild = match msg.guild(&ctx.cache) {
        Some(guild) => guild,
        None => {
            msg.channel_id
                .say(&ctx.http, "Groups and DMs don't have a server info.")
                .await?;
            return Ok(());
        }
    };

    let owner = guild.owner_id.to_user(&ctx.http).await?;
    let members = guild.member_count;
    let emojis = guild.emojis.len();
    let roles = guild.roles.len();
    let channels = guild.channels(&ctx.http).await?.len();
    let creation_date = guild.id.created_at().format("%b %e, %Y @ %l:%M %p");

    let icon_url = match guild.icon_url() {
        Some(url) => format!("{}?size=1024", url),
        None => "https://i.imgur.com/8QlQWvT.png".to_string(),
    };

    let banner_url = match guild.banner_url() {
        Some(url) => format!("{}?size=1024", url),
        None => "https://i.imgur.com/8QlQWvT.png".to_string(),
    };

    msg.channel_id
        .send_message(&ctx.http, |m| {
            m.embed(|e| 
                e.title(format!("{}'s Information", guild.name))
                .thumbnail(icon_url)
                .image(banner_url)
                .description(format!("`Owner   :` **{}**\n`Members :` **{}**\n`Emojis  :` **{}**\n`Roles   :` **{}**\n`Channels:` **{}**\n`Created :` **{}**", owner.name, members, emojis, roles, channels, creation_date))
            )
        })
        .await?;

    Ok(())
}