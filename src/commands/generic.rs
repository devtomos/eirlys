use rust_decimal::Decimal;
use rust_decimal::prelude::FromPrimitive;
use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::model::prelude::*;
use serenity::prelude::*;
use crate::general::gen_funcs::get_sens;

#[command]
pub async fn sensitivity(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let from_game = args.single::<String>()?.to_uppercase();
    let to_game = args.single::<String>()?.to_uppercase();
    let dpi = args.single::<f64>()?;
    let sens = args.single::<f64>()?;

    let conv_game1 = get_sens(&from_game).unwrap();
    let conv_game2 = get_sens(&to_game).unwrap();

    let convert_sens = Decimal::from_f64(((conv_game1 * dpi) * sens) / (conv_game2 * dpi)).unwrap();
    let convert_in360 = Decimal::from_f64(360.0 / (conv_game1 * dpi * 1.0 * sens)).unwrap();
    let convert_cm360 = Decimal::from_f64(360.0 / (conv_game1 * dpi * 1.0 * sens) * 2.54).unwrap();

    msg.reply(&ctx.http, format!("Sensitivity: `{}`\n`{}cm/360` | `{}in/360`", convert_sens.round_dp(2), convert_cm360.round_dp(2), convert_in360.round_dp(2))).await?;

    Ok(())
}

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