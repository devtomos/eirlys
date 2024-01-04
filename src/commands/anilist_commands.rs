use crate::api::database_access::{lookup_guild, lookup_user, create_user, update_user};
use crate::api::anilist_api::{search_media, relation_names, user_search};
use crate::DatabasePool;
use tracing::info;

use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::builder::{CreateEmbed, CreateSelectMenuOption, CreateSelectMenu, CreateActionRow};
use serenity::model::prelude::*;
use serenity::prelude::*;
use serenity::model::gateway::Ready;
use serenity::model::user::OnlineStatus;
use serenity::model::prelude::Activity;
use serenity::async_trait;
use serenity::model::application::interaction::Interaction;
use serenity::utils::Colour;

// ------------------------------------------------------------------------------------------------------------------------ //

// TODO: Create a trait for the anilist api functions so that I can use one reqwst client instead of creating a new one for each function

#[command]
#[aliases("anisetup", "aniset", "anilist_setup", "setupani", "setupanilist")]
pub async fn setup(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let username = args.message().to_string();
    let data_read = ctx.data.read().await;
    let pool = data_read.get::<DatabasePool>().expect("Expected DatabasePool in TypeMap.");
    let pool = pool.lock().await;

    let anilist_user = user_search(username).await;
    let check_user_db = lookup_user(msg.author.id.into(), msg.guild_id.unwrap().into(), (*pool).clone().into()).await.unwrap();

    if check_user_db.is_empty() {
        info!("{} is not within the database. Adding them.", msg.author.name);
        create_user(msg.author.id.into(), msg.guild_id.unwrap().into(), anilist_user.1[0].clone(), anilist_user.1[4].parse().unwrap(), (*pool).clone().into()).await.unwrap();
        msg.channel_id.say(&ctx.http, format!("`{}` has been added to the database.", msg.author.name)).await?;
    } else {
        info!("{} is already within the database. Updating them.", msg.author.name);
        update_user(msg.author.id.into(), anilist_user.1[4].parse().unwrap(), anilist_user.1[0].clone(), (*pool).clone().into()).await.unwrap();
        msg.channel_id.say(&ctx.http, format!("`{}` has been updated in the database.", msg.author.name)).await?;
    }

    Ok(())  
}

// ------------------------------------------------------------------------------------------------------------------------ //

#[command]
#[aliases("aniuser", "userani")]
pub async fn user(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let mut username = args.message().to_string();
    let data_read = ctx.data.read().await;
    let pool = data_read.get::<DatabasePool>().expect("Expected DatabasePool in TypeMap.");
    let pool = pool.lock().await;

    if username.is_empty() {
        info!("No arguments passed, searching for user in database.");
        username = lookup_user(msg.author.id.into(), msg.guild_id.unwrap().into(), (*pool).clone().into()).await.unwrap();

        if username.is_empty() {
            info!("{} is not within the database.", msg.author.name);
            msg.channel_id.say(&ctx.http, format!("You have not setup your anilist account. Please use the `setup` command.")).await?;
            return Ok(());
        }
    }
    let user_search = user_search(username.clone()).await;
    
    if user_search.0.is_empty() {
        info!("{} was not found in the Anilist API.", username);
        msg.channel_id.say(&ctx.http, format!("`{}` was not found in the Anilist API. Did you misspell their name?", username)).await?;
        return Ok(());
    }

    match msg.channel_id.send_message(&ctx.http, |m| {
        m.embed(|e| {
            e.title(&user_search.1[0])
                .url(&user_search.1[1])
                .thumbnail(&user_search.1[3])
                .image(&user_search.1[2])
                .description(user_search.0.join("\n"))
        })

    }).await
    {
        Ok(_) => (),
        Err(e) => {
            println!("Error sending message: {:?}", e);
            msg.channel_id.send_message(&ctx.http, |m| {
                m.embed(|e| {
                    e.title("An Error Occurred")
                        .description("There was an error when sending the dropdown menu. Alert the owner, or try again later.")
                        .color(Colour::RED)
                
                })
            }).await?;
        },
    };

    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

#[command]
pub async fn anime(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let media_name = args.message().to_string();

    let all_media = relation_names(media_name.clone(), String::from("ANIME")).await;

    if all_media.0.is_empty() {
        info!("Nothing related or close to {} was found.", &media_name);
        msg.channel_id.say(&ctx.http, format!("There are no relations to the anime `{}`. Please try another anime or keyword.", &media_name)).await?;
        return Ok(());
    }

    let mut select_menu = CreateSelectMenu::default();
    select_menu.min_values(1);
    select_menu.placeholder("Select an anime");
    select_menu.custom_id("anime_dropdown");
    select_menu.max_values(1);

    select_menu.options(|options| {
        for media in all_media.0 {
            let mut create_option = CreateSelectMenuOption::default();
            create_option.label(&media);
            create_option.value(&media);
            options.add_option(create_option);
        }
        options
    });
    info!("Added all options to the select menu.");

    let mut action_row = CreateActionRow::default();
    let act = action_row.add_select_menu(select_menu);

    info!("Sending select menu with anime options.");
    match msg.channel_id.send_message(&ctx.http, |m| {
            m.components(|c| {
                c.add_action_row(act.to_owned())
            })
    }).await
    {
        Ok(_) => (),
        Err(e) => {
            println!("Error sending message: {:?}", e);
            msg.channel_id.send_message(&ctx.http, |m| {
                m.embed(|e| {
                    e.title("An Error Occurred")
                        .description("There was an error when sending the dropdown menu. Alert the owner, or try again later.")
                        .color(Colour::RED)
                
                })
            }).await?;
        },
    };
    
    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

#[command]
pub async fn manga(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let media_name = args.message().to_string();

    let all_media = relation_names(media_name.clone(), String::from("MANGA")).await;

    if all_media.0.is_empty() {
        info!("Nothing related or close to {} was found.", &media_name);
        msg.channel_id.say(&ctx.http, format!("There are no relations to the manga `{}`. Please try another manga or keyword.", &media_name)).await?;
        return Ok(());
    }

    let mut select_menu = CreateSelectMenu::default();
    select_menu.min_values(1);
    select_menu.placeholder("Select a manga");
    select_menu.custom_id("manga_dropdown");
    select_menu.max_values(1);

    select_menu.options(|options| {
        for media in all_media.0 {
            let mut create_option = CreateSelectMenuOption::default();
            create_option.label(&media);
            create_option.value(&media);
            options.add_option(create_option);
        }
        options
    });
    info!("Added all options to the select menu.");

    let mut action_row = CreateActionRow::default();
    let act = action_row.add_select_menu(select_menu);

    info!("Sending select menu with manga options.");
    match msg.channel_id.send_message(&ctx.http, |m| {
            m.components(|c| {
                c.add_action_row(act.to_owned())
            })
    }).await
    {
        Ok(_) => (),
        Err(e) => {
            println!("Error sending message: {:?}", e);
            msg.channel_id.send_message(&ctx.http, |m| {
                m.embed(|e| {
                    e.title("An Error Occurred")
                        .description("There was an error when sending the dropdown menu. Alert the owner, or try again later.")
                        .color(Colour::RED)
                
                })
            }).await?;

        },
    };
    
    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

// Added this to anilist_commands to easily maintain the anime/manga dropdowns
pub struct ComponentHandler;
#[async_trait]
impl EventHandler for ComponentHandler {
    async fn ready(&self, ctx: Context, ready: Ready) {
        let activity = Activity::playing("With Rust");
        ctx.set_presence(Some(activity), OnlineStatus::Idle).await;
        info!("{} is connected!", ready.user.name);
    }

    async fn interaction_create(&self, ctx: Context, interaction: Interaction) {
        if let Interaction::MessageComponent(command) = interaction {
            let data = command.data.clone();

            if data.custom_id.as_str() == "anime_dropdown" || data.custom_id.as_str() == "manga_dropdown" {
                info!("Command {:?} was used ", data.custom_id);

                command.defer(&ctx.http).await.unwrap();
                let guild_id = command.guild_id.unwrap_or(GuildId(0));

                let data_read = ctx.data.read().await;
                let pool = data_read.get::<DatabasePool>().expect("Expected DatabasePool in TypeMap.");
                let pool = pool.lock().await;

                let db_check = lookup_guild(guild_id.into(), (*pool).clone().into()).await.unwrap();
                let mut media_type = "ANIME";

                if data.custom_id.as_str() == "manga_dropdown" {
                    media_type = "MANGA";
                }
                
                info!("Searching for {} in the Anilist API.", data.values[0]);
                let search = search_media(data.values[0].clone(), media_type.to_string(), db_check).await;

                let mut embed = CreateEmbed::default();
                embed.title(&search.1[0])
                    .url(&search.1[1])
                    .thumbnail(&search.1[2])
                    .image(&search.1[3])
                    .description(search.0.join("\n"));

                info!("Editing message with {}'s information.", data.values[0]);
                match command
                    .edit_original_interaction_response(&ctx.http, |response| {
                        response
                            .add_embed(embed)
                    })
                    .await
                {
                    Ok(_) => (),
                    Err(e) => println!("Error sending message: {:?}", e),
                };
            }
        }
    }
}

// ------------------------------------------------------------------------------------------------------------------------ //